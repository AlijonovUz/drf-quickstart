from django.core.exceptions import FieldDoesNotExist
from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    DEFAULT_HIDDEN_FIELDS = ["is_active"]
    DEFAULT_READONLY_FIELDS = ["id", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        hidden_fields = getattr(self.Meta, "hide_fields", self.DEFAULT_HIDDEN_FIELDS)
        for field_name in hidden_fields:
            self.fields.pop(field_name, None)

        readonly_fields = list(self.DEFAULT_READONLY_FIELDS) + list(
            getattr(self.Meta, "extra_readonly_fields", [])
        )
        for field_name in readonly_fields:
            if field_name in self.fields:
                self.fields[field_name].read_only = True

        related_fields = getattr(self.Meta, "related_fields", [])

        if isinstance(related_fields, dict):
            items = related_fields.items()
        else:
            items = [(f, None) for f in related_fields]

        for field_name, val in items:
            self._build_related_field(field_name, val)

        self._restrict_to_view_fields()

    def _build_related_field(self, field_name, val):
        source = field_name
        fields_to_serialize = val
        exclude_fields = None
        nested_related = {}
        explicit_source = False

        if isinstance(val, dict):
            explicit_source = "source" in val
            source = val.get("source", field_name).replace("__", ".")
            fields_to_serialize = val.get(
                "fields", None if val.get("exclude") else "__all__"
            )
            exclude_fields = val.get("exclude", None)
            nested_related = val.get("related_fields", {})

        if field_name in self.fields:
            self.fields[field_name].write_only = True

        is_many, related_model = self._resolve_related_model(source)
        if related_model is None:
            return

        if (
            is_many
            and not explicit_source
            and hasattr(related_model, "objects")
            and hasattr(related_model.objects, "active")
        ):
            source = f"{source}.active"

        if isinstance(fields_to_serialize, type) and issubclass(
            fields_to_serialize, serializers.Serializer
        ):
            serializer_class = fields_to_serialize
        else:
            serializer_class = get_short_serializer(
                related_model,
                fields=fields_to_serialize,
                exclude=exclude_fields,
                nested_related_fields=nested_related,
            )

        self.fields[f"{field_name}_info"] = serializer_class(
            source=source, read_only=True, many=is_many
        )

    def _resolve_related_model(self, source):
        curr_model = self.Meta.model
        field = None
        try:
            for part in source.split("."):
                field = curr_model._meta.get_field(part)
                curr_model = field.related_model
        except (FieldDoesNotExist, AttributeError):
            return False, None

        if field is None:
            return False, None

        is_many = (
            getattr(field, "many_to_many", False)
            or getattr(field, "one_to_many", False)
            or getattr(field, "auto_created", False)
        )
        return is_many, curr_model

    def _restrict_to_view_fields(self):
        view = self.context.get("view")
        allowed = getattr(view, "serializer_fields", None) if view else None
        if not allowed:
            return

        allowed = set(allowed)
        allowed |= {f"{f}_info" for f in allowed}

        for field_name in set(self.fields) - allowed:
            self.fields.pop(field_name)

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        for field_name in ("created_at", "updated_at"):
            if field_name in ret:
                ret[field_name] = ret.pop(field_name)
        return ret


def get_short_serializer(
    model_class, fields=None, exclude=None, nested_related_fields=None
):
    if fields is not None:
        _fields = fields
    elif exclude is None:
        _fields = "__all__"
    else:
        _fields = None

    meta_attrs = {"model": model_class, "related_fields": nested_related_fields or {}}
    if exclude:
        meta_attrs["exclude"] = exclude
    else:
        meta_attrs["fields"] = _fields

    meta_class = type("Meta", (), meta_attrs)
    return type(
        f"{model_class.__name__}ShortSerializer",
        (BaseModelSerializer,),
        {"Meta": meta_class},
    )