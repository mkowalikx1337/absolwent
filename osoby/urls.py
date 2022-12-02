from django.urls import path
from . import views
from django.views.generic import ListView
from osoby.models import Absolwent


app_name = 'osoby'
urlpatterns = [
    path('', ListView.as_view(
        model=Absolwent,
        context_object_name='osoby',
        template_name='osoby/lista_osob2.html'
    ), name='lista'),
    path('loguj/', views.loguj_osobe, name='loguj-osobe'),
    path('wyloguj/', views.wyloguj_osobe, name='wyloguj-osobe'),
    path('rejestruj/', views.rejestruj_osobe, name='rejestruj-osobe'),
    path('edytuj/', views.edytuj_osobe, name='edytuj-osobe'),

    path('plik/', views.upload_dokument, name='dokument'),
    path('absolwent/edytuj/<int:pk>', views.EdytujAbsolwent.as_view(), name='edytuj-absolwent'),
    path('absolwent/usun/<int:pk>', views.UsunAbsolwent.as_view(), name='usun-absolwent'),
    path('profil/', views.EditUser, name='profil-osobe'),
    path('haslo-zmien/', views.zmien_haslo, name ='haslo-zmien'),
]
