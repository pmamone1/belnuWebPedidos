from django.contrib import admin
from  .models import Cart, CartItem
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display =('cart_id', 'date_added')
    readonly_fields = ('date_added',)
    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

class CartItemAdmin(admin.ModelAdmin):
    list_display =('product', 'cart', 'quantity','is_active')
    
    class Meta:
        verbose_name = "Item de Carrito"
        verbose_name_plural = "Items de Carrito"

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
