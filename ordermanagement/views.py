from datetime import datetime
from genericpath import exists
from itertools import product
import json

from django.contrib import messages
from django.shortcuts import render, redirect
from cartmanagement.models import Cart
from moreAdmin.views import adminorder
from moreAdmin.models import Address, Coupon, Myorders, Payment
from cartmanagement.views import viewcart
from moreUser.views import user_login, usersignup
from productmanagement.models import Stock
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.views.decorators.cache import never_cache
from django.http import JsonResponse


@never_cache
def checkout(request):
    
    if request.user.is_authenticated and request.user.is_active:
        print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
        try:
            cart2 = Cart.objects.filter(userid=request.user.id)
            print(cart2)
        except:
            cart2= None

        
        try:
            print('GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG')
            cart = Cart.objects.get(userid=request.user.id)
            print('heloooooooooooooooooo')
            print(cart)
        except:
            cart = None

        print(cart)
        if not cart2 and cart is None:
            return redirect(viewcart)
        

        add = Address.objects.filter(user=request.user)
        ob = Cart.objects.values().filter(userid=request.user.id)
        total=0
        for j in ob:
            
            total = total + j['amount']

            m = total*100
        
        request.session['t']=total
        ord2 = str(datetime.now())+str(request.user.id)
        ord1 = ord2.translate({ord(':'): None,ord('-'): None, ord(' '): None, ord('.'): None})
        request.session['neworderid'] = ord1

        now = datetime.now()

        # coupons
        if 'coupons' in request.GET:
            code = request.GET['coupon']

            try:
                coup = Coupon.objects.get(coupon_code=code,added_date__lt=now,validtill__gt=now,minimum_price__lt=total )
                
                request.session['coupon_offer'] = coup.discount
                request.session['coupon_code'] = coup.coupon_code
                if request.session['coupon_offer'] is not None :
                    total = total-(total*request.session['coupon_offer'])/100

            except Coupon.DoesNotExist:
                return redirect(checkout)

        if request.method=='POST':

            Name     = request.POST['name']
            address  = request.POST['address']
            method   = request.POST['method']
            y = Address.objects.get(id=address)

            for i in ob:
                obj = Stock.objects.get(id=i['productid_id'])
                if obj.stock >= i['quantity']:

                    s = Myorders(userid =request.user,name=Name, address=y,method=method,productid=obj,orderid=ord1,productname=i['productname'],amount=i['price'],quantity=i['quantity'],image=i['image'],totalamount=i['amount'])
                    s.save()
                    Stock.objects.filter(id=i['productid_id']).update(stock=(obj.stock-i['quantity']))

                else:
                    messages.warning(request,' PRODUCT OUT OF STOCK')
                    return redirect(checkout)
                
                
                
                
            if request.POST['method']=='razorpay':

                amount = m
                order_currency = 'INR'
                client = razorpay.Client(
                        auth=("rzp_test_Nf4iy5nJpLvtmt", "Y2D6cZPsAz452WAVT8VpDTM1")
                        )
                payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': 0})
                payment_id = payment['id']
                request.session['payment']= payment
                payment_status = payment['status']
                
                if payment_status == 'created':
                    return render(request, "razorpay.html", {'payment': payment, 'm' : amount, "ob":ob, "total":total,'ord1':ord1 })
                # return render(request, "razorpay.html")

                return redirect(checkout)
                
            elif request.POST['method']=='paypal':
                orderid = request.session['neworderid']
                context= {'total':total,'orderid':orderid,'ob':ob,'m':m,'ord1':ord1 }
                de = Cart.objects.filter(userid=request.user.id)
                de.delete()
                return render(request,'paypal.html', context)
                    
            else:
                de = Cart.objects.filter(userid=request.user.id)
                de.delete()
                return render(request,'ordersuccess.html')

        return render(request,'checkout.html',{'ob':ob, 'm':m, 'total':total, 'add':add})
    else:
        return redirect(user_login)

def myorder(request):
    if request.user.is_authenticated and request.user.is_active:

        ob = Myorders.objects.filter(userid=request.user.id).order_by('-id')
        
        context = {'ob':ob}
        return render(request, 'myorder.html',context)
    else:
        return redirect(user_login)


def cancelorder(request,id):
    obj = Myorders.objects.values('status','orderstatus').get(id=id)
   
    if obj['orderstatus']=='Placed':
        if obj['status']==True:
            Myorders.objects.filter(id=id).update(status=False)
            
            n='order cancelled'
            messages.info(request,n)
            return redirect(myorder)
        else:
            return redirect(myorder)
    else:
        
        return redirect(myorder)


@csrf_exempt
def success(request):
    if request.user.is_authenticated and request.user.is_active:

        response=request.POST
        order_ins = Myorders.objects.values('orderid').filter(userid_id=request.user)
        
        total = request.session['t']
        neworderid = request.session['neworderid']
        
        params_dict = {
            'razorpay_payment_id' : response['razorpay_payment_id'],
            'razorpay_order_id' : response['razorpay_order_id'],
            'razorpay_signature' : response['razorpay_signature']
        }
        
        
        ins = Payment(user=request.user, paymentid=params_dict["razorpay_payment_id"], paymentmethod='razor', totalamount=total,status='paid',
                    orderid=neworderid)
        ins.save()
        pay = Payment.objects.filter(orderid=request.user)

        client = razorpay.Client(auth=("rzp_test_Nf4iy5nJpLvtmt", "Y2D6cZPsAz452WAVT8VpDTM1"))
        de = Cart.objects.filter(userid=request.user.id)
        de.delete() 
        try:
            client.utility.verify_payment_signature(params_dict)

            return render(request, 'ordersuccess.html')
        except:
            return render(request, 'ordersuccess.html')
    


def paypal(request):
    if request.user.is_authenticated and request.user.is_active:

        return render(request,'paypal.html')


def success1(request):
    if request.user.is_authenticated and request.user.is_active:

        return render(request,'success1.html')


def payments(request):
    if request.user.is_authenticated and request.user.is_active:


        body = json.loads(request.body)
        
        request.session['body']=body
        total = request.session['t']
        neworderid = request.session['neworderid']
        pay = Payment(user = request.user, paymentid= body['paypal_transaction_id'], paymentmethod='PayPal',totalamount=total,status='Paid', orderid = neworderid )
        pay.save()

        data = {
            'order_number': body['orderID'],
            'transID': body['paypal_transaction_id'],
        }
        return JsonResponse(data)


