import logging

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from apps.core.models import Item, UserLog
from apps.core.permissions import IsItemHostOrReadOnly
from apps.core.serializers import (
    CommentCreateSerializer, CommentFullSerializer, CommentSerializer,
    ItemSerializer,
)
from apps.core.utils import get_limit_offset


logger = logging.getLogger(UserLog.GROUP_ITEM)
logger_comment = logging.getLogger(UserLog.GROUP_COMMENT)


class ItemViewSet(viewsets.ModelViewSet):
    lookup_value_regex = '\d+'
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsItemHostOrReadOnly]

    # [GET] /items/
    def list(self, request):
        pass

    # [POST] /items/
    def create(self, request):
        pass

    # [GET] /items/<pk>/
    def retrieve(self, request, pk=None):
        pass

    # [PUT] /items/<pk>/
    def update(self, request, pk=None):
        pass

    # [PATCH] /items/<pk>/
    def partial_update(self, request, pk=None):
        pass

    # [DELETE] /items/<pk>/
    def destroy(self, request, pk=None):
        pass

    # [GET, POST] /items/<pk>/comments/
    @detail_route(methods=['get', 'post'])
    def comments(self, request, pk=None):
        item = self.get_object()
        return {
            'GET': self.comments_get,
            'POST': self.comments_post,
        }[request.method](request, item)

    # [GET] /items/<pk>/comments/
    def comments_get(self, request, item):
        limit, offset = get_limit_offset(request.GET)

        response = []
        comments = item.comments.order_by('id')[offset:offset+limit]
        for comment in comments:
            serializer_class = CommentSerializer
            if request.user in [comment.writer, item.host]:
                serializer_class = CommentFullSerializer
            response.append(serializer_class(comment).data)

        return Response({
            'count': item.comments.all().count(),
            'comments': response,
        })

    # [POST] /items/<pk>/comments/
    def comments_post(self, request, item):
        serializer = CommentCreateSerializer(data=request.data, context={
            'item': item,
            'writer': request.user,
        })
        if not serializer.is_valid():
            return Response({
                'detail': 'Not valid data.',
                'errors': serializer.errors,
            }, status=400)

        serializer.save()

        logger_comment.info('write', {
            'r': request,
            'extra': {'item': item.id},
        })
        return Response({
            'comment': serializer.data,
        })
