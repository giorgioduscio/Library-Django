from django.contrib import admin

# Register your models here.
from .models import Categoria, Prodotto, Ordine

admin.site.register(Categoria)
admin.site.register(Prodotto)
admin.site.register(Ordine)
