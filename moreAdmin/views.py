import datetime
from django.utils import timezone
from multiprocessing import context
from operator import countOf
import re
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import login , logout
from moreAdmin.models import Coupon, Myorders, Payment
from django.db.models import Count
from productmanagement.models import Stock
from moreAdmin.models import User
from django.db.models import Sum
from django.db.models.functions import TruncMonth

# Create your views here.
@never_cache
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect(dashboard)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(dashboard)
        else:
            messages.info(request,'invalid credentials')
            return redirect(admin_login)
    return render(request,'admin_login.html')

   
@never_cache
def dashboard(request):
    if request.user.is_authenticated and request.user.is_staff:
        product = Stock.objects.all()
        bb = Myorders.objects.all()
        revenue = 0
        for i in bb:
            revenue = revenue + int(i.amount)

        print(revenue)
        use = Stock.objects.count()
        ob = Myorders.objects.filter(orderstatus='deliverd').count()
        pending = Myorders.objects.filter(orderstatus='Placed').count() 
           
        
        order   = Myorders.objects.all()
        context={'product':product,'use':use,'ob':ob,'bb':bb,'pending':pending,'revenue':revenue}

        product = Stock.objects.all()
        ymax = timezone.now()
        ymin = (timezone.now() - datetime.timedelta(days=365))
        yearly = Myorders.objects.filter(orderdate__lte=ymax, orderdate__gte=ymin)
        mmax = timezone.now()
        mmin = (timezone.now() - datetime.timedelta(days=30))
        monthly = Myorders.objects.filter(orderdate__lte=mmax, orderdate__gte=mmin)
        ymax = timezone.now()
        ymin = (timezone.now() - datetime.timedelta(days=7))
        weekly = Myorders.objects.filter(orderdate__lte=ymax, orderdate__gte=ymin)
        a = []
        n = 1
        subm = timezone.now()
        n = 4
        for i in range(4):
            k = 0
            for i in monthly:
                if i.orderdate <= subm and i.orderdate >= (subm - datetime.timedelta(days=7)):
                    k += 1

            a.append({'name': 'week' + str(n), 'value': k})
            n -= 1
            subm = subm - datetime.timedelta(days=7)

        subw = timezone.now()
        n = 7
        b = []
        for i in range(7):
            k = 0
            for i in weekly:
                if i.orderdate <= subw and i.orderdate >= (subw - datetime.timedelta(days=1)):
                    k += 1
            b.append({'name': 'day' + str(n), 'value': k})
            n -= 1
            subw = subw - datetime.timedelta(days=1)
        monthly_sales = list(reversed(a))
        weekly_sales = list(reversed(b))
        user_count = User.objects.all().count()
        order_price = Payment.objects.all().aggregate(Sum('totalamount'))
        total_income = order_price['totalamount__sum']
        order_count = Myorders.objects.all().count()
        product_count = product.count()
        payment = Payment.objects.all()

        obje = Myorders.objects.filter(orderdate__year=2022)
        
        obje1 = Myorders.objects.values('orderdate','orderid','amount','orderstatus').annotate(month=TruncMonth('orderdate')).values('month','orderdate','orderid','amount','orderstatus').annotate(c=Count('id')).values('month','c','orderdate','orderid','amount','orderstatus')
        
        lol=[]
        for i in obje1:
            lol.append({'order_id':i['orderid'],'delivery_status':i['orderstatus'],'month':i['month'].month,'year':i['month'].year,'total_price':i['amount']})
            
        return render(request, 'admin_dashboard.html',
                    context={'monthly': monthly, 'yearly': yearly, 'monthly_sales': monthly_sales,
                            'weekly_sales': weekly_sales, 'user_count': user_count, 'total_income': total_income,
                            'order_count': order_count, 'product_count': product_count, 'payment': payment, 'lol':lol,'revenue':revenue,'product':product,'use':use,'ob':ob,'bb':bb,'pending':pending, })
        
        
    return redirect(admin_login)


