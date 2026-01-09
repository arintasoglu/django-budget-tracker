from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    
    path('', views.anmelden, name="anmelden"),
    path('registrieren/', views.registrieren, name="registrieren"),
    path('abmelden/', views.abmelden, name="abmelden"),
    path('navbar/', views.navbar, name="navbar"),
    path('meineBuchungen/', views.buchung, name="buchung"),
    path('buchung/loeschen/<int:id>/', views.buchung_loeschen, name="buchung_loeschen"),
    path('buchung/bearbeiten/<int:id>/', views.buchung_bearbeiten, name="buchung_bearbeiten"),
    path('buchung_hinzufuegen/', views.buchung_hinzufuegen, name="buchung_hinzufuegen"),
    path('meineKategorien/', views.kategorie, name="kategorie"),
    path('kategorie/loeschen/<int:id>/', views.kategorie_loeschen, name="kategorie_loeschen"),
    path('kategorie_hinzufuegen/', views.kategorie_hinzufuegen, name="kategorie_hinzufuegen"),
    path('meineBuchungen/export_buchungen/', views.export_buchungen, name="export_buchungen"),


]
