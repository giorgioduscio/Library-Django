from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.id} ({self.nome})"

class Prodotto(models.Model):
    nome = models.CharField(max_length=100)
    descrizione = models.TextField()
    prezzo = models.FloatField()
    quantita = models.IntegerField(default=1)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id} ({self.nome}, {self.prezzo}€)"

class Ordine(models.Model):
    utente_nome = models.CharField(max_length=100)
    data_ordine = models.DateTimeField(auto_now_add=True)
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id} ({self.utente_nome}, {self.data_ordine})"

"""
Categoria
    Categoria.objects.create( nome="Elettronica" )
    Categoria.objects.create( nome="Abbigliamento" )
    Categoria.objects.create( nome="Libri" )

prodotti
    Prodotto.objects.create(
        nome="Telefono",
        descrizione="Telefono smartphone",
        prezzo=500.0,
        quantita=10,
        categoria=Categoria.objects.get(nome="Elettronica")
    );
    Prodotto.objects.create(
        nome="Maglietta",
        descrizione="Maglietta di cotone",
        prezzo=20.0,
        quantita=50,
        categoria=Categoria.objects.get(nome="Abbigliamento")
    );
    Prodotto.objects.create(
        nome="Canottiera",
        descrizione="Canottiera di plastica",
        prezzo=10.0,
        quantita=100,
        categoria=Categoria.objects.get(nome="Abbigliamento")
    );
    Prodotto.objects.create(
        nome="L'ascesa di Scaktarx",
        descrizione="Libro di fantascienza",
        prezzo=20.0,
        quantita=50,
        categoria=Categoria.objects.get(nome="Libri")
    );
    Prodotto.objects.create(
        nome="Babbo Babbone",
        descrizione="Gioco da tavolo",
        prezzo=10.0,
        quantita=100,
        categoria=Categoria.objects.get(nome="Libri")
    );

ordini
    Ordine.objects.create(
        utente_nome ="Maurizio",
        prodotto =Prodotto.objects.get(id=1)
    );
    Ordine.objects.create(
        utente_nome ="Mario",
        prodotto =Prodotto.objects.get(id=2)
    );
    Ordine.objects.create(
        utente_nome ="Federica",
        prodotto =Prodotto.objects.get(id=3)
    );
    Ordine.objects.create(
        utente_nome ="Zalib",
        prodotto =Prodotto.objects.get(id=3)
    );
    Ordine.objects.create(
        utente_nome ="Carlo",
        prodotto =Prodotto.objects.get(id=4)
    );
    Ordine.objects.create(
        utente_nome ="Lola",
        prodotto =Prodotto.objects.get(id=5)
    );

ESERCIZI
1) Prodotto.objects.filter(prezzo__gte=10)
   .filter(prezzo__lte=100)
   .order_by("prezzo")

2) Prodotto.objects.select_related("categoria")
   .filter(quantita__gt=0)
   .exclude(prezzo__gt=500)

3) Ordine.objects.filter(prodotto=Prodotto.objects.get(id=3))
   .count()

4) from django.db.models import Avg, Max, Min;
   Prodotto.objects 
   .aggregate(massimo =Max("prezzo"),
              minimo =Min("prezzo"),
              media =Avg("prezzo"))
   .filter(quantita__gt=0)

5) Prodotto.objects.all().order_by("-prezzo")[:5]
"""

class Localita(models.Model):
    nome =models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id} ({self.nome})"

class Evento(models.Model):
    titolo =models.CharField(max_length=50)
    localita =models.ManyToManyField("Localita")

    def __str__(self):
        return f"{self.id} ({self.titolo})"

"""
Localita.objects.create( nome="Roma" );
Localita.objects.create( nome="Milano" )


conc = Evento.objects.create(
    titolo="Concerto"
); 
for loc in Localita.objects.all():
  conc.localita.add(loc);

expo = Evento.objects.create(
    titolo="Expo",
    localita=[Localita.objects.get(id=1)]
)

"""