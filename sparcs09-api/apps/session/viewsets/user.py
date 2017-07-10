import logging

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response

from apps.core.models import UserLog
from apps.session.serializers import UserSerializer


logger = logging.getLogger(UserLog.GROUP_ACCOUNT)


class UserViewSet(viewsets.ModelViewSet):
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

        serializer = UserSerializer(user, data=request.data, show_private=True)
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
    def destroy():
        return Response({
            'detail': 'Deleting user is not allowed.',
        }, status=403)
