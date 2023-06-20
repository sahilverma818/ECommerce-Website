from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    product_id = models.CharField(max_length=10, primary_key=True)
    product_name = models.CharField(max_length=50, default = "Product Name Not Available")
    product_desc = models.CharField(max_length=200, default = "Product Description Not Available")
    product_category = models.CharField(max_length=50, default = "Product Category Not Available")
    product_price = models.FloatField(default = 0)


class Cart(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
   