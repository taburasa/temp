from django.conf.urls import url
from . import views

app_name = 'travel_buddy'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add$', views.add, name='add'),
    url(r'^create$', views.create, name='create'),
    url(r'^destination/(?P<trip_id>[0-9]+)$', views.trip, name='trip'),
    url(r'^join/(?P<trip_id>[0-9]+)$', views.join, name='join'),
]
