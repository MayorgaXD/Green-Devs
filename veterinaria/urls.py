from django.urls import path
from . import views

urlpatterns = [
    path('api/usuarios/', views.gestion_usuarios, name='api_usuarios'),
    path('api/especialistas/', views.gestion_especialistas, name='api_especialistas'),
]