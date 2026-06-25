from django.contrib import admin
from .models import Autore, Libro, Scarpe

# Register your models here.
@admin.register(Autore)
class AutoreAdmin(admin.ModelAdmin):
    list_display = ['nome', 'nazione']
    list_filter = ['nazione']
    list_editable =['nazione']


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ["titolo", "anno", "autore", "genere"]
    list_filter = ["genere"]


@admin.register(Scarpe)
class ScarpeAdmin(admin.ModelAdmin):
    list_display = ["nome", "prezzo", "descrizione", "categoria", "materiale", 'disponibilita', 'taglie_disponibili', 'immagine_url', 'sconto',]
    list_filter = ["categoria"]
    search_fields = ['categoria', 'nome']
    list_editable = ['sconto']