def salesreport(request):
    product = Stock.objects.all()
    ymax = timezone.now()
    ymin = (timezone.now() - datetime.timedelta(days=365))
    yearly = Myorders.objects.filter(orderdate__lte=ymax, orderdate__gte=ymin)
    mmax = timezone.now()
    mmin = (timezone.now() - datetime.timedelta(days=30))
    monthly = Myorders.objects.filter(orderdate__lte=mmax, orderdate__gte=mmin)
    ymax = timezone.now()
    ymin = (timezone.now() - datetime.timedelta(days=7))
    weekly = Myorders.objects.filter(orderdate__lte=ymax, orderdate__gte=ymin)
    a = []
    n = 1
    subm = timezone.now()
    n = 4
    for i in range(4):
        k = 0
        for i in monthly:
            if i.orderdate <= subm and i.orderdate >= (subm - datetime.timedelta(days=7)):
                k += 1

        a.append({'name': 'week' + str(n), 'value': k})
        n -= 1
        subm = subm - datetime.timedelta(days=7)

    subw = timezone.now()
    n = 7
    b = []
    for i in range(7):
        k = 0
        for i in weekly:
            if i.orderdate <= subw and i.orderdate >= (subw - datetime.timedelta(days=1)):
                k += 1
        b.append({'name': 'day' + str(n), 'value': k})
        n -= 1
        subw = subw - datetime.timedelta(days=1)
    monthly_sales = list(reversed(a))
    weekly_sales = list(reversed(b))
    user_count = User.objects.all().count()
    order_price = Payment.objects.all().aggregate(Sum('totalamount'))
    total_income = order_price['totalamount__sum']
    order_count = Myorders.objects.all().count()
    product_count = product.count()
    payment = Payment.objects.all()

    obje = Myorders.objects.filter(orderdate__year=2022)
    
    obje1 = Myorders.objects.values('orderdate','orderid','amount','orderstatus').annotate(month=TruncMonth('orderdate')).values('month','orderdate','orderid','amount','orderstatus').annotate(c=Count('id')).values('month','c','orderdate','orderid','amount','orderstatus')
    
    lol=[]
    for i in obje1:
        lol.append({'order_id':i['orderid'],'delivery_status':i['orderstatus'],'month':i['month'].month,'year':i['month'].year,'total_price':i['amount']})
        
    return render(request, 'report.html',
                  context={'monthly': monthly, 'yearly': yearly, 'monthly_sales': monthly_sales,
                           'weekly_sales': weekly_sales, 'user_count': user_count, 'total_income': total_income,
                           'order_count': order_count, 'product_count': product_count, 'payment': payment, 'lol':lol})



def logout_admin(request):
    if request.user.is_authenticated and request.user.is_staff:
        logout(request)
    return redirect(admin_login)

  
def adminorder(request):
    if request.user.is_authenticated and request.user.is_staff:
        ob = Myorders.objects.all().order_by('-id')
        context={'ob':ob}
    
        return render(request,'adminorder.html', context)
    else:
        return redirect("/")

def cancelorderr(request,id):
    obj = Myorders.objects.values('status','orderstatus').get(id=id)
    
    if obj['orderstatus'] == 'pending':
        if obj['status']==True:
            try:
                Myorders.objects.filter(id=id).update(status=False)
            except:
                pass
            n='order cancelled'
            messages.info(request,n)
            return redirect(adminorder)
        else:
            return redirect(adminorder)

    else:
              
        return redirect(adminorder)



def orderstatus(request,id):
    ob = Myorders.objects.values('orderstatus','status').get(id=id)
    if ob['status']==True:
        if ob['orderstatus']=='Placed':
            Myorders.objects.filter(id=id).update(orderstatus='shipped')
            n= 'Status updated successfully to Shipped'
            messages.success(request,n)
            return redirect(adminorder)

        else:
            Myorders.objects.filter(id=id).update(orderstatus='deliverd')
            n= 'Status updated successfully to Delivered'
            messages.success(request,n)

            return redirect(adminorder)
    else:
        return redirect(adminorder)  


def couponmanagement(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method=='POST':
            name         = request.POST['name']
            couponcode   = request.POST['couponcode']
            validdate    = request.POST['validdate']
            minimumprice = request.POST['minimumprice']
            discount     = request.POST['discount']
            ins = Coupon(coupon_name = name,coupon_code=couponcode,validtill=validdate,minimum_price=minimumprice,discount=discount)
            ins.save()
            n = ' Coupon added'
            messages.success(request,n)
            return redirect(couponmanagement)

        coupon = Coupon.objects.all()
        context ={'coupon':coupon} 
        return render(request,'couponmanagement.html',context) 
    else:
        return redirect("/")


def deletecoupon(request,id):
    co = Coupon.objects.filter(id=id)
    co.delete()
    Coupon.objects.all()
    n = ' Coupon Deleted Successfully'
    messages.success(request,n)
    return redirect(couponmanagement)
  












