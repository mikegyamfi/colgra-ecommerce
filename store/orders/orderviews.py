from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store import models

def index(request):
    orders = models.Order.objects.filter(user=request.user)
    context = {'orders':orders}
    return render(request, 'store/layouts/order-page.html', context)

def view_order(request, t_no):
    order = models.Order.objects.filter(tracking_number=t_no).filter(user=request.user).first()
    order_items = models.OrderItem.objects.filter(order=order)
    context = {'order_items':order_items, 'order':order}
    return render(request, 'store/layouts/view-order.html', context)