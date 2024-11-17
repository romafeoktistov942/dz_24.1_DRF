from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверяем права на создание и удаление."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """Проверяем права на просмотр и редактирование."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
