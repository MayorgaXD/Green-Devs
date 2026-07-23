from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Usuario, Especialista
from .serializers import UsuarioSerializer, EspecialistaSerializer

# --- ENDPOINTS PARA GANADEROS (USUARIOS) ---

@api_view(['GET', 'POST'])
def gestion_usuarios(request):
    # Si la app externa pide VER la información guardada
    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Si la app externa envía el FORMULARIO COMPLETADO para GUARDAR
    elif request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() # Se guarda automáticamente en PostgreSQL
            return Response({"mensaje": "Ganadero guardado con éxito", "datos": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- ENDPOINTS PARA VETERINARIOS (ESPECIALISTAS) ---

@api_view(['GET', 'POST'])
def gestion_especialistas(request):
    # Si la app externa pide VER la lista de veterinarios
    if request.method == 'GET':
        especialistas = Especialista.objects.all()
        serializer = EspecialistaSerializer(especialistas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Si el veterinario llenó su FORMULARIO y la app externa lo envía para GUARDAR
    elif request.method == 'POST':
        serializer = EspecialistaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() # Se guarda automáticamente en PostgreSQL
            return Response({"mensaje": "Especialista guardado con éxito", "datos": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)