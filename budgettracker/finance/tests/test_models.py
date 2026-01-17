from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth.models import User
from finance.models import Buchung, Kategorie
from datetime import date
from django.db.models import ProtectedError


class BuchungModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.kategorie = Kategorie.objects.create(
            name="Lebensmittel", benutzer=self.user
        )
        self.buchung = Buchung.objects.create(
            type="expense",
            beschreibung="Wocheneinkauf",
            betrag=75.50,
            datum=date(2026, 1, 16),
            kategorie=self.kategorie,
            benutzer=self.user,
        )

    def test_buchung_creation(self):
        self.assertEqual(self.buchung.beschreibung, "Wocheneinkauf")
        self.assertEqual(self.buchung.betrag, 75.50)
        self.assertEqual(self.buchung.datum, date(2026, 1, 16))
        self.assertEqual(self.buchung.kategorie.name, "Lebensmittel")
        self.assertEqual(self.buchung.benutzer.username, "testuser")

    def test_buchung_str_method(self):
        expected_str = "Wocheneinkauf - 75.50 am 2026-01-16"
        self.assertEqual(str(self.buchung), expected_str)

    def test_category_delete_is_protected_when_bookings_exist(self):
        with self.assertRaises(ProtectedError):
            self.kategorie.delete()


class KategorieModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="testuser2", password="12345")
        self.user2 = User.objects.create_user(username="testuser3", password="12345")
        self.kategorie = Kategorie.objects.create(name="Transport", benutzer=self.user1)

    def test_category_creation(self):
        self.assertEqual(self.kategorie.name, "Transport")
        self.assertEqual(self.kategorie.benutzer.username, "testuser2")

    def test_category_str_method(self):
        self.assertEqual(str(self.kategorie), "Transport")

    def test_category_name_unique_per_user(self):
        Kategorie.objects.create(name="Essen", benutzer=self.user1)

        with self.assertRaises(IntegrityError):
            Kategorie.objects.create(name="Essen", benutzer=self.user1)

    def test_category_name_can_repeat_for_different_users(self):
        Kategorie.objects.create(name="Essen", benutzer=self.user1)
        Kategorie.objects.create(name="Essen", benutzer=self.user2)

        self.assertEqual(Kategorie.objects.filter(name="Essen").count(), 2)
