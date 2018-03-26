from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^(?P<matricola>[0-9]+)/$', views.controlloPlanning, name='controlloPlanning'),
    #url(r'^segnalazione/(?P<matricola>[0-9]+)/$', views.ricezione, name='ricezione'),
    url(r'^dipendente/(?P<matricola>[0-9]+)/done/$', views.visitato, name='visitato'),
    url(r'^planning/(?P<id>[0-9]+)/$', views.orarioPlanning, name='orarioPlanning'),
    url(
        r'^(?P<matricola>[0-9]+)/planning/(?P<id>[0-9]+)/done/$',
        views.fineGiro,
        name='fineGiro'
        ),


]
