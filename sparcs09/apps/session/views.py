from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponseForbidden, JsonResponse
import json
import urllib
import random


# /session/login/
def login(request):
    if request.user.is_authenticated():
        return redirect('/')

    request.session['next'] = request.META.get('HTTP_REFERER', '/')
    url = 'https://sso.sparcs.org/api/token/require/?app=sparcs09'
    if settings.DEBUG:
        url = 'https://sso.sparcs.org/api/token/require/?url=' + \
           request.build_absolute_uri('/session/callback/')
    return redirect(url)

# /session/callback/
def callback(request):
    tokenid = request.GET.get('tokenid', '')

    profile = urllib.urlopen('https://sso.sparcs.org/api/token/info/?tokenid=' + tokenid)
    profile = json.load(profile)

    username = profile['sparcs_id']
    if not username:
        return HttpResponseForbidden()

    user_list = User.objects.filter(username=username)
    if len(user_list) == 0:
        user = User.objects.create_user(username=username,
                                        email=profile['email'],
                                        password=str(random.getrandbits(32)),
                                        first_name=profile['first_name'],
                                        last_name=profile['last_name'])
        user.save()
    else:
        user = user_list[0]

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)

    nexturl = request.session.pop('next', '/')
    return redirect(nexturl)


# /session/logout/
def logout(request):
    if not request.user.is_authenticated():
        return redirect('/')

    auth.logout(request)
    return redirect('/')


# /session/unregister/
def unregister(request):
    return JsonResponse({"status": 0})
