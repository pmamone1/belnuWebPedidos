from telnetlib import STATUS
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, UserProfileForm, UserForm
from .models import Account, UserProfile
from orders.models import Order, OrderProduct
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models import Q
from .serializers import OrderSerializer
from django.shortcuts import HttpResponse
import json

import smtplib
import ssl
from email.message import EmailMessage



from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests

# Create your views here.
def register(request):
    form = RegistrationForm()
    
    if request.method == 'POST':
        numero_vendedor = request.POST.get('numero_vendedor',"")
        nombre_vendedor = request.POST.get('nombre_vendedor',"")
        if numero_vendedor == "" or nombre_vendedor == "":
            messages.warning(request, 'No ingreso Numero y/o Nombre de Vendedor')
            return redirect('register')             
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password )
            user.phone_number = phone_number
            user.save()


            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.numero_vendedor = numero_vendedor
            profile.nombre_vendedor = nombre_vendedor
            profile.save()

            current_site = get_current_site(request)

            # Configuracion de los mails
            email_sender = 'belnu.pedidos@gmail.com'
            email_password = 'gmgznpennopfxvjg' #esta es la contraseña global de gmail para este mail
            email_receiver = email

            # configuramos el mail 
            subject = 'Por favor activa tu cuenta en Belnu Pedidos Web!'
            body = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

            # Add SSL (layer of security)
            context = ssl.create_default_context()

            # Log in and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
                messages.success(request, 'Se registro el usuario exitosamente')
            return redirect('/accounts/login/?command=verification&email='+email)


    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            print("hay usu")
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation= item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    #  product_variation = [1, 2, 3, 4, 5]
                    #  ex_var_list = [5, 6, 7, 8]

                    for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity +=1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()
            except:
                pass


            # http://127.0.0.1:8000/accounts/login/?next=/cart/checkout/
            
            auth.login(request, user)
            messages.success(request, 'Has iniciado sesion exitosamente')
            url  = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
    
        else:
            
            if Account.objects.filter(email=email).exists():
                user=Account.objects.filter(email=email).first()
                print("pppp" +email)
                messages.error(request, 'El usuario no se encuentra activo')
                current_site = get_current_site(request)

                # Configuracion de los mails
                email_sender = 'belnu.pedidos@gmail.com'
                email_password = 'gmgznpennopfxvjg' #esta es la contraseña global de gmail para este mail
                email_receiver = email

                # configuramos el mail 
                subject = 'Por favor activa tu cuenta en Belnu Pedidos Web!'
                body = render_to_string('accounts/account_verification_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })

                em = EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                em['Subject'] = subject
                em.set_content(body)

                # Add SSL (layer of security)
                context = ssl.create_default_context()

                # Log in and send the email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())
                    messages.success(request, 'No has activado tu cuenta todavia, te hemos enviado un nuevo enlace a tu mail para que puedas activar tu cuenta')
                return redirect('/accounts/login/?command=verification&email='+email)
            else:    
                print("no hay usu")
                messages.error(request, 'Las credenciales son incorrectas')
                return redirect('login')


    return render(request, 'accounts/login.html')
  
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Has salido de sesion')

    return redirect('login')



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Felicidades, tu cuenta esta activa!')
        return redirect('login')
    else:
        messages.error(request, 'La activacion es invalida')
        return redirect('register')

@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_admin:
        orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    else:
        orders = Order.objects.order_by('-created_at').filter(is_ordered=True)
    orders_count = orders.count()

    userprofile = UserProfile.objects.get(user_id=request.user.id)

    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }

    return render(request, 'accounts/dashboard.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)

            # Configuracion de los mails
            email_sender = 'belnu.pedidos@gmail.com'
            email_password = 'gmgznpennopfxvjg' #esta es la contraseña global de gmail para este mail
            email_receiver = email

            # configuramos el mail 
            subject = 'Por favor activa tu cuenta en Belnu Pedidos Web!'
            body = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

            # Add SSL (layer of security)
            context = ssl.create_default_context()

            # Log in and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
                
            messages.success(request, 'Un email fue enviado a tu bandeja de entrada para resetear tu password')
            return redirect('login')
        else:
            messages.error(request, 'La cuenta de usuario no existe')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user=None

        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request, 'Por favor resetea tu password')
            return redirect('resetPassword')
        else:
            messages.error(request, 'El link ha expirado')
            return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'El password se reseteo correctamente')
            return redirect('login')
        else:
            messages.error(request, 'El password de confirmacion no concuerda')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')

