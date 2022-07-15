from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    #path('payments/', views.payments, name='payments'),
    path('order_complete/<str:numero_vendedor>/<str:grand_total>/<str:nombre_vendedor>/<str:nombre_completo>/<str:numero_pedido>/<str:status>/<str:fecha>/', views.order_complete, name='order_complete'),
]
#numero_vendedor,grand_total,nombre_vendedor,nombre_completo,numero_pedido,status,fecha