from django import forms
from django.contrib.auth.models import User

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
