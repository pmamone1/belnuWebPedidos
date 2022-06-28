from django.contrib import admin
from .models import Product,Variation

from django.utils.html import format_html
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'recargo_interior','precio_vv', 'porcentaje_vv', 'stock','stock_total','category', 'is_available', 'modified_date','imagen')
    list_filter = ('is_available', 'category', 'modified_date')
    
    prepopulated_fields = {'slug': ('product_name',)}

    def imagen(self,obj):
        return format_html('<img src={}  width="80px" height="80px" />',obj.images.url)

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','subtitulo','variation_value','stock','is_active','imagen')
    list_editable = ("is_active",)
    search_fields = ['product__product_name','subtitulo','is_active','variation_value','stock']
    list_filter = ['product','is_active']
    
    def imagen(self,obj):
        return format_html('<img src={}  width="80px" height="80px" />',obj.image.url)


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation,VariationAdmin)   
     