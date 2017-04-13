from django.conf.urls import url
from apps.buy import views

urlpatterns = [
    url('^$', views.main),
    url('^list/$', views.record),
    url('^item/(?P<pid>\d+)/$', views.item),
    url('^item/(?P<pid>\d+)/list/$', views.item_total),
]
