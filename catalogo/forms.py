from django import forms
from .models import Risorsa

class RisorsaForm(forms.ModelForm):
    class Meta:
        model = Risorsa
        fields = ['titolo', 'descrizione', 'prezzo', 'disponibile']
