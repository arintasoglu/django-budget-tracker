from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.forms import AuthenticationForm


## View for rendering the navbar
## dummy
def navbar(request):
    return render(request, "navbar.html")


def anmelden(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        benutzername = form.cleaned_data.get("username")
        passwort = form.cleaned_data.get("password")
        benutzer = authenticate(request, username=benutzername, password=passwort)
        if benutzer is not None:
            login(request, benutzer)
            return redirect("navbar")
    return render(request, "anmelden.html", {"form": form})



def registrieren(request):
    form = RegisterModelForm(request.POST or None)
    if form.is_valid():
        benutzer = form.save()
        messages.success(
            request, "Registrierung erfolgreich. Sie können sich jetzt anmelden."
        )
        login(request, benutzer)
        return redirect("navbar")
    return render(request, "registrieren.html", {"form": form})


def abmelden(request):
    logout(request)
    return redirect("anmelden")
