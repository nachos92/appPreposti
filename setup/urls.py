from django.conf.urls import include, url
from django.contrib import admin
from . import views



urlpatterns = [
    url(r'^start/$', views.start, name='start'),
    url(r'^impostazioni/$', views.impostazioni, name='impostazioni'),
    url(r'^dipendenti/upload/$', views.uploadDip, name='uploadDip'),
    url(r'^preposti/upload/$', views.uploadPrep, name='uploadPrep'),
    url(r'^responsabili/upload/$', views.uploadResp, name='uploadResp'),
    url(r'^dipendenti/prova/$', views.dipProva, name='dipProva'),
]
