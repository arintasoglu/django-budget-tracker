from django.test import TestCase
from django.contrib.auth.models import User
from finance.models import Buchung, Kategorie
from django.urls import reverse
from decimal import Decimal


class TestViews(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="viewtestuser1", password="12345"
        )
        self.user2 = User.objects.create_user(
            username="viewtestuser2", password="12345"
        )

        self.kategorie1 = Kategorie.objects.create(name="Freizeit", benutzer=self.user1)
        self.kategorie2 = Kategorie.objects.create(name="Reisen", benutzer=self.user2)

        self.buchung1 = Buchung.objects.create(
            type="expense",
            beschreibung="Kinoabend",
            betrag=30.00,
            datum="2026-01-17",
            kategorie=self.kategorie1,
            benutzer=self.user1,
        )

        self.buchung2 = Buchung.objects.create(
            type="expense",
            beschreibung="Flugticket",
            betrag=500.00,
            datum="2026-01-18",
            kategorie=self.kategorie2,
            benutzer=self.user2,
        )

    def test_booking_list_requires_login(self):
        response = self.client.get(reverse("buchung"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_view_returns_200_for_logged_in_user(self):
        self.client.login(username="viewtestuser1", password="12345")
        response = self.client.get(reverse("übersicht"))
        self.assertEqual(response.status_code, 200)

    def test_user_sees_own_bookings_only(self):
        self.client.login(username="viewtestuser1", password="12345")
        response = self.client.get(reverse("buchung"))
        self.assertContains(response, "Kinoabend")
        self.assertNotContains(response, "Flugticket")

    def test_user_cannot_delete_other_users_bookings(self):
        self.client.login(username="viewtestuser1", password="12345")
        response = self.client.post(
            reverse("buchung_loeschen", args=[self.buchung2.buchungId])
        )
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            Buchung.objects.filter(buchungId=self.buchung2.buchungId).exists()
        )

    def test_create_booking_creates_new_record(self):
        self.client.login(username="viewtestuser1", password="12345")
        data = {
            "type": "income",
            "beschreibung": "Gehalt",
            "betrag": 2000.00,
            "datum": "2026-01-20",
            "kategorie": self.kategorie1.kategorieId,
        }
        response = self.client.post(reverse("buchung_hinzufuegen"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Buchung.objects.filter(benutzer=self.user1, beschreibung="Gehalt").count(),
            1,
        )

    def test_update_booking_updates_existing_record(self):
        self.client.login(username="viewtestuser1", password="12345")
        data = {
            "type": "expense",
            "beschreibung": "Kinoabend aktualisiert",
            "betrag": 35.00,
            "datum": "2026-01-17",
            "kategorie": self.kategorie1.kategorieId,
        }
        response = self.client.post(
            reverse("buchung_bearbeiten", args=[self.buchung1.buchungId]), data
        )
        self.buchung1.refresh_from_db()
        self.assertEqual(self.buchung1.beschreibung, "Kinoabend aktualisiert")
        self.assertEqual(self.buchung1.betrag, Decimal("35.00"))

    def test_create_category_creates_new_category(self):
        self.client.login(username="viewtestuser1", password="12345")
        data = {
            "name": "Essen",
        }
        response = self.client.post(reverse("kategorie_hinzufuegen"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Kategorie.objects.filter(benutzer=self.user1, name="Essen").exists()
        )

    def test_category_with_bookings_cannot_be_deleted(self):
        self.client.login(username="viewtestuser1", password="12345")
        response = self.client.post(
            reverse("kategorie_loeschen", args=[self.kategorie1.kategorieId])
        )
        self.assertTrue(
            Kategorie.objects.filter(kategorieId=self.kategorie1.kategorieId).exists()
        )

    def test_export_contains_only_user_bookings(self):
        self.client.login(username="viewtestuser1", password="12345")
        response = self.client.get(reverse("export_buchungen"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("Kinoabend", content)
        self.assertNotIn("Flugticket", content)

    def test_charts_view_loads_successfully(self):
        self.client.login(username="viewtestuser1", password="12345")
        response = self.client.get(reverse("diagramme"))
        self.assertEqual(response.status_code, 200)
