from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'original_price', 'selling_price']

class CustomUserAdmin(UserAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number']

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }))

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'product_qty']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'tracking_number', 'product', 'price', 'quantity']
    search_fields = ['tracking_number']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['fname', 'lname', 'tracking_number', 'phone', 'total_price', 'status', 'created_at']
    search_fields = ['tracking_number']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(models.Category)
admin.site.register(models.Payment)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.Wishlist)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.Comment)