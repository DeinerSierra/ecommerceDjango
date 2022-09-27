from django.shortcuts import render, redirect, get_object_or_404
from tienda.models import Producto, Variedad
from .models import Carro, CarroItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

def _carro_id(request):
    carro = request.session.session_key
    if not carro:
        carro = request.session.create()
    return carro


def agregar_al_carro(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    
    variacion_producto = []
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variacion = Variedad.objects.get(producto=producto,variedad_categoria__iexact = key, variedad_valor__iexact = value)
                variacion_producto.append(variacion)
            except:
                pass
    try:
        carro = Carro.objects.get(carro_id = _carro_id(request))
    except Carro.DoesNotExist:
        carro = Carro.objects.create(carro_id = _carro_id(request))
        carro.save()
        
    
    item_dentro_del_carro = CarroItem.objects.filter(producto = producto, carro = carro).exists()
    
    if item_dentro_del_carro:
        carro_item = CarroItem.objects.filter(producto = producto, carro = carro)
        lista_variantes = []
        id = []
        for item in carro_item:
            variedad_en_carro = item.variedad.all()
            lista_variantes.append(list(variedad_en_carro))
            id.append(item.id)
        
        if variacion_producto in lista_variantes:
            index = lista_variantes.index(variacion_producto)
            item_id = id[index]
            item = CarroItem.objects.get(producto=producto, id=item_id)
            item.cantidad +=1
            item.save()
        else:
            item =CarroItem.objects.create(producto=producto, cantidad=1, carro = carro)
            if len(variacion_producto) > 0:
                item.variedad.clear()
                item.variedad.add(*variacion_producto)
            item.save()
    else:
        carro_item = CarroItem.objects.create(producto = producto, cantidad = 1, carro = carro)
        if len(variacion_producto) > 0:
           carro_item.variedad.clear()
           carro_item.variedad.add(*variacion_producto)
        carro_item.save()
    
    return redirect('carrito:carro')
    
        


def remover_carro(request, producto_id, carro_item_id):

    producto = get_object_or_404(Producto, id=producto_id)
    try:
        if request.user.is_authenticated:
            carro_item = CarroItem.objects.get(producto=producto, user=request.user, id=carro_item_id)
        else:
            carro = Carro.objects.get(carro_id=_carro_id(request))
            carro_item = CarroItem.objects.get(producto=producto, carro=carro, id=carro_item_id)
        if carro_item.cantidad > 1:
            carro_item.cantidad -= 1
            carro_item.save()
        else:
            carro_item.delete()
    except:
        pass
    return redirect('carrito:carro')


def remover_carro_item(request, producto_id, carro_item_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.user.is_authenticated:
        carro_item = CarroItem.objects.get(producto=producto, user=request.user, id=carro_item_id)
    else:
        carro = Carro.objects.get(carro_id=_carro_id(request))
        carro_item = CarroItem.objects.get(producto=producto, carro=carro, id=carro_item_id)

    carro_item.delete()
    return redirect('carro')


def carro(request, total=0, cantidad=0, carro_items=None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            carro_items = CarroItem.objects.filter(usuario=request.user, is_active=True)
        else:
            carro = Carro.objects.get(carro_id=_carro_id(request))
            carro_items = CarroItem.objects.filter(carro=carro, is_active=True)

        for carro_item in carro_items:
            total += (carro_item.producto.precio * carro_item.cantidad)
            cantidad += carro_item.cantidad
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass ## solo ignora la exception

    contexto = {
        'total': total,
        'quantity': cantidad,
        'carro_items': carro_items,
        'tax' : tax,
        'grand_total': grand_total
    }

    return render(request, 'carro/carro.html', contexto)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)



        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass ## solo ignora la exception

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total': grand_total
    }

    return render(request, 'store/checkout.html', context)
