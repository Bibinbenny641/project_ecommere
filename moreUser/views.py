

import email
from email.policy import EmailPolicy
from multiprocessing import context
from multiprocessing.connection import Client
from site import USER_BASE
from unittest import result
from cartmanagement.models import Cart, Guestcart
from morebuy.verify import check
from productmanagement.models import Banner
from twilio.rest import Client
from morebuy import verify
import random
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.shortcuts import render, redirect
from moreAdmin.models import Address, Myorders, User
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth import authenticate ,login , logout
from productmanagement.views import viewproduct
from django.views.decorators.cache import never_cache

# Create your views here.
#signup
def otp(request):
    
    if request.method =='POST':
        code = request.POST['otp']
        # user = User.objects.get(phone_no=phoneno) 
        print(code)
        phone=request.session['phoneno']
        k=verify.check(phone, code)
        print(k)
        if k:
            print('hhhhhhhhhhhhhhhhhhhhhhhhhhhh')
            User.objects.filter(phoneno=phone).update(active=True)
            return redirect(user_login)
        else:
            u = User.objects.filter(phoneno=phone)
            u.delete()
            messages.info(request,'sighnup failed pls retry')
            return redirect(usersignup)
          

    return render(request,'otp.html')


#-----------------login with otp verification ------------def otp(request):
def otp1(request): 
    if request.method =='POST':
        code = request.POST['otp']
        # user = User.objects.get(phone_no=phoneno) 
        print(code)
        phone=request.session['phoneno']
        k=verify.check(phone, code)
        print(k)
        if k:
            print('hhhhhhhhhhhhhhhhhhhhhhhhhhhh')
            try:

                user = User.objects.get(phoneno=phone)
                auth.login(request,user)
            except:
                return redirect(user_login)
            messages.info(request,'login success')
            return redirect(viewproduct)
        else:
            
            messages.info(request,'login failed')
            return redirect(user_login)
    return render(request,'otp.html')

@never_cache  
def user_login(request):
    if request.user.is_authenticated and request.user.is_active:
        return redirect(viewproduct)

    if request.method == 'POST':
        email = request.POST['email'] 
        password = request.POST['password']
        

        user = auth.authenticate(email=email,password=password)

        if user is not None and user.active==True:
            print(user.is_active)
            if 'guest_key' in request.session:
                p = request.session['guest_key']
                guest_cart = Guestcart.objects.filter(userreference=p)

                auth.login(request, user)
                for i in guest_cart:
                    try:
                        cart = Cart.objects.get(userid=request.user,productid=i.productid)
                        print(cart)
                    except:
                        cart = None
                    if cart:
                        Cart.objects.filter(userid=request.user, productid=i.productid).update(quantity = cart.quantity+i.quantity)
                    else:
                        k = Cart(userid=request.user,productid=i.productid,quantity=i.quantity,amount=i.amount,price=i.price,productname=i.productname,image=i.image)
                        k.save()

            auth.login(request, user)
            
            n= 'login Successfuly'
            messages.success(request,n)
            return redirect(viewproduct)
        else:
            n = 'invalid credentials'
            messages.success(request,n)
            return redirect(user_login)

    return render(request, 'user_login.html')


def usersignup(request):
    if request.method =='POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        phoneno = request.POST['phoneno']
        # num1 = random.randint(1000, 9999)
        # print(num1)
        # account_sid = 'ACa07e119377124b5372c3aba9aa6c3f8d'
        # auth_token = '5b0acf72a30eaf5f29581fd62ec8dfb2'
        # client = Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        # message = client.messages.create(
        #     body='otp : ' + str(num1),
        #     from_='[+][1][8597651446]',
        #     to='[+][91]'+str([phoneno])
        # )
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1!=password2:
            messages.error(request,('password did no match'))
            return redirect(usersignup)
        # for i in username: 
        #     if i == " ":
        if fullname.isspace():
            messages.error(request,('Name should not contain spaces'))
            return redirect(usersignup)

        if email.isspace():
            messages.error(request,('username should not contain spaces'))
            return redirect(usersignup)
        if  len(phoneno)!= 10 :
            messages.error(request,'Phone number must contain 10 numbers')
            return redirect(usersignup)
        if User.objects.filter(phoneno=phoneno).exists():
            messages.info(request,'phone no already taken')
            return redirect(usersignup)

        elif User.objects.filter(email=email).exists():
            messages.info(request,'email taken')
            return redirect(usersignup)
        else:
            
            # print(num1)
            # print(phoneno)
            request.session['phoneno']=phoneno
            phone=phoneno
            print(phone)
            verify.send(phone)
            
            user = User.objects.create_user(fullname = fullname,  email=email, phoneno = phoneno, password=password1)

            user.save()
            
            return redirect(otp)
    return render(request, 'user_signup.html')


