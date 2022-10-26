from itertools import count
from multiprocessing import context
from operator import countOf
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from moreUser.views import user_login, usersignup
from .models import Cart, Guestcart, wishlist
from moreAdmin.models import User
from productmanagement.views import singleproduct, viewproduct
from productmanagement.models import Category, Stock
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.cache import never_cache




# Create your views here.
@never_cache
def viewcart(request):
    if request.user.is_authenticated and request.user.is_active:
        ob = Cart.objects.filter(userid=request.user.id).order_by('id')
        print(ob)
        onj = Category.objects.values('offers')
        print(onj)

        
        total=0
        for j in ob:
            
            total = total + j.amount
            
            t=total*100
        context={'total':total,'ob':ob}

        return render(request, 'mycart.html', context)
    else:
        
        if not request.session.session_key:
            request.session.create()
        request.session['guest_key']=request.session.session_key
        key = request.session['guest_key']
        print(request.session.session_key)
        
        ob = Guestcart.objects.filter(userreference=request.session.session_key)
        total=0
        for j in ob:
            
            total = total + j.amount
        context = {'total':total,'ob':ob}
        return render(request, 'mycart.html', context)
        
    

def removecart(request,id):
    if request.user.is_authenticated and request.user.is_active:

        o = Cart.objects.get(id=id)
        o.delete()
        n = 'Product Removed from cart'
        messages.info(request,n)
    else:
        ob = Guestcart.objects.get(id=id)
        ob.delete()
        n = 'Product Removed from cart'
        messages.info(request,n)
    
    return redirect(viewcart)

def dquantity(request):
    if request.user.is_authenticated and request.user.is_active:
        
        if request.method =="POST":
            id = request.POST['id']
            
            ob=Cart.objects.values('quantity').get(id=id)
            quantity = ob['quantity']
            if quantity >= 2:


                Cart.objects.filter(id=id).update(quantity=ob['quantity']-1)
            ob=Cart.objects.values('quantity').get(id=id)
            o=Cart.objects.values('quantity','price','amount').get(id=id)
            Cart.objects.filter(id=id).update(amount=o['price']*o['quantity'])

            Cart.objects.filter(id=id).update(amount=o['price']*o['quantity'])
            o=Cart.objects.values('quantity','price','amount').get(id=id)
            
            cart = Cart.objects.filter(userid=request.user)
            

            amount = o['amount']
            q =ob['quantity']
            total = 0
            for j in cart:
            
                total = total + j.amount
            return JsonResponse({'amount':amount,'q':q,'total':total})

    else:
        if request.method =="POST":
            id = request.POST['id']
            ob=Guestcart.objects.values('quantity').get(id=id)
            quantity = ob['quantity']
            if quantity >= 2:

                Guestcart.objects.filter(id=id).update(quantity=ob['quantity']-1)
            ob=Guestcart.objects.values('quantity').get(id=id)
            o=Guestcart.objects.values('quantity','price','amount').get(id=id)
            Guestcart.objects.filter(id=id).update(amount=o['price']*o['quantity'])

            Guestcart.objects.filter(id=id).update(amount=o['price']*o['quantity'])
            o=Guestcart.objects.values('quantity','price','amount').get(id=id)

            amount = o['amount']
            q =ob['quantity']

            cart = Guestcart.objects.filter(userreference=request.session.session_key)
            total = 0
            for j in cart:
            
                total = total + j.amount
            return JsonResponse({'amount':amount,'q':q,'total':total})
                
@csrf_exempt
def iquantity(request):
    if request.user.is_authenticated and request.user.is_active:
        if request.method =="POST":
            id = request.POST['id']
            ob=Cart.objects.values('quantity').get(id=id)

            Cart.objects.filter(id=id).update(quantity=ob['quantity']+1)
            ob=Cart.objects.values('quantity').get(id=id)
            o=Cart.objects.values('quantity','price','amount').get(id=id)

            Cart.objects.filter(id=id).update(amount=o['price']*o['quantity'])
            o=Cart.objects.values('quantity','price','amount').get(id=id)

            amount = o['amount']
            q =ob['quantity']
            cart = Cart.objects.filter(userid=request.user)
            total = 0
            for j in cart:
            
                total = total + j.amount

            
        return JsonResponse({'amount':amount,'q':q,'total':total})
    else:
        if request.method =="POST":
            id = request.POST['id']
            ob=Guestcart.objects.values('quantity').get(id=id)

            Guestcart.objects.filter(id=id).update(quantity=ob['quantity']+1)
            ob=Guestcart.objects.values('quantity').get(id=id)
            o=Guestcart.objects.values('quantity','price','amount').get(id=id)

            Guestcart.objects.filter(id=id).update(amount=o['price']*o['quantity'])
            o=Guestcart.objects.values('quantity','price','amount').get(id=id)

            amount = o['amount']
            q =ob['quantity']
            cart = Guestcart.objects.filter(userreference=request.session.session_key)
            total = 0
            for j in cart:
            
                total = total + j.amount
            
            
        return JsonResponse({'amount':amount,'q':q,'total':total})


def viewwishlist(request):
    if request.user.is_authenticated and request.user.is_active:
        wish = wishlist.objects.filter(user=request.user)
        context = {'wish':wish}
        return render(request,'mywishlist.html',context)
    return redirect(user_login)



def addwishlist(request,id):
    if request.user.is_authenticated and request.user.is_active:
        s = Stock.objects.all().get(id=id)
        w = wishlist.objects.all()
    
        if wishlist.objects.filter(productid=s ,user=request.user).exists():
            n='Added to Wishlist'
            messages.info(request,n)
            return redirect(viewproduct)
        else:
            add = wishlist(productname = s.name, user=request.user,productid=s, description = s.description, image = s.image1,price=s.price)

            add.save()
            n='Added to Wishlist'
            messages.info(request,n)
    else:
        return redirect(user_login)
    return redirect(viewproduct)

def removewishlist(request,id):
    w = wishlist.objects.get(id=id)
    w.delete()
    n = 'Product Removed from wishlist'
    messages.success(request,n)
    return redirect(viewwishlist)

    





    
