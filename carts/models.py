from tabnanny import verbose
from django.db import models
from store.models import Product

# Create your models here.
class Cart(models.Model):
   cart_id = models.CharField(max_length=250,blank=True,verbose_name='Id_Carrito')
   date_added = models.DateField(auto_now_add=True,verbose_name='Fecha de agregado')
    
   class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"
        ordering = ['-date_added']
    
   
   def __str__(self):
       return self.cart_id

    
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='Producto')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,verbose_name='Carrito')
    quantity = models.IntegerField(verbose_name='Cantidad')
    is_active =models.BooleanField(default=True,verbose_name='Activo')
   
    def __unicode__(self):
        return self.product

    def sub_total(self):
        return (self.product.price + self.product.recargo_interior) * self.quantity

    class Meta:
       verbose_name = "Item de Carrito"
       verbose_name_plural = "Items de Carrito"
       ordering = ['product']
       
       