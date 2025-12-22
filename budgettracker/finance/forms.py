from django import forms
from django.contrib.auth.models import User

from .models import Buchung


class RegisterModelForm(forms.ModelForm):
    passwort = forms.CharField(widget=forms.PasswordInput)
    confirm_passwort = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            self.add_error("email", "Diese E-Mail-Adresse wird bereits verwendet.")
        return email

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("passwort")
        pw2 = cleaned.get("confirm_passwort")
        if pw and pw2 and pw != pw2:
            self.add_error("confirm_passwort", "Passwörter stimmen nicht überein.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["passwort"])
        if commit:
            user.save()
        return user


class BuchungsForm(forms.ModelForm):
    class Meta:
        model = Buchung
        fields = ["type", "kategorie", "beschreibung", "betrag", "datum"]

    def clean_beschreibung(self):
        beschreibung = self.cleaned_data.get("beschreibung")
        if len(beschreibung or "") > 200:
            self.add_error(
                "beschreibung", "Beschreibung darf maximal 200 Zeichen lang sein."
            )
        return beschreibung


"""class BuchungsForm(forms.Form):
    type = forms.CharField(max_length=10)
    kategorie = forms.CharField(max_length=100)
    beschreibung = forms.CharField(required=False)
    betrag = forms.DecimalField(max_digits=10, decimal_places=2)
    datum = forms.DateField()




    def clean_beschreibung(self):
        beschreibung = self.cleaned_data.get("beschreibung")
        if len(beschreibung or "") > 200:
            self.add_error(
                "beschreibung", "Beschreibung darf maximal 200 Zeichen lang sein."
            )
        return beschreibung
        """
