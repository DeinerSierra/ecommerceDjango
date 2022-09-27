from django.urls import path
from . import views

app_name = 'carrito'
urlpatterns = [
    path('', views.carro, name='carro'),
    path('agregar_carro/<int:producto_id>/', views.agregar_al_carro, name='agregar_carro'),
    path('remover_carro/<int:producto_id>/<int:carro_item_id>/', views.remover_carro, name='remover_carro'),
    path('remover_carro_item/<int:producto_id>/<int:carro_item_id>/', views.remover_carro_item, name='remover_carro_item'),
    path('checkout/', views.checkout, name='checkout'),
]