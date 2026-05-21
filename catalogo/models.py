from django.db import models

class Risorsa(models.Model):
    titolo      = models.CharField(max_length=255)
    descrizione = models.TextField()
    prezzo      = models.FloatField()
    disponibile = models.BooleanField(default=True)
    creato_il   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        disponibile = "Disponibile" if(self.disponibile) else "Non disponibile"
        return f"{self.id}) {self.titolo}: {self.prezzo}€ {disponibile}"
    class Meta:
        ordering = ['titolo']

class Utente(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    eta = models.IntegerField()
    # libri_prestito =models.ar

    def __str__(self):
        return f"{self.nome} {self.cognome} ({self.email}) {self.eta} anni"
