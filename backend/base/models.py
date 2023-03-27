from django.db import models
from django.contrib.auth.models import User
import os
import random
from django.utils import timezone


def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

def upload_image_path(instance, filename):
	new_filename = random.randint(1, 2541781232)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
	return "img/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)
    
class Product(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    brand=models.CharField(max_length=200,null=True,blank=True)
    category=models.CharField(max_length=200,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    rating=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    numReviews=models.IntegerField(null=True,blank=True,default=0)
    price=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    countInStock=models.IntegerField(null=True,blank=True,default=0)
    createdAt=models.DateTimeField(auto_now_add=True)
    createdAt=models.DateTimeField(auto_now_add=True)
    download = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    _id=models.AutoField(primary_key=True,editable=False)

    def __str__(self):
        return self.name

class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    rating=models.IntegerField(null=True,blank=True,default=0)
    comment=models.TextField(null=True,blank=True)
    _id=models.AutoField(primary_key=True,editable=False)

    def __str__(self):
        return str(self.rating)


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    paymentMethod=models.CharField(max_length=200,null=True,blank=True)
    taxPrice=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    totalPrice=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    createdAt=models.DateTimeField(auto_now_add=True)
    _id=models.AutoField(primary_key=True,editable=False)
    
    
    def __str__(self):
        return str(self.createdAt)


class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    qty=models.IntegerField(null=True,blank=True,default=0)
    price=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    _id=models.AutoField(primary_key=True,editable=False)

        
    def __str__(self):
        return self.name

class OrderCheckout(models.Model):
    order=models.OneToOneField(Order,on_delete=models.CASCADE,null=True,blank=True)
    purchaseBy=models.CharField(max_length=200,null=True,blank=True)
    dateofPurchase=models.DateTimeField(auto_now_add=False,null=True,blank=True)
    purchasePrice=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    purchasedGame = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    _id=models.AutoField(primary_key=True,editable=False)

    def __str__(self):
        return self.purchaseBy
    
    # class User(models.Model):
        # created_at = models.DateTimeField(auto_now_add=True)
    
# class UserProfile(models.Model):
#         user = models.OneToOneField(User, on_delete=models.CASCADE)
#         username = models.CharField(max_length=255, default='')
#         email = models.CharField(max_length=255, default='')
#         first_name = models.CharField(max_length=255, default='')
#         last_name = models.CharField(max_length=255, default='')
#         phone = models.CharField(max_length=20, default='')
#         city = models.CharField(max_length=20, default='')

#         def __str__(self):
#              return self.first_name

class User(models.Model):
    username = models.CharField(max_length=30, unique=True,default='')
    email = models.EmailField(max_length=255, unique=True, default='')
    password = models.CharField(max_length=255, default='')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.CharField(max_length=30, default=timezone.now)


    def __str__(self):
        return self.username