from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^(?P<cod_prep>[0-9]+)/$', views.controlloPlanning, name='controlloPlanning'),
    url(r'^segnalazione/(?P<n_matricola>[0-9]+)/$', views.ricezione, name='ricezione'),
    url(r'^planning/daydone/$', views.daydone, name='daydone'),

    #Puo' servire
    url(r'^planning/(?P<id>[0-9]+)/$', views.orarioPlanning, name='orarioPlanning'),
    url(
        r'^(?P<n_matricola>[0-9]+)/planning/(?P<id_sett>[0-9]+)/done/$',
        views.fineGiro,
        name='fineGiro'
        ),


]
