from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import Libro, Autore, Scarpe


class AutoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autore
        fields = '__all__'


# For writing (POST, PUT, PATCH requests) - uses ID
class LibroWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = "__all__"


# For reading (GET requests) - shows full author
class LibroReadSerializer(serializers.ModelSerializer):
    autore = AutoreSerializer(read_only=True)

    class Meta:
        model = Libro
        fields = ["id", "titolo", "anno", "genere", "autore"]


class ScarpeSerializer(serializers.ModelSerializer):
    prezzo_scontato = serializers.ReadOnlyField()  # o SerializerMethodField() definendo però il metodo
    sconto = serializers.FloatField()
    prezzo = serializers.FloatField()
    
    class Meta:
        model = Scarpe
        fields = "__all__"

