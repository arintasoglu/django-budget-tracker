from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.anmelden, name="anmelden"),
    path('registrieren/', views.registrieren, name="registrieren"),
    path('abmelden/', views.abmelden, name="abmelden"),
    path('navbar/', views.navbar, name="navbar"),

]
