from email.mime import image
from itertools import product
import re
from django.shortcuts import render , redirect
from django.contrib import messages
from cartmanagement.models import Cart, Guestcart
from moreAdmin.models import User
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from productmanagement.forms import StockForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from productmanagement.models import Banner, Category, Stock, Subcategory


# Create your views here.
def category(request):
    if request.method=='POST':
        categoryname = request.POST['categoryname']
        offers = request.POST['offers']
        if Category.objects.filter(categoryname=categoryname).exists():
            messages.warning(request,' Named category already found')
            return redirect(category)
        else:
            i = Category(categoryname = categoryname, offers = offers)
            i.save()
            n=' Category added'
            messages.success(request,n)

        return redirect(allcategory) 
    # return redirect('/')
    return render(request,'add_category.html')

def subcategory(request):
    ob = Category.objects.all()
    context={'ob':ob}
    

    if request.method=='POST':
        subcatname = request.POST['subcatname']
        category = request.POST['category']
        ins = Subcategory(subcatname=subcatname,category_id=category)
        ins.save()
        n = 'Subcategory added'
        messages.info(request,n)
        return redirect(allcategory)
    return render(request,'add_sub.html',context)


def addproduct(request):
    
    oj  = Category.objects.all()
    sub = Subcategory.objects.all()
    
    n = 'Add product'
    
    if 'cat' in request.GET:
        
        categ = request.GET['category']
        request.session['categ'] = categ
        sub = Subcategory.objects.filter(category=categ)
        request.session['cat']=True
        request.session['catname']=sub[0].category.categoryname
        
    if request.method=='POST':
        print(request.FILES.get('filename1'))
        name = request.POST['name']
        category = sub[0].category.id
        subcategory = request.POST['subcategory']
        price  = request.POST['price']
        stock = request.POST['stock']
        quantity = request.POST['quantity']
        description = request.POST['description']
        filename1 = request.FILES.get('filename1')
        filename2 = request.FILES.get('filename2')
        filename3 = request.FILES.get('filename3')
        filename4 = request.FILES.get('filename4')
        print(filename1)
        print(filename2)
        print(filename3)
        print(filename4)
        
        ins = Stock(name=name, price= price,category_id=category,subcatname_id=subcategory,stock=stock, quantity=quantity, description=description,image1=filename1,image2=filename2,image3=filename3,image4=filename4)
        ins.save()
        request.session['cat']=False
        
        print(ins.id)
        request.session['productid']=ins.id
        # return redirect(addImage)
        messages.warning(request,'Product added Successfully')
        return redirect(adminproduct)

    context={'oj':oj,'sub':sub, }

    return render(request,'add_products.html',context)

def addImage(request):
    ins=request.session['productid']
    pro = get_object_or_404(Stock, id=ins)
    if request.method=='POST':
        form = StockForm(request.POST,request.FILES, instance=pro)
        # for filename, file in request.FILES:

        print(request.FILES)

        if form.is_valid():
            form.save()
            
            messages.warning(request,'Product added Successfully')
            return redirect(adminproduct)

        
    else:
        form = StockForm()
    context ={'form':form}
    return render(request,'images.html', context)

