from rest_framework import viewsets
from apps.base.mixins import (
    DynamicPermissionMixin,
    AutoSchemaMixin,
)


class BaseManageViewSet(AutoSchemaMixin, DynamicPermissionMixin, viewsets.ModelViewSet):
    pass


class BaseReadOnlyViewSet(
    AutoSchemaMixin, DynamicPermissionMixin, viewsets.ReadOnlyModelViewSet
):
    pass
