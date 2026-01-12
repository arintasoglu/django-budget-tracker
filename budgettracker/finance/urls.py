from django.contrib import admin
from django.urls import include, path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.anmelden, name="anmelden"),
    path("registrieren/", views.registrieren, name="registrieren"),
    path("abmelden/", views.abmelden, name="abmelden"),
    path("navbar/", views.navbar, name="navbar"),
    path("meineBuchungen/", views.buchung, name="buchung"),
    path("buchung/loeschen/<int:id>/", views.buchung_loeschen, name="buchung_loeschen"),
    path(
        "buchung/bearbeiten/<int:id>/",
        views.buchung_bearbeiten,
        name="buchung_bearbeiten",
    ),
    path("buchung_hinzufuegen/", views.buchung_hinzufuegen, name="buchung_hinzufuegen"),
    path("meineKategorien/", views.kategorie, name="kategorie"),
    path(
        "kategorie/loeschen/<int:id>/",
        views.kategorie_loeschen,
        name="kategorie_loeschen",
    ),
    path(
        "kategorie_hinzufuegen/",
        views.kategorie_hinzufuegen,
        name="kategorie_hinzufuegen",
    ),
    path(
        "meineBuchungen/export_buchungen/",
        views.export_buchungen,
        name="export_buchungen",
    ),
    path("diagramme/", views.diagramme, name="diagramme"),
    path(
        "passwort_zuruecksetzen/",
        auth_views.PasswordResetView.as_view(
            template_name="passwort_zuruecksetzen.html",
            email_template_name="passwort_zuruecksetzen_email.html",
        ),
        name="passwort_zuruecksetzen",
    ),
    path(
        "passwort_zuruecksetzen/erfolg/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="passwort_zuruecksetzen_erfolg.html"
        ),
        name="password_reset_done",
    ),
    path(
        "passwort_zuruecksetzen/bestaetigen/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="passwort_zuruecksetzen_bestaetigen.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "passwort_zuruecksetzen/abgeschlossen/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="passwort_zuruecksetzen_abgeschlossen.html"
        ),
        name="password_reset_complete",
    ),
]
