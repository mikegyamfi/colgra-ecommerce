from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store import models

def add_to_comments(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            comment_text = request.POST.get('comment_text')
            comment = models.Comment.objects.create(user=request.user, product_id=prod_id, comment_text=comment_text)
            comment.save()
            return JsonResponse({'status':"Thanks for the review."})
        else:
            return JsonResponse({'status':"Log in to write a review."})
    return redirect('home')


def delete_comment(request):
     if request.method == 'POST':
        comment_id = int(request.POST.get('comment_id'))
        print(comment_id)
        if request.user.is_authenticated:
            if models.Comment.objects.filter(user=request.user, id=comment_id):
                item = models.Comment.objects.get(id=comment_id)
                item.delete()
                return JsonResponse({'status':'Comment deleted'})
            else:
                return JsonResponse({'status':'No such product found'})
        else:
            return JsonResponse({'status':'Log in to continue'})
    

