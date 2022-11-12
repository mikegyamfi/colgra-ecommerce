import email
import secrets
import requests
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store import models
from django.contrib.auth.models import User 
import random
from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def index(request):
    raw_cart = models.Cart.objects.filter(user=request.user)
    for item in raw_cart:
        if item.product_qty > item.product.quantity:
            models.Cart.objects.delete(id=item.id)
    cart_items = models.Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart_items:
        total_price += item.product.selling_price * item.product_qty

    user_profile = models.UserProfile.objects.filter(user=request.user).first()

    total_price_paystack = total_price * 100

    ref = 'col'+str(random.randint(11111111, 99999999))
    while models.Payment.objects.filter(ref=ref) is None:
        ref = 'dstore'+str(random.randint(11111111, 99999999))
            
    
    context = {'cart_items':cart_items, 'total_price':total_price, 'amount':total_price_paystack, 'user_profile':user_profile, 'ref':ref}
    return render(request, 'store/layouts/checkout.html', context)

@login_required(login_url='login')
def place_order(request):
    if request.method == 'POST':
        new_order_items = models.Cart.objects.filter(user=request.user)
        price = 0 
        for item in new_order_items:
            price += item.product.selling_price

        new_payment = models.Payment.objects.create(
            amount = price,
            email = request.POST.get('email'),
            ref = request.POST.get('ref'),
        )
        new_payment.save()

        current_user = models.CustomUser.objects.filter(id=request.user.id).first()
        if not current_user.first_name:
            current_user.first_name = request.POST.get('fname')
            current_user.last_name = request.POST.get('lname')
            current_user.save()
        if not models.UserProfile.objects.filter(user=request.user):
            user_profile = models.UserProfile()
            user_profile.user = request.user
            user_profile.phone = request.POST.get('phone')
            user_profile.address = request.POST.get('address')
            user_profile.city = request.POST.get('city')
            user_profile.state = request.POST.get('state')
            user_profile.country = request.POST.get('country')
            user_profile.pincode = request.POST.get('pincode')
            user_profile.save()
            

        new_order = models.Order()
        new_order.user = request.user
        new_order.fname = request.POST.get('fname')
        new_order.lname = request.POST.get('lname')
        new_order.email = request.POST.get('email')
        new_order.phone = request.POST.get('phone')
        new_order.address = request.POST.get('address')
        new_order.city = request.POST.get('city')
        new_order.state = request.POST.get('state')
        new_order.country = request.POST.get('country')
        new_order.pincode = request.POST.get('pincode')

        new_order.payment_mode = request.POST.get('payment_mode')

        cart = models.Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price += item.product.selling_price * item.product_qty
        new_order.total_price = cart_total_price
        track_no = 'dstore'+str(random.randint(11111111, 99999999))
        while models.Order.objects.filter(tracking_number=track_no) is None:
            track_no = 'dstore'+str(random.randint(11111111, 99999999))
        new_order.tracking_number = track_no
        
        new_order.save()



        for item in new_order_items:
            models.OrderItem.objects.create(
                order = new_order,
                product = item.product,
                tracking_number = track_no,
                price = item.product.selling_price,
                quantity = item.product_qty
            )

            orderproduct = models.Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity -= item.product_qty
            orderproduct.save()

        messages.success(request, "Your order has been placed")

        verify_payment(request, new_payment.ref)
        

        for order in new_order_items:
            requests.get(f"https://sms.arkesel.com/sms/api?action=send-sms&api_key=WlZGdW9CdUxaeWJsc2hld1BTaU0&to=233275680647&from=Colgra&sms=New Order Placed\nCustomer Name: {new_order.fname} {new_order.lname}\nProduct: {order.product.name}\nQuantity: {order.product_qty}\nCustomer Tel: {new_order.phone}")
            requests.get(f"https://sms.arkesel.com/sms/api?action=send-sms&api_key=WlZGdW9CdUxaeWJsc2hld1BTaU0&to={new_order.phone}&from=Colgra&sms=New Order Placed Succesfully\nHello {new_order.fname}\nYour order has been placed successfully.\nProduct: {order.product.name}\nQuantity: {order.product_qty}\nPrice: {new_order.total_price}\nTracking Number: {new_order.tracking_number}\nKindly keep your tracking number safe as it will be needed in any enquiries you wish to make concerning your order.\n\nSincerely,\nThe Colgra Clothing Team.")

        models.Cart.objects.filter(user=request.user).delete()

        return redirect('home')
    
        
    
def verify_payment(request, ref):
    payment = models.Payment.objects.filter(ref=ref).first()
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "Successful")
    else:
        messages.error(request, "Failed")
    return redirect("home")
