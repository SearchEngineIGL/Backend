from rest_framework.permissions import BasePermission

class IsUser(BasePermission):
    def has_permission(self, request, view):
        print("hello User")
        print(request.user.user_type)
        return request.user.user_type == 'simple' 