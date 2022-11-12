from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store import models

@login_required(login_url='login')
def index(request):
    wishlist_items = models.Wishlist.objects.filter(user=request.user)
    context = {'wishlist':wishlist_items}
    return render(request, 'store/layouts/wishlist.html', context)

def add_to_wishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            if models.Product.objects.get(id=prod_id):
                if models.Wishlist.objects.filter(product_id=prod_id, user=request.user):
                    return JsonResponse({'status':'Item already in your wishlist'})
                else:
                    wishlist_item = models.Wishlist.objects.create(user=request.user, product_id=prod_id)
                    wishlist_item.save()
                    return JsonResponse({'status':'Item added to wishlist'})
            else:
                return JsonResponse({'status':'No such product found'})
        else:
            return JsonResponse({'status':'Log in to continue'})
    return redirect('home')

def delete_wishlist_item(request):
    if request.method == 'POST':
        prod_id = request.POST.get('product_id')
        if request.user.is_authenticated:
            if models.Wishlist.objects.filter(user=request.user, product_id=prod_id):
                item = models.Wishlist.objects.get(product_id=prod_id)
                item.delete()
                return JsonResponse({'status':'Item removed from wishlist'})
            else:
                return JsonResponse({'status':'No such product found'})
        else:
            return JsonResponse({'status':'Log in to continue'})
    return redirect('home')