def viewproduct(request):
    if request.user.is_authenticated and request.user.is_active:
    
        products = Stock.objects.all()
        product=[]
        
        for i in products:
            product.append({
                "id"    : i.id,
                "name"  : i.name,
                "price" : i.price,
                "quantity" : i.quantity,
                "stock"  : i.stock,
                "description":i.description,
                "image1"    : i.image1,
                "image2"    : i.image2,
                "image3"    : i.image3,
                "image4"    : i.image4,
                "proOffer"  : i.proOffer,
                "category"  : i.category.offers,
                "productOfferedPrice" :i.price -  i.price * (i.proOffer/100),
                "categoryOfferedPrice":i.price - i.price * (i.category.offers/100)
                
            })
           
        
        paginator = Paginator(product, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        ob = Stock.objects.values()
        cat = Category.objects.all()
        c = Cart.objects.filter(userid=request.user).count()
        name=request.GET.get('srch')
       
# ....SEARCH...................

        if request.method == 'GET' and name is not None:
            
            match = Stock.objects.values('name','price','quantity','image1','description','id','stock').annotate(search=SearchVector('name','description')).filter(search=name)
            c = Cart.objects.filter(userid=request.user).count()
                
            return render(request ,'products.html',{'match':match,'cat':cat,'c':c})

        context={'ob':ob,'cat':cat,'c':c,'users' : paged_products}
        return render(request,'products.html',context)


# ............GUEST USER..................
    else:
        
        products = Stock.objects.all()
        product=[]
        for i in products:
            product.append({
                "id"    : i.id,
                "name"  : i.name,
                "price" : i.price,
                "quantity" : i.quantity,
                "stock"  : i.stock,
                "description":i.description,
                "image1"    : i.image1,
                "image2"    : i.image2,
                "image3"    : i.image3,
                "image4"    : i.image4,
                "proOffer"  : i.proOffer,
                "category"  : i.category.offers,
                "productOfferedPrice" :i.price -  i.price * (i.proOffer/100),
                "categoryOfferedPrice":i.price - i.price * (i.category.offers/100)


            })
        paginator = Paginator(product, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        ob = Stock.objects.values()
        
        cat = Category.objects.all()
            
        name=request.GET.get('srch')
            
# ............SEARCH...................

        if request.method == 'GET' and name is not None:
            match = Stock.objects.values('name','price','quantity','image1','description','id','stock').annotate(search=SearchVector('name','description')).filter(search=name)
                
            return render(request ,'products.html',{'match':match,'cat':cat})

        context={'ob':ob,'cat':cat,'users' : paged_products}
        return render(request,'products.html',context)
    
    

def singleproduct(request,id):
    ob = Stock.objects.all().get(id=id)
    count = Stock.objects.all().filter(id=id).count()

    cat = Category.objects.values('offers').get(id=ob.category_id)
    pro = ob.proOffer
    c =cat['offers']
    if c >= pro:
        offeredprice = ob.price - (ob.price * cat['offers'])/100
        request.session['offer'] = offeredprice
    else:
        offeredprice = ob.price - (ob.price * pro)/100
        request.session['offer'] = offeredprice

    
    
    context = {'ob':ob,'offeredprice':offeredprice,'c':c,'pro':pro,'count':count}
    if request.method == 'POST':
        quantity = request.POST['quantity']
        request.session['quantity']=quantity
        if request.user.is_authenticated and request.user.is_active:
            ca= Cart.objects.filter(userid=request.user).count()

            p =  Stock.objects.all().get(id=id)
            u = User.objects.all().get(id=request.user.id)
            
            if Cart.objects.filter(productid=id,userid=request.user).exists():
                c = Cart.objects.get(productid_id=id,userid=request.user)
                c.productname = p.name
                
                c.productid = p
                c.userid= u
                c.quantity=c.quantity + int(quantity)
                c.image = p.image1
                c.amount=c.amount*int(quantity)
                c.save()
                n = 'Added to Cart'
                messages.info(request,n)
                
            else:
                offer =request.session['offer']
                t = Cart(productname = p.name, productid= p,userid = u,price=offer,quantity= quantity,image=p.image1)
                if int(quantity)>1:
                    t.amount=p.price*int(quantity)

                else:
                    t.amount = offer
                t.save()
                n = 'Added to Cart'
                messages.info(request,n)
        else:
            quantity = request.session['quantity']
            
            if not request.session.session_key:
                request.session.create()
            request.session['guest_key']=request.session.session_key
            key = request.session['guest_key']
            offer =request.session['offer']
            p =  Stock.objects.all().get(id=id)
            if Guestcart.objects.filter(productid_id=id,userreference=key).exists():
                g = Guestcart.objects.get(productid_id=id,userreference=key)
                
                g.quantity = g.quantity + int(quantity)
                g.save()
                n = 'Added to Cart'
                messages.info(request,n)
            else:

                t = Guestcart(productname = p.name,userreference=key, productid= p,price=offer,quantity= quantity,image=p.image1)
                if int(quantity)>1:
                    t.amount=p.price*int(quantity)

                else:
                    t.amount = offer
                t.save()
                n = 'Added to Cart'
                messages.info(request,n)
            

    return render(request,'singleproduct.html',context)

def adminproduct(request):
    if request.user.is_authenticated and request.user.is_staff:

        p = Stock.objects.all().order_by('id')
        context={'p':p}
        return render(request,'admin_products.html',context)
    else:
        return redirect("/")
    
def editproduct(request,id):
    if request.user.is_authenticated and request.user.is_staff:

        oj  = Category.objects.all()
        obj = Subcategory.objects.filter()
        n = 'Edit Product'
        pro  = Stock.objects.get(id = id)
        context={'oj':oj, 'obj':obj, 'n':n,'pro':pro}
        
        
        if request.method=='POST':
            pro         = Stock.objects.get(id = id)
            name        = request.POST['name']
            category    = request.POST['category']
            subcategory = request.POST['subcategory']
            price       = request.POST['price']
            stock       = request.POST['stock']
            quantity    = request.POST['quantity']
            description = request.POST['description']
            # filename1   = request.POST['filename1']
            # filename2   = request.POST['filename2']
            # filename3   = request.POST['filename3']
            # filename4   = request.POST['filename4']

            pro.name        = name
            
            pro.price       = price
            pro.stock       = stock
            pro.quantity    = quantity
            pro.description = description
            # pro.filename1   = filename1
            # pro.filename2   = filename2
            # pro.filename3   = filename3
            # pro.filename4   = filename4
            pro.save()
            n='Product Updated'
            messages.warning(request,n)
            return redirect(adminproduct)
        return render(request, 'editproduct.html',context)
    else:
        return redirect("/")
    

def removeproduct(request,id):
    
    o = Stock.objects.get(id=id)
    o.delete()
    n = 'Product Removed'
    messages.info(request,n)
    Stock.objects.all()
    
    return redirect(adminproduct)

def banner(request):
    if request.user.is_authenticated and request.user.is_staff:

        ob=Banner.objects.all()
        context={'ob':ob}
        return render(request,'banner.html',context)
    else:
        return redirect("/")

def addbanner(request):
    if request.user.is_authenticated and request.user.is_staff:

        if request.method=='POST':
            heading = request.POST['heading']
            filename= request.POST['filename']
            description = request.POST['description']
            ins = Banner(heading=heading,image=filename,description=description)
            ins.save()
            n = 'banner added'
            messages.warning(request,n)
            return redirect(banner)
        return render(request,'addbanner.html')
    else:
        return redirect("/")


def allcategory(request):
    if request.user.is_authenticated and request.user.is_staff:
        
        
        o = Category.objects.all().order_by('id')
        ob = Subcategory.objects.all().order_by('id')

        context={'o':o,'ob':ob}
        return render(request,'allcategory.html',context)
    else:
        return redirect("/")


def disablecategory(request,id):
    ob=Category.objects.get(id=id)
    
    ob.delete()
    n = 'Category Deleted Successfully'
    messages.info(request,n)
    return redirect(allcategory)

def deleSubcategory(request,id):
    o = Subcategory.objects.get(id=id)
    o.delete()
    n = 'Subcategory Deleted Successfully'
    messages.info(request,n)
    return redirect(allcategory)
    
    

def deletebanner(request,id):
    o = Banner.objects.get(id=id)
    o.delete()
    Banner.objects.all()
    return redirect(banner)


def filter(request,id):
    cat = Category.objects.all()
    cate = Category.objects.get(id=id)
    u = Stock.objects.filter(category=id)
    users=[]
    for i in u:
        users.append({
            "id"    : i.id,
            "name"  : i.name,
            "price" : i.price,
            "quantity" : i.quantity,
            "stock"  : i.stock,
            "description":i.description,
            "image1"    : i.image1,
            "image2"    : i.image1,
            "image3"    : i.image1,
            "image4"    : i.image1,
            "proOffer"  : i.proOffer,
            "offeredprice" :i.price -  i.price * (i.proOffer/100)
        })
    context = {'users':users,'cat':cat,'cate':cate}
    
    return render(request, 'products.html',context)

def editoffer(request,id):
    if request.method=='POST':
        offer = request.POST['offer']
        Category.objects.filter(id=id).update(offers=offer)
        n="offer updated"
        messages.warning(request,n)

        return redirect(offermanagement)
    return render(request,'editoffer.html')

def offermanagement(request):
    cat = Category.objects.all().order_by('id')
    product = Stock.objects.all().order_by('id')
    context = {'cat':cat,'product':product}
    return render(request,'offermanagement.html',context)

def editProOffer(request,id):
    if request.method == 'POST':
        offer = request.POST['offer']
        Stock.objects.filter(id=id).update(proOffer=offer)
        messages.info(request,'offer updated')
        return redirect(offermanagement)
    return render(request,'productoffer.html')

