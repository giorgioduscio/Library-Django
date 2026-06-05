from django import forms
from .models import Risorsa, Utente

class RisorsaForm(forms.ModelForm):
    class Meta:
        model = Risorsa
        fields = ['titolo', 'descrizione', 'prezzo', 'disponibile']

class UtenteForm(forms.ModelForm):
    class Meta:
        model = Utente
        fields = ['nome', 'cognome', 'email', 'eta', 'attivo', 'libri_prestito']
