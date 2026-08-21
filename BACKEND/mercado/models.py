from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('VENDEDOR', 'Productor / Vendedor'),
        ('COMPRADOR', 'Comprador / Supermercado'),
    )
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('OTRO', 'Otro / Prefiero no decir'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='COMPRADOR')
    correo = models.EmailField(max_length=254, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, default='M')
    cedula = models.CharField(max_length=30, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    finca = models.CharField(max_length=150, blank=True, null=True)
    direccion_exacta = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=100, default='Nueva Guinea')
    
    # DATOS BANCARIOS DEL VENDEDOR
    banco_nombre = models.CharField(max_length=100, blank=True, null=True, default='Banco LAFISE')
    numero_cuenta = models.CharField(max_length=100, blank=True, null=True)
    titular_cuenta = models.CharField(max_length=150, blank=True, null=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.rol})"


class CosechaProducto(models.Model):
    CATEGORIAS = (
        ('CITRICO', 'Cítricos (Naranja, Limón, Mandarina)'),
        ('FRUTA', 'Otras Frutas Frescas'),
    )
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mis_cosechas')
    nombre_producto = models.CharField(max_length=150)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='CITRICO')
    precio_justo = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=50, default='Cien')
    cantidad_disponible = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='cosechas/', blank=True, null=True)
    
    es_preventa = models.BooleanField(default=False)
    fecha_corte_estimada = models.DateField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_producto} - {self.cantidad_disponible} {self.unidad_medida}"


class TicketTransaccion(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Apartado / Pendiente de Entrega'),
        ('COMPLETADO', 'Venta Validada y Finalizada'),
        ('CANCELADO', 'Cancelado (Inventario Retornado)'),
    )
    
    codigo_ticket = models.CharField(max_length=20, unique=True)
    comprador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mis_compras')
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mis_ventas')
    producto = models.ForeignKey(CosechaProducto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total_pagar = models.DecimalField(max_digits=12, decimal_places=2)
    
    # REFERENCIA DE TRANSFERENCIA O PAGO
    referencia_pago = models.CharField(max_length=100, blank=True, null=True, default='Efectivo contra entrega')
    
    pin_seguridad = models.CharField(max_length=6)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo_ticket} - {self.producto.nombre_producto} ({self.estado})"