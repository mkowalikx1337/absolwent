from django.shortcuts import render
# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from osoby.models import Absolwent
from osoby.forms import UserLoginForm2, DokumentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from osoby.forms import UserCreateForm2, UserEditForm2
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from osoby.forms import AbsolwentForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm


def index(request):
    return render(request, 'osoby/index.html')


def lista_osob(request):
    osoby = Absolwent.objects.all()
    kontekst = {'osoby': osoby}
    return render(request, 'osoby/lista_osob2.html', kontekst)


def loguj_osobe(request):
    if request.method == 'POST':
        form = UserLoginForm2(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            nazwa = form.cleaned_data['nazwa']
            haslo = form.cleaned_data['haslo']
            user = authenticate(request, username=nazwa, password=haslo)
            if user is not None:
                login(request, user)
                messages.success(request, "Zostałeś zalogowany!")
                return redirect(reverse('osoby:lista'))
            else:
                messages.error(request, "Błędny login lub hasło!")
    else:
        form = UserLoginForm2()
    kontekst = {'form': form}
    return render(request, 'osoby/loguj_osobe2.html', kontekst)


def wyloguj_osobe(request):
    logout(request)
    messages.info(request, "Zostałeś wylogowany!")
    return redirect(reverse('osoby:lista'))


def rejestruj_osobe(request):
    if request.method == 'POST':
        form = UserCreateForm2(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Utworzono konto! Możesz się zalogować!")
            return redirect(reverse('osoby:loguj-osobe'))
    else:
        form = UserCreateForm2()
    return render(request, 'osoby/rejestruj_osobe1.html', {'form': form})


@login_required()
def edytuj_osobe(request):
    try:
        a = Absolwent.objects.filter(user=request.user).first()
    except Absolwent.DoesNotExist:
        a = 0
    print(a)
    if request.method == 'POST':
        form = UserEditForm2(instance=request.user, data=request.POST)
        if form.is_valid():
            print(form.cleaned_data['klasa'])
            if a:
                a.klasa = form.cleaned_data['klasa']
                a.save()
            else:
                a = Absolwent.objects.create(user=request.user, klasa=form.cleaned_data['klasa'])
            form.save()
            messages.success(request, "Zaktualizowano dane użytkownika!")
            return redirect(reverse('osoby:lista'))
    else:
        if a:
            a = a.klasa.id
        form = UserEditForm2(instance=request.user, initial={'klasa':a})
    return render(request, 'osoby/edytuj_osobe1.html', {'form': form})


def upload_dokument(request):
    if request.method == 'POST':
        form = DokumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DokumentForm()
    return render(request, 'osoby/upload_dokument_form.html', {'form': form})


def EditUser(request):
    user = request.user
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Dane zaktualizowano.')
            return redirect(reverse('osoby:lista'))
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'osoby/edytuj_osobe1.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EdytujAbsolwent(SuccessMessageMixin, UpdateView):
    model = Absolwent
    form_class = AbsolwentForm
    context_object_name = 'absolwent'
    template_name = 'osoby/edytuj_absolwent1.html'
    success_url = '/osoby/'
    success_message = 'Absolwenta przypisano do klasy!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['absolwenci'] = Absolwent.objects.all()
        return context


@method_decorator(login_required, name='dispatch')
class UsunAbsolwent(DeleteView):
    model = Absolwent
    context_object_name = 'absolwent'
    template_name = 'osoby/usun_absolwent1.html'
    success_url = '/osoby/'
    success_message = 'Absolwenta usunięto!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['absolwenci'] = Absolwent.objects.all()
        return context


@login_required()
def zmien_haslo(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Twoje hasło zostało zmienione!')
            return redirect(reverse('osoby:lista'))
        else:
            messages.error(request, 'Popraw poniższe błędy.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'osoby/haslo_zmien.html', {'form': form})