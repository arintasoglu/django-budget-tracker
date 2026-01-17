from sqlite3 import IntegrityError
from urllib import request
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.db.models.deletion import ProtectedError
from .resources import BuchungResource
from .chart import (
    generate_expense_income_chart,
    generate_pie_income_chart,
    generate_pie_expense_chart,
)
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


@login_required(login_url="anmelden")
def übersicht(request):
    total_income = (
        Buchung.objects.filter(
            benutzer=User.objects.get(username=request.user.get_username()),
            type="income",
        ).aggregate(total_amount=models.Sum("betrag"))["total_amount"]
        or 0
    )
    total_expense = (
        Buchung.objects.filter(
            benutzer=User.objects.get(username=request.user.get_username()),
            type="expense",
        ).aggregate(total_amount=models.Sum("betrag"))["total_amount"]
        or 0
    )

    recent_buchungen = Buchung.objects.filter(
        benutzer=User.objects.get(username=request.user.get_username())
    ).order_by("-datum")[:5]

    return render(
        request,
        "dashboard.html",
        {
            "total_income": total_income,
            "total_expense": total_expense,
            "recent_buchungen": recent_buchungen,
        },
    )


def anmelden(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        benutzername = form.cleaned_data.get("username")
        passwort = form.cleaned_data.get("password")
        benutzer = authenticate(request, username=benutzername, password=passwort)
        if benutzer is not None:
            login(request, benutzer)
            return redirect("übersicht")
    return render(request, "anmelden.html", {"form": form})


def registrieren(request):
    form = RegisterModelForm(request.POST or None)
    if form.is_valid():
        benutzer = form.save()
        messages.success(
            request, "Registrierung erfolgreich. Sie können sich jetzt anmelden."
        )
        login(request, benutzer)
        return redirect("übersicht")
    return render(request, "registrieren.html", {"form": form})


@login_required(login_url="anmelden")
def abmelden(request):
    logout(request)
    return redirect("anmelden")


@login_required(login_url="anmelden")
def buchung(request):
    buchungen = Buchung.objects.filter(
        benutzer=User.objects.get(username=request.user.get_username())
    )
    kategorien = Kategorie.objects.filter(
        benutzer=User.objects.get(username=request.user.get_username())
    )
    kategorie_filter = request.GET.getlist("kategorieFilter")
    type_filter = request.GET.getlist("typeFilter")
    date_from = request.GET.get("dateFrom")
    date_to = request.GET.get("dateTo")
    if date_from:
        buchungen = buchungen.filter(datum__gte=date_from)
    if date_to:
        buchungen = buchungen.filter(datum__lte=date_to)
    if type_filter:
        buchungen = buchungen.filter(type__in=type_filter)
    if kategorie_filter:
        buchungen = buchungen.filter(kategorie_id__in=kategorie_filter)

    buchungen = buchungen.order_by("-datum", "-buchungId")

    params = request.GET.copy()
    params.pop("page", None)
    extra_qs = ""
    if params:
        extra_qs = "&" + params.urlencode()

    paginator = Paginator(buchungen, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "buchung.html",
        {
            "page_obj": page_obj,
            "kategorien": kategorien,
            "extra_qs": extra_qs,
        },
    )


@login_required(login_url="anmelden")
def buchung_hinzufuegen(request):
    form = BuchungsForm(request.POST or None)
    kategorien = Kategorie.objects.filter(
        benutzer=User.objects.get(username=request.user.get_username())
    )

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


@login_required(login_url="anmelden")
def buchung_loeschen(request, id):
    buchung = get_object_or_404(Buchung, buchungId=id, benutzer=request.user)
    buchung.delete()
    return redirect("buchung")


@login_required(login_url="anmelden")
def buchung_bearbeiten(request, id):
    buchung = get_object_or_404(Buchung, buchungId=id, benutzer=request.user)
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


@login_required(login_url="anmelden")
def kategorie(request):
    kategorien = Kategorie.objects.filter(
        benutzer=User.objects.get(username=request.user.get_username())
    )
    paginator = Paginator(kategorien, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "kategorie.html", {"page_obj": page_obj})


@login_required(login_url="anmelden")
def kategorie_hinzufuegen(request):
    form = KategorieForm(request.POST or None, initial={"benutzer": request.user})
    if form.is_valid():
        kategorie = form.save(commit=False)
        kategorie.benutzer = request.user
        kategorie.save()
        return redirect("kategorie")

    return render(request, "kategorie_hinzufuegen.html", {"form": form})


@login_required(login_url="anmelden")
def kategorie_loeschen(request, id):
    kategorie = get_object_or_404(Kategorie, kategorieId=id, benutzer=request.user)
    try:
        kategorie.delete()
        messages.success(request, "Kategorie wurde gelöscht.")
    except ProtectedError:
        messages.error(
            request,
            "Diese Kategorie kann nicht gelöscht werden, "
            "da noch Buchungen vorhanden sind.",
        )

    return redirect("kategorie")


@login_required(login_url="anmelden")
def export_buchungen(request):
    buchungen = Buchung.objects.filter(
        benutzer=User.objects.get(username=request.user.get_username())
    )
    dataset = BuchungResource().export(buchungen)
    csv_data = dataset.export("csv", delimiter=";")
    response = HttpResponse(csv_data, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="buchungen.csv"'
    return response


@login_required(login_url="anmelden")
def diagramme(request):
    kategorien = Kategorie.objects.filter(
        benutzer=User.objects.get(username=request.user.get_username())
    )
    buchungs_in = Buchung.objects.filter(
        benutzer=User.objects.get(username=request.user.get_username()), type="income"
    )
    buchungs_ex = Buchung.objects.filter(
        benutzer=User.objects.get(username=request.user.get_username()), type="expense"
    )

    sum_expense = sum(b.betrag for b in buchungs_ex)
    sum_income = sum(b.betrag for b in buchungs_in)

    chart = generate_expense_income_chart(sum_expense, sum_income)

    context = {}

    for kategorie in kategorien:

        buchungen_income = Buchung.objects.filter(
            benutzer=User.objects.get(username=request.user.get_username()),
            kategorie=kategorie,
            type="income",
        )
        buchungen_expense = Buchung.objects.filter(
            benutzer=User.objects.get(username=request.user.get_username()),
            kategorie=kategorie,
            type="expense",
        )
        total_income = sum(buchung.betrag for buchung in buchungen_income)
        total_expense = sum(buchung.betrag for buchung in buchungen_expense)
        context[kategorie.name] = {
            "kategorie": kategorie.name,
            "income": total_income,
            "expense": total_expense,
        }
    pie_chart = None
    pie_chart_expense = None
    has_income_data = any(v["income"] > 0 for v in context.values())
    has_expense_data = any(v["expense"] > 0 for v in context.values())

    if has_income_data:
        pie_chart = generate_pie_income_chart(context)
    if has_expense_data:
        pie_chart_expense = generate_pie_expense_chart(context)

    pie_chart_html = pie_chart.to_html() if pie_chart else None
    pie_chart_expense_html = pie_chart_expense.to_html() if pie_chart_expense else None

    return render(
        request,
        "diagramme.html",
        {
            "chart": chart.to_html(),
            "pie_chart": pie_chart_html,
            "pie_chart_expense": pie_chart_expense_html,
        },
    )
