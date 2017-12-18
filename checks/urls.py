from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^(?P<cod_prep>[0-9]+)/$', views.controlloPlanning, name='controlloPlanning'),
    url(r'^segnalazione/(?P<n_matricola>[0-9]+)/$', views.ricezione, name='ricezione'),
    url(r'^planning/(?P<planningId>[0-9]+)/daydone/$', views.daydone, name='daydone'),

]
