from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_staff
        )


class IsAuthOrStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            (request.method in SAFE_METHODS)
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            (request.method in SAFE_METHODS)
            or request.user.is_staff
            or obj.author == request.user
        )
