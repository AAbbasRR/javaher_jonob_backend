# grouping import
from rest_framework.permissions import (
    AllowAny as AllowAnyPermission,
    IsAuthenticated as IsAuthenticatedPermission,
)
from rest_framework.permissions import BasePermission


class IsSuperUserPermission(BasePermission):
    """
    Allows access only to type superuser users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.type == request.user.UserTypeOptions.Superuser
        )


class IsStaffOrAbovePermission(BasePermission):
    """
    Allows access only to type staff users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.type
            in [
                request.user.UserTypeOptions.Staff,
                request.user.UserTypeOptions.Superuser,
            ]
        )


class IsSecretaryOrAbovePermission(BasePermission):
    """
    Allows access only to type secretary users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.type
            in [
                request.user.UserTypeOptions.Secretary,
                request.user.UserTypeOptions.Staff,
                request.user.UserTypeOptions.Superuser,
            ]
        )


class IsWorkerOrAbovePermission(BasePermission):
    """
    Allows access only to type worker users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.type
            in [
                request.user.UserTypeOptions.Worker,
                request.user.UserTypeOptions.Secretary,
                request.user.UserTypeOptions.Staff,
                request.user.UserTypeOptions.Superuser,
            ]
        )
