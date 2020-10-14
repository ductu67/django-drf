from rest_framework.permissions import BasePermission
from apps.authentication.constants import RolesType


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == None:
                raise PermissionError('You need to add roles for users')
            return request.user.role.name == RolesType.ADMIN.value
        return False


class IsHumanResourceUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == None:
                raise PermissionError('You need to add roles for users')
            return request.user.role.name == RolesType.HR.value or request.user.role.name == RolesType.ADMIN.value
        return False
