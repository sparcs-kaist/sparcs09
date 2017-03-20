from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from apps.session import views

urlpatterns = [
    url(r'^$', lambda x: HttpResponseRedirect('/')),
    url(r'^login/$', views.login),
    url(r'^callback/$', views.callback),
    url(r'^logout/$', views.logout),
    url(r'^unregister/$', views.unregister),
]
