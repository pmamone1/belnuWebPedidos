from email import message
from django.shortcuts import render, redirect
from django.http import JsonResponse
from carts.models import CartItem
from .forms import OrderForm
from datetime import datetime
from .models import Order, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from accounts.models import UserProfile



# Create your views here.

def place_order(request, total=0, quantity=0):
    
    # busca el usuarrio
    current_user = request.user
    # busca los items que eligio el usuario
    cart_items = CartItem.objects.filter(user=current_user)
    #cuenta la cantidad de items del carrito
    cart_count = cart_items.count()

    #si el carro esta vacio se redirige al store
    if cart_count <= 0:
        print("cart_count="+ str(cart_count))
        return redirect('store')

    #inicializa el valor del total a 0
    grand_total = 0
    
    # saca el total del pedido mas la cantidad de ejemplares
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    # guarda el total del pedido
    grand_total = total
            
    print("entro en el checkout")
    user = request.user
    # busca el profile en la bd
    userProfile = UserProfile.objects.get(user=current_user)
    #asigna el numero de vendedor y nombre
    numero_vendedor = userProfile.numero_vendedor
    nombre_vendedor = userProfile.nombre_vendedor
    
    #yr=int(datetime.date.today().strftime('%Y'))
    #mt=int(datetime.date.today().strftime('%m'))
    #dt=int(datetime.date.today().strftime('%d'))
    
    #d = datetime(yr,mt,dt)
    d=datetime.now()
    current_date = d.strftime("%Y%m%d%H%M%S")
        
    # arma el numero de pedido
    order_number = current_date+"_"+str(numero_vendedor)+"_"+str(nombre_vendedor) 
    
    if request.method == 'POST':
        print("entro en el post")
        form = OrderForm(request.POST)
        
        # Guarda el pedido en la base de datos
        data = Order()
        data.user = current_user
        data.numero_vendedor = numero_vendedor
        data.nombre_vendedor = nombre_vendedor
        data.order_number = order_number  
        data.first_name = current_user.first_name
        data.last_name = current_user.last_name
        data.phone = current_user.phone_number
        data.email = current_user.email
            
        data.order_total = grand_total
        
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()
        print("guardamos la orden!")

        # Mover todos los carrito items hacia la tabla order product
        order = Order.objects.filter(user=request.user, is_ordered=False, order_number=order_number).first()
        
        cart_items = CartItem.objects.filter(user=request.user)
        
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order = order
            orderproduct.profile = userProfile            
            orderproduct.user = user
            orderproduct.product = item.product
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.numero_pedido = order_number
            orderproduct.save()
            ############################
            print("el item id="+str(item.id))
            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variation.set(product_variation)
            print(product_variation)
            orderproduct.save()

            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()
        CartItem.objects.filter(user=request.user).delete()
        data.is_ordered = True
        data.status ="Accepted"
        
        data.save()
        print("borramos el carrito y se guardo todo!")
        context = {
            'grand_total': str(grand_total),
            'numero_vendedor': numero_vendedor,
            'nombre_vendedor': nombre_vendedor,
            'nombre_completo': current_user.first_name + ", " + current_user.last_name,
            'numero_pedido': order_number,
            'status': data.status,
            'fecha': str(data.created_at),
        }
        return redirect('order_complete', grand_total=grand_total, numero_vendedor=numero_vendedor, nombre_vendedor=nombre_vendedor, nombre_completo=current_user.first_name + ", " + current_user.last_name, numero_pedido=order_number, status=data.status, fecha=data.created_at)   
            
       
       
       
    context = {
            'user': user,
            'cart_items': cart_items,
            'grand_total': grand_total,
            'numero_vendedor': numero_vendedor,
            'nombre_vendedor': nombre_vendedor,
            'fecha_pedido': datetime.now().strftime("%Y-%m-%d"),
            'order_number': order_number,
            'total_items':quantity,
        }
    return render(request,'store/checkout.html',context)



def order_complete(request,numero_vendedor,grand_total,nombre_vendedor,nombre_completo,numero_pedido,status,fecha):
    try:
        order = Order.objects.get(order_number=numero_pedido, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
    except:
        pass
    print(ordered_products)
    print(ordered_products.count())
    context = {
            'ordered_products': ordered_products,
            'grand_total': str(grand_total),
            'numero_vendedor': numero_vendedor,
            'nombre_vendedor': nombre_vendedor,
            'nombre_completo': nombre_completo,
            'fecha_pedido': fecha,
            'numero_pedido': numero_pedido,
            'nombre_completo': nombre_completo,
            'status': status,
        }
        
    return render(request, 'orders/order_complete.html', context)
