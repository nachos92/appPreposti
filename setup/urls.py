from django.conf.urls import include, url
from django.contrib import admin
from . import views



urlpatterns = [
    url(r'^start/$', views.start, name='start'),
    url(r'^dipendenti/upload/$', views.uploadDip, name='uploadDip'),

]