def home(request):

    ob = Banner.objects.values()
    context={'ob':ob}
    return render(request,'home.html',context)

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        n = 'Logout Successfully'
        messages.info(request,n)
    return redirect(user_login)

   

def myprofile(request):
    if request.user.is_authenticated and request.user.is_active:
        ob=User.objects.all().get(id=request.user.id)
        o =Address.objects.filter(user_id=request.user)
        context={'ob':ob,'o':o}
        return render(request,'myprofile.html',context)
    return redirect(user_login)

def editprofile(request):
    ob = User.objects.filter(id=request.user.id)
    if request.method=='POST':
        name        = request.POST['name']
        if name.isspace():
            
            messages.error(request,('Name should not contain spaces'))
            return redirect(editprofile)
        if  name.isnumeric():
            messages.error(request,('Name should not contain Numbers'))
            return redirect(editprofile)

        User.objects.filter(id=request.user.id).update(fullname=name)
        return redirect(myprofile)

    return render(request,'editprofile.html')

def address(request):
    
    if request.method=='POST':
        housename=request.POST['housename']
        city     =request.POST['city']
        district =request.POST['district']
        zipcode  =request.POST['zipcode']
        if housename.isspace():
            
            messages.error(request,('Housename should not contain spaces'))
            return redirect(address)
        if housename.isnumeric():
                messages.error(request,('Housename should not contain Numbers'))
                return redirect(address)

        if city.isspace():
            messages.error(request,('Cityname should not contain spaces'))
            return redirect(address)
        if housename.isnumeric():
            messages.error(request,('City should not contain Numbers'))
            return redirect(address)
        if district.isspace():
            messages.error(request,('Districtname should not contain spaces'))
            return redirect(address)
        if  district.isnumeric():
            messages.error(request,('District should not contain Numbers'))
            return redirect(address)
        if zipcode.isspace():
            messages.error(request,('Name should not contain spaces'))
            return redirect(address)
        else:

            ins = Address(user=request.user,housename=housename, city1=city, district1=district, zipcode1=zipcode )
            ins.save()
            return redirect(myprofile)
    return render(request,'address.html')

def changepassword(request):
    if request.user.is_authenticated and request.user.is_active:

        if request.method=='POST':
            password1    = request.POST['password1']
            newpassword1 = request.POST['newpassword1']
            newpassword2 = request.POST['newpassword2']
            if newpassword1.isspace():
                messages.error(request,('Password should not contain spaces'))
                return redirect(changepassword)
            
            o = check_password(password1,request.user.password)
            if o:
                if newpassword1 == newpassword2:
                    user = User.objects.get(id=request.user.id)
                    user.set_password(newpassword1)
                    user.save()

                    messages.success(request,('password changed'))
                    return redirect(user_login)
                else:
                    messages.error(request,('password did not match'))
                    return redirect(changepassword)
            else:
                messages.error(request,('old password is wrong'))
                return redirect(changepassword)

    else:
        return redirect("/")
           
    return render(request,'password.html')

def deleteaddress(request,id):
    dele = Address.objects.filter(id=id)
    dele.delete()

    return redirect(myprofile)


def otplogin(request):
    if request.method =='POST':
        phoneno = request.POST['phoneno']
        request.session['phoneno']=phoneno
        h = request.session['phoneno']
        phone=phoneno
        print(phone)
        verify.send(phone)
        return redirect(otp1)
    return render(request,'loginotp.html')