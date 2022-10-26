from django.db import models
from moreAdmin.models import User
from productmanagement.models import Stock

# Create your models here.
class Cart(models.Model):
    userid      = models.ForeignKey(User,on_delete= models.CASCADE,null=True)
    productid   = models.ForeignKey(Stock,on_delete= models.CASCADE)
    productname = models.CharField(max_length=200)
    price       = models.IntegerField(null=True)
    image       = models.ImageField(upload_to='pics')
    quantity    = models.IntegerField()
    amount      =models.IntegerField()

class Guestcart(models.Model):
    userreference      = models.CharField(max_length=200,null=True)
    productid          = models.ForeignKey(Stock,on_delete= models.CASCADE)
    productname        = models.CharField(max_length=200)
    price              = models.IntegerField(null=True)
    image              = models.ImageField(upload_to='pics')
    quantity           = models.IntegerField()
    amount             = models.IntegerField()

class wishlist(models.Model):
    user        = models.ForeignKey(User,on_delete= models.CASCADE,null=True)
    productid   = models.ForeignKey(Stock,on_delete= models.CASCADE)
    productname = models.CharField(max_length=200)
    price       = models.IntegerField(null=True)
    image       = models.ImageField(upload_to='pics')
    description = models.CharField(max_length=750)