def filtrar_pedido(request):
    if request.method == 'POST':
        filtro= request.POST.get('filtro')
        print(filtro)
    try:    
        if filtro =="1":
            orders = Order.objects.all().order_by('-created_at')
        elif filtro =="2":
            orders = Order.objects.filter(is_ordered=True,status="Accepted").order_by('-created_at')
        elif filtro =="3":
            orders = Order.objects.filter(is_ordered=True,status="Completed").order_by('-created_at')
        elif filtro =="4":
            orders = Order.objects.filter(is_ordered=False,status="Cancelado").order_by('-created_at')
        
    except:
        pass
    
    paginator = Paginator(orders, 5)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = orders.count()
    
    if filtro=="1":
        filtro="Todos"
    elif filtro=="2":
        filtro="Pendientes"
    elif filtro=="3":
        filtro="Enviados"
    elif filtro=="4":
        filtro="Cancelados"
    print("el filtro que esta pasando es =" +filtro)
    
    context = {
        'product_count': product_count,
        'orders': paged_products,
        'filtro': filtro,
    }
     
    return render(request, 'accounts/my_orders.html', context)
    
    


def my_orders(request):
    if not request.user.is_admin:
        orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    else:
        orders = Order.objects.all().filter(status="Accepted").order_by('-created_at')
        
    paginator = Paginator(orders, 5)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = orders.count()
        
    context = {
        'product_count': product_count,
        'orders': paged_products,
    }
     
    return render(request, 'accounts/my_orders.html', context)

def borrar_pedido(request, pk):
    order = Order.objects.get(pk=pk)
    if order.status =="Accepted":
        print("Entro")
        order.status ="Cancelado"
        order.is_ordered = False
        order.save()
        messages.success(request, 'El pedido se cancelo correctamente, se enviara un email al vendedor')
        current_site = get_current_site(request)

        # Configuracion de los mails
        email_sender = 'belnu.pedidos@gmail.com'
        email_password = 'gmgznpennopfxvjg' #esta es la contraseña global de gmail para este mail
        email_receiver = order.email

        # configuramos el mail 
        subject = 'Tu pedido fue Cancelado!'
        body = render_to_string('accounts/borrar_pedido_email.html', {
                'user': order.user,
                'domain': current_site,
                'order':order,
            })

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        return redirect('my_orders')
    else:
        print("no entro")



@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    vendedor=UserProfile.objects.get(user=request.user)

    print(vendedor.numero_vendedor, vendedor.nombre_vendedor)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Su informacion fue guardada con exito')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
        'numero_vendedor': vendedor.numero_vendedor,
        'nombre_vendedor': vendedor.nombre_vendedor,
    }

    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()

                messages.success(request, 'El Password se actualizo exitosamente')
                return redirect('change_password')
            else:
                messages.error(request, 'Por favor ingrese un password valido')
                return redirect('change_password')
        else:
            messages.error(request, 'El password no coincide con la confirmacion de password')
            return redirect('change_password')

    return render(request, 'accounts/change_password.html')

def selected_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order_product_id = OrderProduct.objects.filter(order=order)

    paginator = Paginator(order_product_id, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = order_product_id.count()
    
    context = {
        'order': order,
        'order_product': paged_products,
        'product_count': product_count,
        'order_p': paged_products,    
        'fecha': order.created_at,
        }
    return render(request, 'accounts/selected_order.html', context)
