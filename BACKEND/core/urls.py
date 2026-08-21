from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mercado import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', views.api_login, name='api_login'),
    path('api/auth/registro/', views.api_registro, name='api_registro'),
    path('api/productos/', views.api_productos, name='api_productos'),
    path('api/perfil/vendedor/<int:vendedor_id>/', views.api_perfil_vendedor, name='api_perfil_vendedor'),
    path('api/pedidos/vendedor/<int:vendedor_id>/', views.api_pedidos_vendedor, name='api_pedidos_vendedor'),
    path('api/productos/<int:producto_id>/eliminar/', views.api_eliminar_producto, name='api_eliminar_producto'),
    
    # ENDPOINTS DE TICKETS Y CONTROL DE STOCK
    path('api/tickets/crear/', views.api_crear_ticket, name='api_crear_ticket'),
    path('api/tickets/cancelar/', views.api_cancelar_ticket, name='api_cancelar_ticket'),
    path('api/tickets/validar/', views.api_validar_ticket, name='api_validar_ticket'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)