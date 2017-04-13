from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponseForbidden, HttpResponse
from apps.session.sparcsssov2 import Client
import random


sso_client = Client(settings.SSO_ID, settings.SSO_KEY)


# /session/login/
def login(request):
    if request.user.is_authenticated:
        return redirect('/')

    request.session['next'] = request.META.get('HTTP_REFERER', '/')

    login_url, state = sso_client.get_login_params()
    request.session['sso_state'] = state
    return redirect(login_url)


# /session/callback/
def callback(request):
    state_before = request.session['sso_state']
    state = request.GET.get('state', '')

    if state != state_before:
        return HttpResponseForbidden()

    code = request.GET.get('code', '')
    profile = sso_client.get_user_info(code)

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
    if not request.user.is_authenticated:
        return redirect('/')

    auth.logout(request)
    return redirect('/')


# /session/unregister/
def unregister(request):
    sso_unregister_msg = """
    <script>
        alert("You cannot unregister SPARCS 09 to save logs");
        window.history.back();
    </script>
    """
    return HttpResponse(sso_unregister_msg)
