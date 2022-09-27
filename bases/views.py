from django.shortcuts import render
from tienda.models import Producto

# Create your views here.
def home(request):
    productos = Producto.objects.all().filter(disponible=True)
    contexto = {'productos': productos}
    return render(request,'bases/home.html', contexto)


