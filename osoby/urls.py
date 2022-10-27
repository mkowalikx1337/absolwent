from django.urls import path

from . import views

app_name = 'osoby'
urlpatterns = [
    path('', views.index, name='lista'),
    path('info/', views.info, name='info'),
    path('loguj/', views.loguj_osobe, name='loguj-osobe'),
    path('wyloguj/', views.wyloguj_osobe, name='wyloguj-osobe'),


]
