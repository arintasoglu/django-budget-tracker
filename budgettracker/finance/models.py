from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES = [("income", "Einkommen"), ("expense", "Ausgabe")]


class Buchung(models.Model):
    buchungId = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=STATUS_CHOICES)
    beschreibung = models.CharField(max_length=200, blank=True, null=True)
    betrag = models.DecimalField(max_digits=10, decimal_places=2)
    datum = models.DateField()
    kategorie = models.ForeignKey("Kategorie", on_delete=models.PROTECT)
    benutzer = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Buchungen"

    def __str__(self):
        return f"{self.beschreibung} - {self.betrag} am {self.datum}"


class Kategorie(models.Model):
    kategorieId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    benutzer = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("benutzer", "name")
        verbose_name_plural = "Kategorien"

    def __str__(self):
        return self.name
