from django import forms
from django.contrib.auth.models import User
from .models import Risorsa

class RisorsaForm(forms.ModelForm):
    class Meta:
        model = Risorsa
        fields = ['titolo', 'autore_nome', 'descrizione', 'prezzo', 'disponibile', 'utente']

class UtenteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
