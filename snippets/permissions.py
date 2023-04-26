from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class IsMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        snippet = obj
        if user.is_superuser:
            return True
        if snippet.users.filter(id=user.id).exists():
            return True
        return False
