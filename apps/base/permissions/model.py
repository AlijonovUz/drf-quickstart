from rest_framework import permissions


class DjangoModelPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }

    def has_permission(self, request, view):
        if getattr(view, "_ignore_model_permissions", False):
            return True

        user = request.user
        if not user or (not user.is_authenticated and self.authenticated_users_only):
            return False

        if (
                getattr(view, "safe_methods_unrestricted", False)
                and request.method in permissions.SAFE_METHODS
        ):
            return True

        model = self._queryset(view).model
        return user.has_perms(self.get_required_permissions(request.method, model))
