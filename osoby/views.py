from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Witaj w Django!</h1>")

def info(request):
    return HttpResponse("<p>Cześć! Tworzymy aplikacje!</p>")
