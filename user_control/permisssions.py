from rest_framework import permissions


class IsOwnerOrAdminControl(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user) or request.user.role == "admin"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsOwnerControl(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user)

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdminControl(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )
