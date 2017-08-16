from rest_framework import permissions

from apps.session.permissions import IsAuthenticated


class IsItemHostOrReadOnly(IsAuthenticated):
    """
    Permission check for items
    - Allow item update/delete permission for host
    - Allow item-related job permission for authenticated users
    """
    message = (
        'Modifying others\' item is not allowed; '
        'for join/commenting items, you should login'
    )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        path_info = list(filter(None, request.path.split('/')))
        suffix = path_info[-1] if len(path_info) else ''
        if suffix in ['comments', 'payments']:
            if self.has_permission(request, view):
                return True
        return obj.host == request.user


class IsCommentWriterOrReadOnly(IsAuthenticated):
    """ Permission check for comment writer """
    message = 'Deleting others\' comments is not allowed'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.writer == request.user
