from django.contrib import admin
from .models import Risorsa

@admin.register(Risorsa)
class ProdottoAdmin(admin.ModelAdmin):
    list_display  =['titolo', 'prezzo', 'disponibile', 'creato_il']
    list_filter   =['disponibile']
    search_fields =['titolo', 'descrizione', 'prezzo']
    list_editable =['disponibile', 'prezzo']
