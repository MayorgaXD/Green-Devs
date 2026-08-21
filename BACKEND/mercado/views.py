import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from .models import CosechaProducto, PerfilUsuario, TicketTransaccion

# ==========================================
# 1. AUTENTICACIÓN
# ==========================================

@csrf_exempt
def api_login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            perfil = getattr(user, 'perfil', None)
            return JsonResponse({
                'mensaje': 'Login exitoso',
                'usuario': {
                    'id': user.id,
                    'username': user.username,
                    'rol': perfil.rol if perfil else 'COMPRADOR',
                    'finca': perfil.finca if perfil else 'Finca Local',
                    'region': perfil.region if perfil else 'Nueva Guinea',
                    'telefono': perfil.telefono if perfil else '',
                    'banco_nombre': perfil.banco_nombre if perfil else 'Banco LAFISE',
                    'numero_cuenta': perfil.numero_cuenta if perfil else '',
                    'titular_cuenta': perfil.titular_cuenta if perfil else user.username
                }
            }, status=200)
        return JsonResponse({'error': 'Credenciales incorrectas'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_registro(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        rol = data.get('rol', 'COMPRADOR')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'El nombre de usuario ya existe'}, status=400)

        user = User.objects.create_user(username=username, password=password)
        PerfilUsuario.objects.create(
            user=user,
            rol=rol,
            correo=data.get('correo', ''),
            telefono=data.get('telefono', ''),
            sexo=data.get('sexo', 'M'),
            cedula=data.get('cedula', ''),
            finca=data.get('finca', ''),
            region=data.get('region', 'Nueva Guinea'),
            banco_nombre=data.get('banco_nombre', 'Banco LAFISE'),
            numero_cuenta=data.get('numero_cuenta', ''),
            titular_cuenta=data.get('titular_cuenta', '')
        )
        return JsonResponse({'mensaje': 'Usuario registrado exitosamente'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ==========================================
# 2. CATÁLOGO Y PERFIL VENDEDOR
# ==========================================

@csrf_exempt
def api_productos(request):
    if request.method == 'GET':
        vendedor_id = request.GET.get('vendedor_id')
        region = request.GET.get('region', '')
        productos = CosechaProducto.objects.all().order_by('-id')
        
        if vendedor_id:
            productos = productos.filter(vendedor_id=vendedor_id)
        if region:
            productos = productos.filter(vendedor__perfil__region__icontains=region)

        data = []
        for p in productos:
            perfil = getattr(p.vendedor, 'perfil', None)
            data.append({
                'id': p.id,
                'vendedor_id': p.vendedor.id,
                'nombre': p.nombre_producto,
                'categoria': p.categoria,
                'precio': float(p.precio_justo),
                'unidad': p.unidad_medida,
                'disponible': p.cantidad_disponible,
                'es_preventa': p.es_preventa,
                'fecha_corte': str(p.fecha_corte_estimada) if p.fecha_corte_estimada else None,
                'imagen': request.build_absolute_uri(p.imagen.url) if p.imagen else None,
                'vendedor': p.vendedor.username,
                'finca': perfil.finca if perfil and perfil.finca else 'Finca Local',
                'telefono': perfil.telefono if perfil and perfil.telefono else 'N/D',
                'banco_nombre': perfil.banco_nombre if perfil and perfil.banco_nombre else 'Banco LAFISE',
                'numero_cuenta': perfil.numero_cuenta if perfil and perfil.numero_cuenta else '102938475',
                'titular_cuenta': perfil.titular_cuenta if perfil and perfil.titular_cuenta else p.vendedor.username
            })
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            vendedor_id = request.POST.get('vendedor_id')
            user = User.objects.get(id=vendedor_id)
            es_preventa = request.POST.get('es_preventa') == 'true'
            fecha_corte = request.POST.get('fecha_corte') if es_preventa else None

            prod = CosechaProducto.objects.create(
                vendedor=user,
                nombre_producto=request.POST.get('nombre'),
                categoria=request.POST.get('categoria', 'CITRICO'),
                precio_justo=request.POST.get('precio'),
                unidad_medida=request.POST.get('unidad'),
                cantidad_disponible=request.POST.get('disponible'),
                es_preventa=es_preventa,
                fecha_corte_estimada=fecha_corte if fecha_corte else None,
                imagen=request.FILES.get('imagen')
            )
            return JsonResponse({'mensaje': 'Publicado con éxito', 'id': prod.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def api_perfil_vendedor(request, vendedor_id):
    try:
        user = User.objects.get(id=vendedor_id)
        perfil = getattr(user, 'perfil', None)
        productos = CosechaProducto.objects.filter(vendedor=user).order_by('-id')
        
        data_productos = []
        for p in productos:
            data_productos.append({
                'id': p.id,
                'nombre': p.nombre_producto,
                'categoria': p.categoria,
                'precio': float(p.precio_justo),
                'unidad': p.unidad_medida,
                'disponible': p.cantidad_disponible,
                'imagen': request.build_absolute_uri(p.imagen.url) if p.imagen else None,
            })
            
        return JsonResponse({
            'vendedor': {
                'id': user.id,
                'username': user.username,
                'telefono': perfil.telefono if perfil and perfil.telefono else 'No proporcionado',
                'finca': perfil.finca if perfil and perfil.finca else 'General',
                'region': perfil.region if perfil else 'Nueva Guinea',
                'banco_nombre': perfil.banco_nombre if perfil else 'Banco LAFISE',
                'numero_cuenta': perfil.numero_cuenta if perfil else 'N/D',
                'titular_cuenta': perfil.titular_cuenta if perfil else user.username
            },
            'productos': data_productos
        }, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Vendedor no encontrado'}, status=404)


# ==========================================
# 3. TICKETS, INVENTARIO Y BANDEJA EN TIEMPO REAL
# ==========================================

@csrf_exempt
def api_crear_ticket(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        comprador_id = data.get('comprador_id')
        producto_id = data.get('producto_id')
        cantidad = int(data.get('cantidad', 0))
        referencia_pago = data.get('referencia_pago', 'Efectivo contra entrega')

        with transaction.atomic():
            producto = CosechaProducto.objects.select_for_update().get(id=producto_id)
            comprador = User.objects.get(id=comprador_id)

            if cantidad <= 0:
                return JsonResponse({'error': 'La cantidad debe ser mayor a cero'}, status=400)
            
            if producto.cantidad_disponible < cantidad:
                return JsonResponse({'error': f'Stock insuficiente. Solo quedan {producto.cantidad_disponible} disponibles.'}, status=400)

            # 1. Descuento en tiempo real
            producto.cantidad_disponible -= cantidad
            producto.save()

            # 2. Generar Ticket y PIN único
            codigo = f"GD-{random.randint(100000, 999999)}"
            pin = str(random.randint(1000, 9999))
            total = float(producto.precio_justo) * cantidad

            ticket = TicketTransaccion.objects.create(
                codigo_ticket=codigo,
                comprador=comprador,
                vendedor=producto.vendedor,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio_justo,
                total_pagar=total,
                referencia_pago=referencia_pago,
                pin_seguridad=pin,
                estado='PENDIENTE'
            )

            perfil_vendedor = getattr(producto.vendedor, 'perfil', None)

            return JsonResponse({
                'mensaje': 'Apartado realizado con éxito',
                'ticket': {
                    'codigo': ticket.codigo_ticket,
                    'producto': producto.nombre_producto,
                    'cantidad': ticket.cantidad,
                    'unidad': producto.unidad_medida,
                    'total': float(ticket.total_pagar),
                    'referencia_pago': ticket.referencia_pago,
                    'comprador': comprador.username,
                    'vendedor': producto.vendedor.username,
                    'telefono_vendedor': perfil_vendedor.telefono if perfil_vendedor and perfil_vendedor.telefono else 'N/D',
                    'pin': ticket.pin_seguridad,
                    'estado': ticket.estado,
                    'fecha': ticket.fecha_creacion.strftime("%d/%m/%Y %H:%M")
                }
            }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_pedidos_vendedor(request, vendedor_id):
    """Bandeja en vivo: Lista todos los pedidos recibidos por este vendedor o relacionados"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        # Busca tickets donde el usuario sea el vendedor O comprador (soporte demo hackathon)
        tickets = TicketTransaccion.objects.filter(
            Q(vendedor_id=vendedor_id) | Q(comprador_id=vendedor_id)
        ).order_by('-id')

        # Si no hay específicos, retorna los últimos registrados para visualización continua
        if not tickets.exists():
            tickets = TicketTransaccion.objects.all().order_by('-id')[:10]

        data = []
        for t in tickets:
            perfil_comp = getattr(t.comprador, 'perfil', None)
            data.append({
                'id': t.id,
                'codigo': t.codigo_ticket,
                'producto': t.producto.nombre_producto,
                'cantidad': t.cantidad,
                'unidad': t.producto.unidad_medida,
                'total': float(t.total_pagar),
                'referencia_pago': t.referencia_pago or 'Efectivo contra entrega',
                'comprador': t.comprador.username,
                'vendedor': t.vendedor.username,
                'telefono_comprador': perfil_comp.telefono if perfil_comp and perfil_comp.telefono else 'N/D',
                'estado': t.estado,
                'fecha': t.fecha_creacion.strftime("%d/%m/%Y %H:%M")
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_cancelar_ticket(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        codigo = data.get('codigo_ticket')

        with transaction.atomic():
            ticket = TicketTransaccion.objects.select_for_update().get(codigo_ticket=codigo)
            
            if ticket.estado != 'PENDIENTE':
                return JsonResponse({'error': 'Solo se pueden cancelar órdenes en estado pendiente'}, status=400)

            # Devolver stock al producto
            producto = ticket.producto
            producto.cantidad_disponible += ticket.cantidad
            producto.save()

            ticket.estado = 'CANCELADO'
            ticket.save()

            return JsonResponse({'mensaje': 'Ticket cancelado. El stock fue regresado a la finca.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_validar_ticket(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        codigo = data.get('codigo_ticket')
        pin_ingresado = str(data.get('pin')).strip()

        ticket = TicketTransaccion.objects.get(codigo_ticket=codigo)

        if ticket.estado != 'PENDIENTE':
            return JsonResponse({'error': f'Este ticket ya está {ticket.estado}'}, status=400)

        if ticket.pin_seguridad != pin_ingresado:
            return JsonResponse({'error': 'PIN de validación incorrecto'}, status=400)

        ticket.estado = 'COMPLETADO'
        ticket.save()

        return JsonResponse({'mensaje': '¡Venta validada exitosamente! Transacción cerrada y verificada.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def api_eliminar_producto(request, producto_id):
    if request.method not in ['POST', 'DELETE']:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body) if request.body else {}
        usuario_id = data.get('usuario_id')
        producto = CosechaProducto.objects.get(id=producto_id)

        if usuario_id:
            user = User.objects.get(id=usuario_id)
            perfil = getattr(user, 'perfil', None)
            es_admin = (perfil and perfil.rol == 'ADMIN') or user.is_superuser
            if producto.vendedor != user and not es_admin:
                return JsonResponse({'error': 'No tienes permiso para eliminar esta cosecha.'}, status=403)

        producto.delete()
        return JsonResponse({'mensaje': 'Cosecha eliminada exitosamente del inventario.'}, status=200)
    except CosechaProducto.DoesNotExist:
        return JsonResponse({'error': 'La cosecha ya no existe.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)