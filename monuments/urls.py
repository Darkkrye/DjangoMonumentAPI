from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from . import views

schema_view = get_swagger_view(title='Monuments API')


urlpatterns = [
    # Users routes
    url(r'^user/(?P<pk>\d+)$', views.user_pk, name='user'),
    url(r'^user$', views.user, name='user'),


    # Notes routes
    url(r'^note/(?P<id>\d+)$', views.note_pk, name='note_id'),
    url(r'^note$', views.note, name='note'),


    # Monuments routes
    url(r'^monument/(?P<id>\d+)$', views.monument_pk, name='monument_id'),
    url(r'^monument$', views.monument, name='monument'),


    # Addresses routes
    url(r'^address/(?P<id>\d+)$', views.address_pk, name='address_id'),
    url(r'^address$', views.address, name='address'),


    # Cities routes
    url(r'^city/(?P<id>\d+)$', views.city_pk, name='city_id'),
    url(r'^city$', views.city, name='city'),


    # Login routes
    url(r'^login$', views.login, name='login'),

    url(r'^', schema_view, name="docs")

]
