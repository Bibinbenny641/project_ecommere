
from email.policy import default
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.db import models


# Create your models here.
class Category(models.Model):
    categoryname = models.CharField(max_length=100)
    offers       = models.IntegerField()
    status    = models.BooleanField(default=True)
    
class Subcategory(models.Model):
    subcatname   = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    status    = models.BooleanField(default=True)


class Stock(models.Model):
    
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.CharField(max_length=10)
    stock = models.IntegerField()
    description = models.CharField(max_length=600)
    image1 = models.ImageField(upload_to='pics/')
    image2 = models.ImageField(upload_to='pics/')
    image3 = models.ImageField(upload_to='pics/')
    image4 = models.ImageField(upload_to='pics/')
    category = models.ForeignKey(Category,on_delete= models.CASCADE)
    subcatname= models.ForeignKey(Subcategory, on_delete= models.CASCADE)
    proOffer  = models.IntegerField(default=5)
    

class Banner(models.Model):
    heading = models.CharField(max_length=50)
    image   = models.ImageField(upload_to='')
    description = models.CharField(max_length=300)


