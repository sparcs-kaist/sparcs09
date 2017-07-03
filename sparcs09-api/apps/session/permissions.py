from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    """
    Permission check for authenticated + terms agreed users
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.profile.terms_agreed
