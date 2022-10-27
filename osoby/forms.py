from django import forms

class UserLoginForm(forms.Form):
    nazwa = forms.CharField(label="Twój login", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    haslo = forms.CharField(label="Hasło", required=True, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}))
