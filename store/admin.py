from django.contrib import admin
from .models import Product
from django.utils.html import format_html
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'recargo_interior','precio_vv', 'porcentaje_vv', 'stock','category', 'is_available', 'modified_date','imagen')
    list_filter = ('is_available', 'category', 'modified_date')
    
    prepopulated_fields = {'slug': ('product_name',)}

    def imagen(self,obj):
        return format_html('<img src={}  width="80px" height="80px" />',obj.images.url)
    

admin.site.register(Product, ProductAdmin)
   
     