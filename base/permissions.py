"""
This file holds custom permission for the project
"""
# third-party
from rest_framework.permissions import AllowAny, BasePermission

# local Django
from base.utils import get_object_or_404


class IsAuthenticatedToCreatePassword(BasePermission):
    """ custom permission class to create password"""

    def has_permission(self, request, _view):
        """ custom permission class to create password if
        password is not created yet"""
        return request.user.is_authenticated and not request.user.verified


class IsAuthenticated(BasePermission):
    """ custom permission class to validate profile setup"""

    def has_permission(self, request, _view):
        """ custom permission validation to check if user had
        done with his/her profile"""

        return request.user and request.user.is_authenticated


class IsAuthenticatedToUpdateProfile(BasePermission):
    """ custom permission class to update profile"""

    def has_permission(self, request, _view):
        """ custom permission class to update profile if
                password is created by user """
        return request.user.is_authenticated and request.user.verified


class IsAdmin(BasePermission):
    """ custom permission class to verify admin user"""

    def has_permission(self, request, _view):
        """ return true if user role is admin """
        return request.user.is_authenticated and request.user.is_admin


class IsEndUser(BasePermission):
    """ custom permission class to verify request user is end user"""

    def has_permission(self, request, _view):
        """ return true if user role is user role """
        return request.user.is_authenticated and request.user.is_car_owner


class IsTechnician(BasePermission):
    """ custom permission class to verify request user is technician"""

    def has_permission(self, request, _view):
        """ return true if user role is user role """
        return request.user.is_authenticated and request.user.is_technician


class RoleBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in
    view.action_permissions
    """

    def has_permission(self, request, view):
        for permission_class, actions in getattr(view, 'action_permissions',
                                                 {}).items():
            if view.action in actions:
                return permission_class().has_permission(request, view)
        return False
