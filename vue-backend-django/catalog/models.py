from django.db import models

# Create your models here.
class Autore(models.Model):
    nome = models.CharField(max_length=200)
    nazione = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = 'Autori'
        
        
class Libro(models.Model):
    titolo = models.CharField(max_length=400)
    autore = models.ForeignKey(Autore, on_delete=models.CASCADE)
    anno = models.IntegerField()
    genere = models.CharField(max_length=100)
    
    def __str__(self):
        return self.titolo
    
    class Meta:
        verbose_name_plural = 'Libri'
    
    
    
    
