from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^users$', views.users, name='index'),
    url(r'^user$', views.user, name='user_post'),
    url(r'^user/(?P<pk>\d+)$', views.user, name='user_delete'),

    url(r'^login$', views.login, name='login'),

    url(r'^note$', views.note, name='note_post'),
    url(r'^note/(?P<id>\d+)$', views.note, name='note_delete'),

    url(r'^monument$', views.monument, name='monument_post'),
    url(r'^monument/(?P<id>\d+)$', views.monument, name='monument_delete'),

    url(r'^address$', views.address, name='address_post'),
    url(r'^address/(?P<id>\d+)$', views.address, name='address_delete'),

    url(r'^city$', views.city, name='city_post'),
    url(r'^city/(?P<id>\d+)$', views.city, name='city_delete'),
]
