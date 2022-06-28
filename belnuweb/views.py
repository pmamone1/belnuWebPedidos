from django.shortcuts import render
from django.core.paginator import Paginator

from store.models import Product

# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True)
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()
    
    context = {'products':paged_products,
               'product_count': product_count,
               }
    
    return render(request, 'home.html', context)

