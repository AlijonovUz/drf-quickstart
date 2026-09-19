from rest_framework import permissions


def RequirePermission(codename):
    class _RequirePermission(permissions.BasePermission):
        def has_permission(self, request, view):
            user = request.user
            return bool(user and user.is_authenticated and user.has_perm(codename))

        def __repr__(self):
            return f"RequirePermission({codename!r})"

    clean_name = codename.replace(".", "_")
    _RequirePermission.__name__ = f"RequirePermission_{clean_name}"
    _RequirePermission.__qualname__ = f"RequirePermission_{clean_name}"
    return _RequirePermission


def RequirePermissions(*codenames):
    class _RequirePermissions(permissions.BasePermission):
        def has_permission(self, request, view):
            user = request.user
            return bool(user and user.is_authenticated and user.has_perms(codenames))

        def __repr__(self):
            return f"RequirePermissions{codenames!r}"

    clean_names = "_".join(c.replace(".", "_") for c in codenames)
    suffix = f"_{clean_names}" if clean_names else ""
    _RequirePermissions.__name__ = f"RequirePermissions{suffix}"
    _RequirePermissions.__qualname__ = f"RequirePermissions{suffix}"
    return _RequirePermissions


def RequireAnyPermission(*codenames):
    class _RequireAnyPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            user = request.user
            if not user or not user.is_authenticated:
                return False
            return any(user.has_perm(c) for c in codenames)

        def __repr__(self):
            return f"RequireAnyPermission{codenames!r}"

    clean_names = "_".join(c.replace(".", "_") for c in codenames)
    suffix = f"_{clean_names}" if clean_names else ""
    _RequireAnyPermission.__name__ = f"RequireAnyPermission{suffix}"
    _RequireAnyPermission.__qualname__ = f"RequireAnyPermission{suffix}"
    return _RequireAnyPermission
