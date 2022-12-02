from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class Klasa(models.Model):
    nazwa = models.CharField("nazwa klasy", max_length=3, default="")
    rok_matury = models.IntegerField("rok matury", default=0)
    rok_naboru = models.IntegerField("rok naboru", default=0)
    data_d = models.DateTimeField("dodana", default=timezone.now)

    class Meta:
        verbose_name_plural = 'klasy'
        ordering = ['rok_matury']
        unique_together = ("nazwa", "rok_naboru")

    def __str__(self):
        return self.nazwa + " " + str(self.rok_matury)


class Absolwent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    klasa = models.ForeignKey(Klasa, on_delete=models.SET_NULL, blank=True, null=True, related_name="uczniowie")

    class Meta:
        verbose_name_plural = 'absolwenci'

    def __str__(self):
        return self.user.get_full_name()


def rozmiar_pliku(value):
    limit = 1024 * 1024
    if value.size > limit:
        raise ValidationError('Za duży plik. Maksymalny rozmiar to 1 MB.')


class Dokument(models.Model):
    opis = models.CharField(max_length=255, unique=True)
    plik = models.FileField(upload_to='dokumenty/', validators=[rozmiar_pliku])
    data_d = models.DateTimeField("dodano", auto_now_add=True)
    TYPY = (('K', 'Lista klas'), ('U', 'Lista uczniów'))
    typ = models.CharField(max_length=1, choices=TYPY, default='K')

    class Meta:
        verbose_name_plural = 'dokumenty'

    def delete(self, *args, **kwargs):
        storage, path = self.plik.storage, self.plik.path
        super(Dokument, self).delete(*args, **kwargs)
        storage.delete(path)

    def __str__(self):
        return self.opis
