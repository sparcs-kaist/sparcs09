from rest_framework import viewsets
from rest_framework.response import Response

from apps.core.models import Content
from apps.core.permissions import IsParticipantOrNone
from apps.core.serializers import (
    ContentSerializer,
)


class ContentViewSet(viewsets.ModelViewSet):
    lookup_value_regex = '\d+'
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsParticipantOrNone]

    # [GET] /contents/
    def list(self, request):
        return Response({
            'detail': 'Listing is not allowed here.',
        }, status=405)

    # [POST] /contents/
    def create(self, request):
        return Response({
            'detail': 'Creating is not allowed here.',
        }, status=405)

    # [GET] /contents/<pk>/
    def retrieve(self, request, pk=None):
        content = self.get_object()
        serializer = ContentSerializer(content)
        return Response({
            'content': serializer.data,
        })

    # [PUT] /contents/<pk>/
    def update(self, request, pk=None):
        return Response({
            'detail': 'Updating is not allowed.',
        }, status=405)

    # [PATCH] /contents/<pk>/
    def partial_update(self, request, pk=None):
        return Response({
            'detail': 'Partial updating is not allowed.',
        }, status=405)

    # [DELETE] /contents/<pk>/
    def destroy(self, request, pk=None):
        content = self.get_object()
        if not request.user == content.item.host:
            return Response({
                'detail': 'Hiding content is only available to the host.',
            }, status=403)
        content = self.get_object()
        content.is_hidden = True
        content.save()
        return Response({})
