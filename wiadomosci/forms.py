from django import forms
from wiadomosci.models import Wiadomosc


class WiadomoscForm(forms.ModelForm):
    class Meta:
        model = Wiadomosc
        fields = ('tresc', 'data_d')
        widgets = {
            'tresc': forms.Textarea(attrs={'cols': 100, 'rows': 2, 'class': 'form-control'}),
            'data_d': forms.DateTimeInput(),
        }