from django.db import models
from django.contrib.auth.models import User

class Risorsa(models.Model):
    titolo      = models.CharField(max_length=100)
    descrizione = models.TextField()
    prezzo      = models.FloatField()
    disponibile = models.BooleanField(default=True)
    creato_il   = models.DateTimeField(auto_now_add=True)
    utenti_prestito = models.ManyToManyField(User, related_name='libri_prestito', blank=True)

    def __str__(self):
        disponibile = "Disponibile" if(self.disponibile) else "Non disponibile"
        return f"{self.id}) {self.titolo}: {self.prezzo}€ {disponibile}"
    class Meta:
        ordering = ['titolo']
