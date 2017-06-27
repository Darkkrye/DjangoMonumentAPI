from django.conf.urls import url

from . import views

urlpatterns = [
    # Users routes
    url(r'^user$', views.users, name='index'),
    url(r'^user/(?P<pk>\d+)$', views.users, name='index'),
    url(r'^user$', views.user, name='user_post'),
    url(r'^user/(?P<pk>\d+)$', views.user, name='user_delete'),

    # Notes routes
    url(r'^note$', views.notes, name='notes'),
    url(r'^note/(?P<id>\d+)$', views.notes, name='notes'),
    url(r'^note$', views.note, name='note_post'),
    url(r'^note/(?P<id>\d+)$', views.note, name='note_delete'),

    # Monuments routes
    url(r'^monument$', views.monuments, name='monuments'),
    url(r'^monument/(?P<id>\d+)$', views.monuments, name='monuments'),
    url(r'^monument$', views.monument, name='monument_post'),
    url(r'^monument/(?P<id>\d+)$', views.monument, name='monument_delete'),

    # Addresses routes
    url(r'^address$', views.addresses, name='addresses'),
    url(r'^address/(?P<id>\d+)$', views.addresses, name='address_delete'),
    url(r'^address$', views.address, name='address_post'),
    url(r'^address/(?P<id>\d+)$', views.address, name='address_delete'),

    # Cities routes
    url(r'^city$', views.cities, name='cities'),
    url(r'^city/(?P<id>\d+)$', views.cities, name='cities'),
    url(r'^city$', views.city, name='city_post'),
    url(r'^city/(?P<id>\d+)$', views.city, name='city_delete'),

    # Login routes
    url(r'^login$', views.login, name='login'),
]
