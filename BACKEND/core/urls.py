from django.contrib.admin import site as admin_site
from django.urls import path
from mercado.views import lista_productos_api

urlpatterns = [
    path('admin/', admin_site.urls),
    path('api/productos/', lista_productos_api, name='lista_productos_api'),
]