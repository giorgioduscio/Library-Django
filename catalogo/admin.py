from django.contrib import admin
from .models import Risorsa

@admin.register(Risorsa)
class ProdottoAdmin(admin.ModelAdmin):
    search_fields =['titolo', 'descrizione', 'prezzo']
    list_display  =['titolo', 'prezzo', 'disponibile', 'creato_il']
    list_filter   =['disponibile']
    list_editable =['disponibile', 'prezzo']
