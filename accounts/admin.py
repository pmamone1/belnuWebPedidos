from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,Distribuidora,Subcuenta

class AccountAdmin(UserAdmin):
    list_display =('email', 'first_name', 'last_name','username', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'    
    
class DistribuidoraAdmin(admin.ModelAdmin): 
    list_display =('codigo','provincia','nombre','ciudad')
    readonly_fields = ('created_at','updated_at')
    
class SubcuentaAdmin(admin.ModelAdmin):
    list_display =('distribuidora','nombre','codigo','provincia','ciudad')
    readonly_fields = ('created_at','updated_at')
    
# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(Distribuidora,DistribuidoraAdmin)
admin.site.register(Subcuenta,SubcuentaAdmin)
