import datetime
from django.db import models
from django.contrib.auth.models import User
# from django import forms


class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Posted_Images')

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100,default='Coffee Table')

    def __str__(self):
     	return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=100,default='Table')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subimage = models.ForeignKey(Image, on_delete=models.SET_NULL,null=True,  default=None)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(null=True,unique=True)
    size_spec = models.TextField(null=True,unique=True)
    price = models.DecimalField(max_digits=4,decimal_places=0,default=0)
    quantity = models.IntegerField(null=True)    
    proimage = models.ForeignKey(Image, on_delete=models.SET_NULL,null=True,  default=None)
    created_time = models.DateTimeField(auto_now_add=True,null=True)
    count_in_stock = models.PositiveIntegerField(blank=True, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True,  default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
     	return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    taxPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.createdAt)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.address)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.rating)