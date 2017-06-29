from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from . import views

schema_view = get_swagger_view(title='Monuments API')


urlpatterns = [
    # Users routes
    url(r'^user$', views.user, name='user'),
    url(r'^user/(?P<pk>\d+)$', views.user_pk, name='user'),

    # Notes routes
    url(r'^note$', views.note, name='note'),
    url(r'^note/(?P<id>\d+)$', views.note_pk, name='note_id'),

    # Monuments routes
    url(r'^monument$', views.monument, name='monument'),
    url(r'^monument/(?P<id>\d+)$', views.monument, name='monument_id'),

    # Addresses routes
    url(r'^address$', views.address, name='address'),
    url(r'^address/(?P<id>\d+)$', views.address, name='address_id'),

    # Cities routes
    url(r'^city$', views.city, name='city'),
    url(r'^city/(?P<id>\d+)$', views.city, name='city_id'),

    # Login routes
    url(r'^login$', views.login, name='login'),

    url(r'^', schema_view, name="docs")

]
