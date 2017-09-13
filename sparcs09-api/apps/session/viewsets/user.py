import logging

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from apps.core.models import UserLog
from apps.core.serializers import UserLogSerializer
from apps.core.utils import get_limit_offset
from apps.session.serializers import (
    UserFullSerializer, UserProfileUpdateSerializer, UserPublicSerializer,
)
from apps.session.sparcsssov2 import Client


logger = logging.getLogger(UserLog.GROUP_ACCOUNT)
sso_client = Client(settings.SSO_ID, settings.SSO_KEY)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    lookup_value_regex = '[0-9a-f]+'
    queryset = User.objects.all()

    # [GET] /users/
    def list(self, request):
        return Response({
            'detail': 'Listing user is not allowed.',
        }, status=403)

    # [POST] /users/
    def create(self, request):
        return Response({
            'detail': 'Creating user is not allowed.',
        }, status=403)

    # [GET] /users/<username>/
    def retrieve(self, request, username=None):
        user = self.get_object()
        serializer_class = UserPublicSerializer
        if request.user == user:
            serializer_class = UserFullSerializer

        serializer = serializer_class(user)
        return Response({
            'user': serializer.data,
        })

    # [PUT] /users/<username>/
    def update(self, request, username=None):
        return Response({
            'detail': 'Updating user is not allowed. Use PATCH',
        }, status=403)

    # [PATCH] /users/<username>/
    def partial_update(self, request, username=None):
        user = self.get_object()
        if request.user != user:
            return Response({
                'detail': 'Updating others profile is forbidden.',
            }, status=403)

        serializer = UserProfileUpdateSerializer(
            user.profile, data=request.data, partial=True,
        )
        if not serializer.is_valid():
            return Response({
                'detail': 'Not valid data.',
                'errors': serializer.errors,
            }, status=400)

        serializer.save()

        logger.info('update', {
            'r': request,
            'extra': {**serializer.validated_data},
        })
        return Response({
            'user': serializer.data,
        })

    # [DELETE] /users/<username>/
    def destroy(self, request, username=None):
        return Response({
            'detail': 'Deleting user is not allowed.',
        }, status=403)

    # [POST] /users/unregister/
    @list_route(methods=['post'])
    def unregister(self, request):
        """
        It follows SPARCS SSO unregister API specification
        Do NOT change its url / request / response format
        """
        bad_response = Response({
            'success': False,
            'reason': 'Invalid request or no such user',
        }, status=400)

        try:
            sid = sso_client.parse_unregister_request(request.POST)
        except:
            return bad_response

        user = User.objects.filter(username=sid).first()
        if not user:
            return bad_response

        # TODO: check this user can be unregistered or not
        some_condition = True
        if not some_condition:
            return Response({
                'success': False,
                'reason': 'some-critical-reason',
                'link': 'https://09.sparcs.org/some-policy-link',
            })

        user.delete()

        logger.info('delete', {
            'r': request,
            'extra': {'sid': sid},
        })
        return Response({
            'success': True,
        })

    # [GET] /users/<username>/logs/
    @detail_route(methods=['get'])
    def logs(self, request, username=None):
        user = self.get_object()
        if request.user != user:
            return Response({
                'detail': 'Retrieving others logs is not allowed',
            })

        limit, offset = get_limit_offset(request.GET)
        group = request.GET.get('group', '')
        logs = UserLog.objects.filter(user=user, is_hidden=False)
        if group:
            logs = logs.filter(group=group)
        logs = logs.order_by('-time')[offset:offset+limit]

        serializer = UserLogSerializer(logs, many=True)
        return Response({
            'logs': serializer.data,
        })
