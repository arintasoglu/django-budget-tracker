from sqlite3 import IntegrityError
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.db.models.deletion import ProtectedError


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


def buchung(request):
    buchungen = Buchung.objects.filter(
        benutzer=User.objects.get(username=request.user.get_username())
    )
    return render(request, "buchung.html", {"buchungen": buchungen})


def buchung_hinzufuegen(request):
    form = BuchungsForm(request.POST or None)
    kategorien = Kategorie.objects.all()

    if form.is_valid():
        buchung = form.save(commit=False)
        buchung.benutzer = request.user
        kategorie_id = request.POST.get("kategorie")
        buchung.kategorie = get_object_or_404(Kategorie, kategorieId=kategorie_id)
        buchung.save()
        return redirect("buchung")

    return render(
        request, "buchung_hinzufuegen.html", {"form": form, "kategorien": kategorien}
    )


def buchung_loeschen(request, id):
    buchung = Buchung.objects.get(buchungId=id)
    buchung.delete()
    return redirect("buchung")


def buchung_bearbeiten(request, id):
    buchung = Buchung.objects.get(buchungId=id)
    kategorie = Kategorie.objects.filter(name=buchung.kategorie).first()
    form = BuchungsForm(request.POST or None, instance=buchung)
    if form.is_valid():
        a = form.save(commit=False)
        a.benutzer = request.user
        kategorie_id = request.POST.get("kategorie")
        a.kategorie = get_object_or_404(Kategorie, kategorieId=kategorie_id)
        a.save()
        return redirect("buchung")

    return render(
        request,
        "buchung_bearbeiten.html",
        {"form": form, "buchung": buchung, "kategorie": kategorie},
    )


def kategorie(request):
    kategorien = Kategorie.objects.filter(
        benutzer=User.objects.get(username=request.user.get_username())
    )
    return render(request, "kategorie.html", {"kategorien": kategorien})


def kategorie_hinzufuegen(request):
    form = KategorieForm(request.POST or None, initial={"benutzer": request.user})
    if form.is_valid():
        kategorie = form.save(commit=False)
        kategorie.benutzer = request.user
        kategorie.save()
        return redirect("kategorie")

    return render(request, "kategorie_hinzufuegen.html", {"form": form})


def kategorie_loeschen(request, id):
    kategorie = Kategorie.objects.get(kategorieId=id)
    try:
        kategorie.delete()
        messages.success(request, "Kategorie wurde gelöscht.")
    except ProtectedError:
        messages.error(
            request,
            "Diese Kategorie kann nicht gelöscht werden, "
            "da noch Buchungen vorhanden sind."
        )

    return redirect("kategorie")
