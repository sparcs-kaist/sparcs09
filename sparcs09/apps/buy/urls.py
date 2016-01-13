from django.conf.urls import include, url
from django.contrib import admin
from sparcs09.apps.buy import views

urlpatterns = [
    url('^$', views.main),
    url('^list/$', views.record),
    url('^item/(?P<pid>\d+)/$', views.item),
    url('^item/(?P<pid>\d+)/list/$', views.item_total),
]
