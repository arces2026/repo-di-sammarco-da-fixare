from django.contrib import admin
from .models import Autore, Libro

# Register your models here.
@admin.register(Autore)
class AutoreAdmin(admin.ModelAdmin):
    list_display = ['nome', 'nazione']
    list_filter = ['nazione']
    list_editable =['nazione']
    
    
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titolo', 'anno', 'autore', 'genere']
    list_filter = ['genere']
    
    

