from apps.base.permissions import FullDjangoModelPermissions


class DynamicPermissionMixin:
    permission_classes = [FullDjangoModelPermissions]
