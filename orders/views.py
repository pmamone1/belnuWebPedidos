from email import message
from django.shortcuts import render, redirect
from django.http import JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from accounts.models import UserProfile

# Create your views here.

def place_order(request, total=0, quantity=0):
    
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        print("cart_count="+ str(cart_count))
        return redirect('store')

    grand_total = 0
    

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    
    grand_total = total
            
    print("entro en el checkout")
    user = request.user
    userProfile = UserProfile.objects.get(user=current_user)
    numero_vendedor = userProfile.numero_vendedor
    nombre_vendedor = userProfile.nombre_vendedor
    yr=int(datetime.date.today().strftime('%Y'))
    mt=int(datetime.date.today().strftime('%m'))
    dt=int(datetime.date.today().strftime('%d'))
    d = datetime.date(yr,mt,dt)
    current_date = d.strftime("%Y%m%d")
        
    order_number = current_date+"_"+str(numero_vendedor)+"_"+str(nombre_vendedor) 
    
    if request.method == 'POST':
        print("entro en el post")
        form = OrderForm(request.POST)
        

        
        print("el formulario es valido")
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
       
    context = {
            'user': user,
            'cart_items': cart_items,
            'grand_total': grand_total,
            'numero_vendedor': numero_vendedor,
            'nombre_vendedor': nombre_vendedor,
            'fecha_pedido': datetime.date.today(),
            'order_number': order_number,
            'total_items':cart_items.count(),
        }
    return render(request,'store/checkout.html',context)



def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price*i.quantity

        #payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except(Order.DoesNotExist):
        return redirect('home')
