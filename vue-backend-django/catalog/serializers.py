from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Libro, Autore


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


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'email': {'required': False, 'allow_blank': True}
        }
        
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user