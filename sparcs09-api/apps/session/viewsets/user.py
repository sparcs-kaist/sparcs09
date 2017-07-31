import logging

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.core.models import UserLog
from apps.session.serializers import UserSerializer
from apps.session.sparcsssov2 import Client


logger = logging.getLogger(UserLog.GROUP_ACCOUNT)
sso_client = Client(settings.SSO_ID, settings.SSO_KEY)


class UserViewSet(viewsets.ViewSet):
    lookup_field = 'sid'
    lookup_value_regex = '[0-9a-f]+'

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

    # [GET] /users/<sid>/
    def retrieve(self, request, sid=None):
        user = User.objects.filter(username=sid).first()
        if not user:
            return Response({
                'detail': 'No such user.',
            }, status=404)

        serializer = UserSerializer(
            user, show_private=request.user.username == sid,
        )

        logger.info('search', {
            'r': request,
            'extra': {'sid': sid},
        })

        return Response({
            'user': serializer.data,
        })

    # [PUT] /users/<sid>/
    def update(self, request, sid=None):
        return Response({
            'detail': 'Updating user is not allowed. Use PATCH',
        }, status=403)

    # [PATCH] /users/<sid>/
    def partial_update(self, request, sid=None):
        user = User.objects.filter(username=sid).first()
        if not user:
            return Response({
                'detail': 'No such user.',
            }, status=404)
        elif request.user.username != sid:
            return Response({
                'detail': 'Updating others profile is forbidden.',
            }, status=403)

        serializer = UserSerializer(
            user, data=request.data, show_private=True, partial=True,
        )
        if not serializer.is_valid():
            return Response({
                'detail': 'Not valid data.',
                'errors': serializer.errors,
            }, status=400)

        serializer.save()

        logger.info('update', {
            'r': request,
            'extra': {'sid': sid, **request.data},
        })

        return Response({
            'user': serializer.data,
        })

    # [DELETE] /users/<sid>/
    def destroy(self, request, sid=None):
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
        return Response({
            'success': True,
        })
