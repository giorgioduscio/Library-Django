from django.contrib import admin
from .models import Artista, Album, Canzone, Genere

@admin.register(Genere)
class GenereAdmin(admin.ModelAdmin):
    list_display = ('id', 'titolo')
    search_fields = ('titolo',)

@admin.register(Artista)
class ArtistaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nazionalita', 'data_debutto')
    search_fields = ('nome', 'nazionalita')
    list_filter = ('nazionalita',)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'artista__nome', 'anno', 'genere', 'disponibile')
    list_filter = ('genere', 'disponibile', 'anno')
    search_fields = ('titolo', 'artista__nome')
    list_editable = ('disponibile',) # Permette di cambiare la disponibilità direttamente dalla lista

@admin.register(Canzone)
class CanzoneAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'album__titolo', 'traccia', 'durata_secondi')
    list_filter = ('album__artista', 'album')
    search_fields = ('titolo', 'album__titolo')
    ordering = ('album', 'traccia')
