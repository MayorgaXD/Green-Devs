from django.http import JsonResponse
from .models import CosechaProducto

def lista_productos_api(request):
    region_buscada = request.GET.get('region', None)
    
    productos = CosechaProducto.objects.filter(disponibilidad_tierra=True)
    
    if region_buscada:
        productos = productos.filter(productor__perfil__region__icontains=region_buscada)
        
    data = []
    for p in productos:
        finca = p.productor.perfil.nombre_finca_o_negocio if hasattr(p.productor, 'perfil') else "Finca Independiente"
        region = p.productor.perfil.region if hasattr(p.productor, 'perfil') else "No especificada"
        
        data.append({
            'id': p.id,
            'nombre': p.nombre_producto,
            'categoria': p.categoria,
            'descripcion': p.descripcion,
            'precio': str(p.precio_justo),
            'unidad': p.unidad_medida,
            'disponible': p.cantidad_disponible,
            'productor': p.productor.get_full_name() or p.productor.username,
            'finca': finca,
            'region': region
        })
        
    return JsonResponse(data, safe=False)