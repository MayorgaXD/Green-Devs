from rest_framework import serializers
from .models import Usuario, Especialista

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class EspecialistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialista
        fields = '__all__'