import logging

from rest_framework import viewsets
from rest_framework.response import Response

from apps.core.models import Comment, UserLog
from apps.core.permissions import IsCommentWriterOrReadOnly


logger = logging.getLogger(UserLog.GROUP_COMMENT)


class CommentViewSet(viewsets.ModelViewSet):
    lookup_value_regex = '\d+'
    queryset = Comment.objects.all()
    permission_classes = [IsCommentWriterOrReadOnly]

    # [GET] /comments/
    def list(self, request):
        return Response({
            'detail': 'Listing is not allowed here.',
        }, status=405)

    # [POST] /comments/
    def create(self, request):
        return Response({
            'detail': 'Creating is not allowed here.',
        }, status=405)

    # [GET] /comments/<pk>/
    def retrieve(self, request, pk=None):
        return Response({
            'detail': 'Retrieving is not allowed here.',
        }, status=405)

    # [PUT] /comments/<pk>/
    def update(self, request, pk=None):
        return Response({
            'detail': 'Updating comment is not allowed.',
        }, status=403)

    # [PATCH] /comments/<pk>/
    def partial_update(self, request, pk=None):
        return Response({
            'detail': 'Updating comment is not allowed.',
        }, status=403)

    # [DELETE] /comments/<pk>/
    def destroy(self, request, pk=None):
        comment = self.get_object()
        comment.is_deleted = True
        comment.save()

        logger.info('delete', {
            'r': request,
            'extra': {'comment': comment.id},
        })
        return Response({})
