from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        team = obj
        if user.is_superuser:
            return True
        if team.users.filter(id=user.id).exists():
            return True
        return False
