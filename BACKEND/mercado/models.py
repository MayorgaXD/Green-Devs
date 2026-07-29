from django.db import models
from django.contrib.auth.models import User

# 1. PERFIL DE USUARIO Y ROLES (Seguridad exigida por la rúbrica)
class PerfilUsuario(models.Model):
    ROLES_CHOICES = [
        ('ADMIN', 'Administrador del Sistema'),
        ('USUARIO', 'Usuario (Productor o Comprador)'),
        ('AUDITOR', 'Auditor de Calidad y Precios Justos'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=15, choices=ROLES_CHOICES, default='USUARIO')
    
    # Datos de Ubicación 
    region = models.CharField(max_length=100, help_text="Municipio o Departamento (ej. Nueva Guinea)")
    comunidad_o_direccion = models.CharField(max_length=200, help_text="Dirección del negocio o finca")
    coordenadas_gps = models.CharField(max_length=100, blank=True, null=True, help_text="Ubicación GPS opcional")
    
    # Identidad Local (Para el panel interactivo del agricultor)
    nombre_finca_o_negocio = models.CharField(max_length=150, blank=True, null=True)
    historia_productor = models.TextField(blank=True, null=True, help_text="Breve descripción de su identidad local")

    def __str__(self):
        return f"{self.user.username} - {self.rol} ({self.region})"


# 2. INVENTARIO DIGITAL DE FRUTAS Y CÍTRICOS (El núcleo del Reto Eco-Mercado)
class CosechaProducto(models.Model):
    CATEGORIAS_CHOICES = [
        ('FRUTA', 'Frutas en General'),
        ('CITRICO', 'Cítricos'),
    ]
    
    productor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'perfil__rol': 'USUARIO'}, related_name='cosechas')
    nombre_producto = models.CharField(max_length=100, help_text="Ej. Naranja agria, Limón criollo, Mandarina, Banano")
    categoria = models.CharField(max_length=100, choices=CATEGORIAS_CHOICES, default='FRUTA')
    descripcion = models.TextField(blank=True, help_text="Detalles del estado de la cosecha")
    
    # Precios Justos y Gestión de Inventario
    precio_justo = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio sugerido sin intermediarios")
    unidad_medida = models.CharField(max_length=50, help_text="Ej. Saco, Docena, Cien, Unidad")
    cantidad_disponible = models.PositiveIntegerField(help_text="Inventario digital en tiempo real")
    
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    disponibilidad_tierra = models.BooleanField(default=True, help_text="Indica si la tierra tiene producción activa actualmente")

    def __str__(self):
        return f"{self.nombre_producto} - {self.cantidad_disponible} {self.unidad_medida}(s)"