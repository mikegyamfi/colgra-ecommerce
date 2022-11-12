from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store import models

def add_to_cart(request):
    if request.method =='POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = models.Product.objects.get(id=prod_id)
            if product_check:
                if models.Cart.objects.filter(user=request.user.id, product_id=prod_id):
                    return JsonResponse({'status':"Item already in Cart"})
                else:
                    product_qty = int(request.POST.get('product_qty'))
                    if product_check.quantity >= product_qty:
                        models.Cart.objects.create(user=request.user, product_id=prod_id, product_qty=product_qty)
                        return JsonResponse({'status':"Product added to Cart"})
                    else:
                        return JsonResponse({'status':"Only " + str(product_check.quantity) + " of this product is available"})
            else:
                return JsonResponse({'status':"Something went wrong"})
        else:
            return JsonResponse({'status':"Login to continue"})
    return redirect('home')

@login_required(login_url='login')
def viewcart(request):
    cart = models.Cart.objects.filter(user=request.user)
    context = {'cart':cart}
    return render(request, 'store/layouts/cart.html', context)

def update_cart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if models.Cart.objects.filter(user=request.user, product_id=prod_id):
            product_qty = int(request.POST.get('product_qty'))
            cart = models.Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = product_qty
            cart.save()
            return JsonResponse({'status':'Item quantity updated'})
    return redirect('home')

def delete_cart_item(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if models.Cart.objects.filter(user=request.user, product_id=prod_id):
            cart_item = models.Cart.objects.get(product_id=prod_id, user=request.user)
            cart_item.delete()
        return JsonResponse({'status':'Item removed from cart'})
    return redirect('home')

