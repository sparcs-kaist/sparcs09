import logging
import re

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from apps.core.models import UserLog
from apps.session.models import UserProfile
from apps.session.serializers import UserFullSerializer
from apps.session.sparcsssov2 import Client


logger = logging.getLogger(UserLog.GROUP_ACCOUNT)
sso_client = Client(settings.SSO_ID, settings.SSO_KEY)


class SessionViewSet(viewsets.ViewSet):
    lookup_field = 'token'
    lookup_value_regex = '[0-9a-f]+'

    # [POST] /sessions/
    def create(self, request):
        code = request.data.get('code', '')
        if not re.match(r'[0-9a-f]+', code):
            return Response({
                'detail': 'Invalid token format.',
            }, status=400)

        try:
            user_info = sso_client.get_user_info(code)
        except:
            return Response({
                'detail': 'Invalid or expired token.',
            }, status=400)

        if not user_info['kaist_id']:
            return Response({
                'detail': 'Not kaist members.',
            }, status=403)

        sid, email = user_info['sid'], user_info['email']
        user = User.objects.filter(username=sid).first()

        # new members - create user and profile
        if not user:
            name = user_info['first_name'] + user_info['last_name']
            user = User.objects.create_user(
                username=sid,
                email=email,
                last_name=name,
            )
            profile = UserProfile(user=user)
            profile.save()
            user.save()

            logger.info('create', {
                'r': request,
                'uid': user.username,
                'extra': {
                    'email': email,
                    'name': name,
                },
            })
        else:
            # update email at every login
            user.email = email
            user.save()

        # issue a token
        token = Token.objects.get_or_create(user=user)
        serializer = UserFullSerializer(user)

        logger.info('login', {'r': request, 'uid': user.username})

        return Response({
            'token': token[0].key,
            'user': serializer.data,
        })

    # [DELETE] /sessions/<token>/
    def destroy(self, request, token=None):
        token_obj = Token.objects.filter(key=token).first()
        if not token_obj:
            return Response({
                'detail': 'No such token.',
            }, status=404)

        sid = token_obj.user.username
        token_obj.delete()

        # redirect_uri should be either empty or a 09 page
        main_uri = request.build_absolute_uri('/')
        redirect_uri = request.data.get('redirect_uri', main_uri)
        if not redirect_uri.startswith(main_uri):
            redirect_uri = main_uri

        logger.info('logout', {
            'r': request,
            'uid': sid,
            'extra': {'redirect_uri': redirect_uri},
        })

        return Response({
            'logout_url': sso_client.get_logout_url(sid, redirect_uri),
        })
