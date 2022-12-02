from django.contrib import admin
from django.contrib import messages
from osoby import models
from osoby.forms import KlasaForm
import csv

admin.site.register(models.Klasa)
admin.site.register(models.Absolwent)

@admin.register(models.Dokument)
class DokumentAdmin(admin.ModelAdmin):
    fields = ('opis', 'plik', 'typ')

    def dodaj_klasy(self, request, dane):
        for klasa in dane:
            form = KlasaForm(data=klasa)
            if form.is_valid():
                messages.success(request, 'Dodano klasę: {} ({})'.format(klasa['nazwa'], klasa['rok_naboru']))
                form.save()
            else:
                bledy = form.non_field_errors().as_text()
                for pole, blad in form.errors.items():
                    if pole != '__all__':
                        bledy += 'Pole: {}, błąd: {}.'.format(pole, blad)
                messages.error(request, 'Nie dodano klasy: {} ({}). Błędy: {}'
                               .format(klasa['nazwa'], klasa['rok_naboru'], bledy))

    def dodaj_absolwentow(self, request, dane):
        pass

    def save_model(self, request, obj, form, change):
        csvfile = request.FILES['plik'].read().decode('utf-8').splitlines()
        nazwy_pol = ('nazwa', 'rok_matury', 'rok_naboru')
        dane = csv.DictReader(csvfile, fieldnames=nazwy_pol)
        if obj.typ == 'K':
            self.dodaj_klasy(request, dane)
        else:
            self.dodaj_absolwentow(request, dane)
        obj.save()