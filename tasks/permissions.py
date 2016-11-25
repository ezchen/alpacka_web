from rest_framework import permissions

class IsAuthorOfTask(permissions.BasePermission):
    def has_object_permission(self, request, view, task):
        if request.user:
            return task.author == request.user
        return false

class IsCourier(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return request.user.is_courier
        return false
