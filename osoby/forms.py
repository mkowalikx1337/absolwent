from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from osoby.models import Klasa, Absolwent, Dokument

from django.forms import ModelChoiceField

class UserLoginForm(forms.Form):
    nazwa = forms.CharField(label="Twój login", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    haslo = forms.CharField(label="Hasło", required=True, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}))


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'required': 'required', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class AbsolwentForm(forms.ModelForm):
    user = UserChoiceField(
        queryset=User.objects.all(),
        label='Osoba',
        disabled=True
    )
    class Meta:
        model = Absolwent
        fields = ('user', 'klasa')


class UserEditForm(forms.ModelForm):
    klasa = forms.ModelChoiceField(
        queryset=Klasa.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control w-25'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'required': 'required', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'required': 'required', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'required': 'required', 'class': 'form-control'}),
        }


class KlasaForm(forms.ModelForm):
    class Meta:
        model = Klasa
        exclude = ('data_d',)


class DokumentForm(forms.ModelForm):
    class Meta:
        model = Dokument
        fields = ('opis', 'plik')



class UserCreateForm2(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserLoginForm2(forms.Form):
    nazwa = forms.CharField(label="Twój login", max_length=50, help_text='Wpisz login.')
    haslo = forms.CharField(label="Hasło", required=True, widget=forms.PasswordInput, help_text='Podaj hasło.')


class UserEditForm2(forms.ModelForm):
    klasa = forms.ModelChoiceField(
        queryset=Klasa.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserForm(forms.Form):
    nazwa = forms.CharField(label="Twój login", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Adres email", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    haslo = forms.CharField(label="Hasło", widget=forms.TextInput(attrs={'type': 'password', 'required': True, 'class': 'form-control'}))
