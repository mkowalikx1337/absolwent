from django.urls import path
from django.views.generic import ListView
from wiadomosci.models import Wiadomosc

from . import views

app_name = 'wiadomosci'
urlpatterns = [

    path('', views.ListaWiadomosci.as_view(), name='lista'),
    path('dodaj/', views.DodajWiadomosc.as_view(), name='dodaj'),
    path('edytuj/<int:pk>', views.EdytujWiadomosc.as_view(), name='edytuj'),
    path('usun/<int:pk>', views.UsunWiadomosc.as_view(), name='usun'),
]