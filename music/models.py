from django.db import models
from django.utils import timezone

class Genere(models.Model):
    """Modello della tabella dei generi"""
    titolo =models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.id}) {self.titolo}"
    class Meta:
        ordering=["titolo"]
        verbose_name='Genere'
        verbose_name_plural='Generi'

class Tag(models.Model):
    titolo =models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.id}) {self.titolo}"
    class Meta:
        ordering=["titolo"]


class Artista(models.Model):
    """Modello della tabella degli artisti"""
    nome         =models.CharField(max_length=150, unique=True)
    nazionalita  =models.CharField(max_length=150, null=True, blank=True)
    biografia    =models.TextField(null=True, blank=True)
    data_debutto =models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.id}) {self.nome} - {self.data_debutto}"
    class Meta:
        ordering=["nome", "-data_debutto"]
        verbose_name='Artista'
        verbose_name_plural='Artisti'

    
class Album(models.Model):
    """Modello della tabella degli albums"""
    titolo      =models.CharField(max_length=200, unique=True)
    anno        =models.IntegerField()
    genere      =models.ForeignKey('Genere', on_delete=models.PROTECT, related_name="Album")
    artista     =models.ForeignKey('Artista', on_delete=models.PROTECT, related_name="Album")
    disponibile =models.BooleanField( default=True )

    def __str__(self):
        disp = "Disponibile" if(self.disponibile)else "Esaurito"
        return f"{self.id}) {self.titolo} ({self.anno}) {disp}"
    class Meta:
        ordering=["titolo", "-anno"]


class Canzone(models.Model):
    """Modello della tabella delle canzoni"""
    titolo  =models.CharField(max_length=200)
    durata_secondi =models.IntegerField()
    traccia =models.IntegerField()
    album   =models.ForeignKey('Album', on_delete=models.CASCADE, related_name="Canzone")
    tags    =models.ManyToManyField("Tag", related_name="canzoni", blank=True)

    def __str__(self):
        return f"{self.id}) {self.titolo} ({self.durata_secondi}s)"
    class Meta:
        ordering=["traccia", "titolo"]
        verbose_name='Canzone'
        verbose_name_plural='Canzoni'
