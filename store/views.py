from unicodedata import category, name
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from . import models

# Create your views here.

def home(request):
    trending_products = models.Product.objects.filter(trending=1)
    context = {'trending_products':trending_products}
    return render(request, 'store/index.html', context)

def about(request):
    return render(request, 'store/about.html')


def collections(request):
    category = models.Category.objects.filter(status=0)
    context = {'category':category}
    return render(request, "store/layouts/collections.html", context=context)


def collection_products(request, name):
    if models.Category.objects.filter(name=name, status=0):
        products = models.Product.objects.filter(category__name=name)
        category_name = models.Category.objects.filter(name=name).first()
        wishlisted = []
        for product in products:
            if models.Wishlist.objects.filter(product_id = product.id):
                wishlisted.append(product)
        context = {'collection_products':products, 'category_name':category_name, 'wishlisted':wishlisted, 'current_user':request.user}
        return render(request, 'store/products/index.html', context=context)
    else:
        messages.warning(request, "Link is broken")
        return reverse('collections')


def product_details(request, cat_name, prod_name, pk):
    if models.Category.objects.filter(name=cat_name, status=0):
        if models.Product.objects.filter(name=prod_name, status=0):
            product = models.Product.objects.filter(name=prod_name, status=0).first()
            comments = models.Comment.objects.filter(product_id=pk)
            user = request.user
            context = {'product':product, 'comments':comments, 'user':user}
        else:
            messages.error(request, 'Something went wrong')
            return reverse('collections')
    else:
        messages.error(request, "No such category found")
        return reverse('collections')
    return render(request, 'store/products/product_detail.html', context)


def product_list_ajax(request):
    products = models.Product.objects.filter(status=0).values_list('name', flat=True)
    product_list = list(products)

    return JsonResponse(product_list, safe=False)


def search_product(request):
    if request.method == 'POST':
        product_searched = request.POST.get('prod_search')
        if product_searched == "":
            return redirect(request.META.get('HTTP_REFERER')) 
        else:
            product = models.Product.objects.filter(name__contains=product_searched).first()

            if product:
                return redirect('collections/'+product.category.name+'/'+product.name+'/'+str(product.id))
            else:
                messages.info(request, "No product matched your search")
                return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))