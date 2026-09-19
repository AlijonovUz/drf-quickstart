from apps.base.permissions import DjangoModelPermissions


class DynamicPermissionMixin:
    permission_classes = [DjangoModelPermissions]
