from django.contrib import admin
from .models import Product

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id','product_name','product_desc','product_category','product_price']

# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ['product_id','username']