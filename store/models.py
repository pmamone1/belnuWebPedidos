from tabnanny import verbose
from django.db import models
from category.models import Category
from accounts.models import Account
from django.db.models import Avg, Count
from django.urls import reverse


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True,verbose_name='Nombre Producto')
    slug = models.SlugField(max_length=200,unique=True)
    description = models.CharField(max_length=500,blank=True,verbose_name='Descripción')
    price = models.DecimalField(max_digits=18,decimal_places=2,verbose_name='PVP')
    recargo_interior = models.DecimalField(max_digits=18,decimal_places=2,verbose_name='Recargo Interior')
    porcentaje_vv = models.DecimalField(max_digits=18,decimal_places=2,verbose_name='% Vendedor')
    images = models.ImageField(upload_to='photos/products',blank=True,verbose_name='Imagen')
    stock = models.IntegerField(verbose_name='Stock')
    is_available = models.BooleanField(default=True,verbose_name='Disponible')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='Categoria')
    created_date = models.DateField(auto_now_add=True,verbose_name='Fecha de creacion')
    modified_date = models.DateField(auto_now=True,verbose_name='Fecha de actualizacion')
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['product_name', '-created_date']
        
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def pvp_total(self):
        return self.price + self.recargo_interior
    
    def precio_vv(self):
        return (self.price*self.porcentaje_vv/100) + self.recargo_interior
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count=0
        if reviews['count'] is not None:
            count = int(reviews['count'])

        return count

    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.CharField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Valoracion"
        verbose_name_plural = "Valoraciones"
        ordering = ['rating']
    
    def __str__(self):
        return self.subject

variation_category_choices = (
                                ('Edicion', 'Edicion'),
                            )

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='Producto')
    subtitulo = models.CharField(max_length=100,verbose_name='Subtitulo',blank=True)
    variantion_category = models.CharField(max_length=200,verbose_name='Variacion', choices = variation_category_choices)
    variation_value = models.CharField(max_length=200,verbose_name='Edicion')
    stock = models.IntegerField(verbose_name='Stock')
    image = models.ImageField(upload_to='photos/products',blank=True,verbose_name='Imagen')
    is_active = models.BooleanField(default=True,verbose_name='Disponible')
    created_date = models.DateField(auto_now_add=True,verbose_name='Fecha de creacion')
    updated_date = models.DateField(auto_now=True,verbose_name='Fecha de actualizacion')
    
    
    def __unicode__(self):
        return self.product
    class Meta:
        verbose_name = "Edicion"
        verbose_name_plural = "Ediciones"
           