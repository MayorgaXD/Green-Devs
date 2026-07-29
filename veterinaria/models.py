from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    ROLES = [
        ('USUARIO', 'Usuario (Productor/Comprador)'),
        ('AUDITOR', 'Auditor de Calidad/Precios'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=15, choices=ROLES, default='USUARIO')
    region = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - Rol: {self.rol}"