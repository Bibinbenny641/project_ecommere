# from curses import noraw
# from locale import normalize

from unicodedata import name
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from productmanagement.models import Stock

# Create your models here.

class UserManager(BaseUserManager):
    def create_user (self,fullname,phoneno,email,password=None, is_staff=False, is_active=False, is_admin=False):
        if not email:
            raise ValueError('user must have an email address')
        if not password:
            raise ValueError('user must have password')
        
        user_obj = self.model(email = self.normalize_email(email))
        user_obj.fullname = fullname
        user_obj.phoneno = phoneno
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self,email,password=None):
        user = self.create_user(email,password=password,is_staff=True,is_admin=True,is_active=True)
        return user

    def create_superuser(self,email,password=None):
        user = self.create_user(email,email,password=password,is_staff=True,is_active=True)
        return user


class User(AbstractBaseUser):
    fullname = models.CharField(max_length=200,blank=True,null=True)
    phoneno = models.CharField(max_length=10,null=True,unique=True)
    email =models.EmailField(max_length=100,unique=True)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    def is_admin(self):
        return self.admin

    def is_active(self):
        return self.active

class Address(models.Model):
    user      = models.ForeignKey(User,on_delete=models.CASCADE)
    housename = models.CharField(max_length=100,default=None)
    city1      = models.CharField(max_length=100,default=None)
    district1  = models.CharField(max_length=100,default=None)
    zipcode1   = models.IntegerField()
    


class Myorders(models.Model):
    productid = models.ForeignKey(Stock,on_delete= models.CASCADE)
    userid    = models.ForeignKey(User,on_delete=models.CASCADE)
    address   = models.ForeignKey(Address,on_delete=models.CASCADE)
    name      = models.CharField(max_length=100)
    quantity  = models.IntegerField()
    amount    = models.CharField(max_length=10)
    method    = models.CharField(max_length=20)
    productname=models.CharField(max_length=100)
    image     = models.ImageField(upload_to='')
    status    = models.BooleanField(default=True)
    totalamount=models.IntegerField()
    orderid   = models.CharField(max_length=150,default=1)
    orderdate = models.DateTimeField(auto_now_add=True, null=True)
    orderstatus=models.CharField(max_length=50,default='Placed')

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paymentid= models.CharField(max_length=150)
    paymentmethod = models.CharField(max_length=100)
    totalamount   = models.IntegerField()
    status        = models.CharField(max_length=100,default='True',null=True)
    orderid       = models.CharField(max_length=150)
    
class Coupon(models.Model):
    coupon_name   = models.CharField(max_length=150)
    coupon_code   = models.CharField(max_length=150)
    added_date    = models.DateTimeField(auto_now_add=True, null=True)
    validtill     = models.DateTimeField()
    minimum_price = models.IntegerField()
    discount      = models.IntegerField()
    


