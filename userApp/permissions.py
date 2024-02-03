from rest_framework.permissions import BasePermission

class IsSimpleUser(BasePermission):
    def has_permission(self, request, view):
        print("hello")
        print(request.user.user_type)
        return request.user.user_type == 'simple' 