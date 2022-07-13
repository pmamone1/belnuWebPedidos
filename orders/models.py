from tabnanny import verbose
from django.db import models
from accounts.models import Account,UserProfile
from store.models import Product, Variation

# Create your models here.
class Order(models.Model):
    STATUS = (
        ('New', 'Nuevo'),
        ('Accepted', 'Aceptado'),
        ('Completed', 'Completado'),
        ('Cancelled', 'Cancelado'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True,verbose_name='Usuario')
    numero_vendedor = models.IntegerField(blank=True,verbose_name='Numero de vendedor',null=True)
    nombre_vendedor = models.CharField(blank=True,max_length=50,verbose_name='Nombre de vendedor',null=True)
    order_number = models.CharField(max_length=20,verbose_name='Numero de Pedido')
    first_name = models.CharField(max_length=50,verbose_name='Nombre')
    last_name = models.CharField(max_length=50,verbose_name='Apellido')
    phone = models.CharField(max_length=50,verbose_name='Telefono',blank=True)
    email = models.CharField(max_length=50,verbose_name='Email')
    order_total = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Total',null=True)
    
    status = models.CharField(max_length=50, choices=STATUS, default='New',verbose_name='Estado')
    ip = models.CharField(blank=True, max_length=20,verbose_name='IP')
    is_ordered = models.BooleanField(default=False,verbose_name='Ordenado')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Fecha de creacion')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Fecha de actualizacion')

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.addres_line_1} {self.addres_line_2}'

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,verbose_name='Pedido')
    user = models.ForeignKey(Account, on_delete=models.CASCADE,verbose_name='Usuario')
    profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='Producto')
    variation = models.ManyToManyField(Variation, blank=True,verbose_name='Variaciones')
    quantity = models.IntegerField(verbose_name='Cantidad')
    product_price = models.FloatField(verbose_name='Precio')
    ordered = models.BooleanField(default=False,verbose_name='Ordenado')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Fecha de creacion')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Fecha de actualizacion')

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = "Producto Pedido"
        verbose_name_plural = "Productos del Pedido"