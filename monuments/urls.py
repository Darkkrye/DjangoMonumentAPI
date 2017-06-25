from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^users$', views.users, name='index'),
    url(r'^user$', views.user, name='user_post'),
    url(r'^user/(?P<pk>\d+)$', views.user, name='user_delete'),
]