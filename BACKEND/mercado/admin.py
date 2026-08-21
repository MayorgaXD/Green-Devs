from django.contrib import admin
from .models import PerfilUsuario, CosechaProducto, TicketTransaccion

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'telefono', 'finca', 'region', 'banco_nombre', 'numero_cuenta')
    search_fields = ('user__username', 'finca', 'telefono')

@admin.register(CosechaProducto)
class CosechaProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'vendedor', 'categoria', 'precio_justo', 'unidad_medida', 'cantidad_disponible', 'es_preventa')
    list_filter = ('categoria', 'es_preventa')
    search_fields = ('nombre_producto', 'vendedor__username')

@admin.register(TicketTransaccion)
class TicketTransaccionAdmin(admin.ModelAdmin):
    list_display = ('codigo_ticket', 'producto', 'vendedor', 'comprador', 'cantidad', 'total_pagar', 'referencia_pago', 'pin_seguridad', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('codigo_ticket', 'pin_seguridad', 'referencia_pago', 'comprador__username', 'vendedor__username')