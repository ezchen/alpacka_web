from rest_framework import permissions

class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, account):
        if request.user:
            return account == request.user
        return False

class IsPhoneVerified(permissions.BasePermission):
    message = "Account's phone has not been verified yet"
    def has_permission(self, request, view):
        if request.user:
            return account.phone_verified
        return False

class IsEmailVerified(permissions.BasePermission):
    message = "Account's email has not been verified yet"
    
    def has_permission(self, request, view):
        if request.user:
            return account.email_verified
        return False
