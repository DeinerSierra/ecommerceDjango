from .models import Carro, CarroItem
from .views import _carro_id

def contador(request):
    contador_carro = 0
    try:
        carro = Carro.objects.filter(carro_id = _carro_id(request))
        carro_items = CarroItem.objects.all().filter(carro = carro[:1])
        for carro_item in carro_items:
            contador_carro += carro_item.cantidad
    except Carro.DoesNotExist:
        contador_carro = 0
    return dict(contador_carro=contador_carro)
        