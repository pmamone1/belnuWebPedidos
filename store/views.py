from logging import exception
from django.shortcuts import render, get_object_or_404, redirect,HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from rest_framework import viewsets
from .serializers import VariationSerializer
import simplejson



from carts.models import CartItem
from carts.views import _cart_id

from .models import Product, Variation
from category.models import Category


def store(request, category_slug=None):
    categories = None
    products = None
    category = Category.objects.all()
        

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context =  {
        'products' : paged_products,
        'product_count': product_count,
        'category': category,
        
    }

    return render(request, 'store/store.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        
        context = {
            'single_product': single_product,
            'in_cart': in_cart,
        }
    except Exception as e:
        raise e
            
    return render(request, 'store/product_detail.html', context)
