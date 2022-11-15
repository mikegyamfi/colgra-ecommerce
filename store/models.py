import email
from email.policy import default
from django.db import models
from django.forms import CharField
import datetime
import os
from .paystack import Paystack
from django.contrib.auth.models import AbstractUser


# Create your models here.


def get_file_path(request, filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join('uploads/', filename)

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=250, null=False, blank=False)
    last_name = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField(max_length=250, null=False, blank=False)
    password1 = models.CharField(max_length=250, null=False, blank=False)
    password2 = models.CharField(max_length=250, null=False, blank=False)
    phone_number = models.PositiveIntegerField(null=True, blank=False)

class Category(models.Model):
    slug = models.CharField(max_length=250, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=True)
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    description = models.TextField(max_length=600, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    meta_title = models.CharField(max_length=150, null=False, blank=False)
    meta_keywords = models.CharField(max_length=150, null=False, blank=False)
    meta_description = models.CharField(max_length=150, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False, blank=True)
    product_image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    description = models.TextField(max_length=600, null=False, blank=False)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    tag = models.CharField(max_length=150, null=False, blank=False)
    meta_title = models.CharField(max_length=150, null=False, blank=False)
    meta_keywords = models.CharField(max_length=150, null=False, blank=False)
    meta_description = models.CharField(max_length=150, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.PositiveIntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=400, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.user.username} - {self.comment_text}"


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=150, null=False)
    phone = models.PositiveIntegerField(null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    order_statuses = (
        ('Pending', 'Pending'),
        ('Out for Shipping', 'Out for Shipping'),
        ('Completed', 'Completed')
    )
    status = models.CharField(max_length=50, choices=order_statuses, default="Pending")
    message = models.TextField(null=True)
    tracking_number = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id} - {self.tracking_number} - {self.user} - {self.fname} - {self.lname}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    tracking_number = models.CharField(max_length=150, null=True)
    quantity = models.PositiveIntegerField(null=False)

    def __str__(self):
        return f"{self.order.id} - {self.order.tracking_number} - {self.order.user} - {self.order.fname} - {self.order.lname}"


class Payment(models.Model):
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment: {self.amount} - {self.ref} - {self.payment_date}"

    # def save(self, *args, **kwargs):
    #     while not self.ref:
    #         ref = secrets.token_urlsafe(10)
    #         object_with_similar_ref = Payment.objects.filter(ref=ref)
    #         if not object_with_similar_ref:
    #             self.ref = ref
    #     super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result["amount"] / 100 == self.amount:
                self.verified = True
            self.save()
            if self.verified:
                return True
            return False

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.PositiveIntegerField(null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
