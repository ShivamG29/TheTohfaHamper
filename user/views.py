from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import datetime
from django.db import connection
# Create your views here.
def home(request):

    cdata = category.objects.all().order_by('-id')[0:6]
    pdata = products.objects.all().order_by('-id')[0:12]
    noofitemsincart=addtocart.objects.all().count()
    return render(request, "user/index.html", {"data": cdata, "prod": pdata,"noofitemsincart":noofitemsincart})


def about(request):
    noofitemsincart = addtocart.objects.all().count()
    return render(request, "user/about.html",{"noofitemsincart":noofitemsincart})


def contactus(request):
    status = False
    noofitemsincart = addtocart.objects.all().count()
    if request.method == "POST":
        N = request.POST.get("name", "")
        M = request.POST.get("mobile", "")
        E = request.POST.get("email", "")
        Mes = request.POST.get("msg", "")
        res = contact(name=N, email=E, contact=M, message=Mes)
        res.save()
        status = True
        return HttpResponse("<script>alert('thanks for enquary....');window.location.href='/user/contactus/'</script>")
        noofitemsincart = addtocart.objects.all().count()

    return render(request, "user/contactus.html", {'S': status,"noofitemsincart":noofitemsincart})


def services(request):
    noofitemsincart = addtocart.objects.all().count()

    return render(request, "user/services.html",{"noofitemsincart":noofitemsincart})


def myorders(request):
    noofitemsincart = addtocart.objects.all().count()

    userid=request.session.get('userid')
    oid=request.GET.get('oid')
    orderdata=""
    if userid:
        cursor=connection.cursor()
        cursor.execute("select o.*,p.* from user_order o,user_products p where o.pid=p.id and o.userid='"+str(userid)+"'")
        orderdata=cursor.fetchall()
        if oid:
            #print(orderdata)
            result=order.objects.filter(id=oid,userid=userid)
            result.delete()
            return HttpResponse("<script>alert('Your Order Has Been Canceled....');window.location.href='/user/myorders/'</script>")

    return render(request, "user/myorders.html",{"pendingorder":orderdata,"noofitemsincart":noofitemsincart})


def myprofile(request):
    noofitemsincart = addtocart.objects.all().count()
    user = request.session.get('userid')
    pdata = profile.objects.filter(email=user)
    if user:
        if request.method == 'POST':
            name = request.POST.get("name", "")
            mobile = request.POST.get("mobile", "")
            password = request.POST.get("passwd", "")
            address = request.POST.get("address", "")
            picname = request.FILES['fu']
            profile(email=user,name=name,passwd=password,mobile=mobile,address=address,ppic=picname).save()
            return HttpResponse("<script>alert('Your Profile Updated Successfully....');window.location.href='/user/myprofile/'</script>")

    return render(request, "user/myprofile.html",{"profile":pdata,"noofitemsincart":noofitemsincart})


def prod(request):
    noofitemsincart = addtocart.objects.all().count()

    cdata=category.objects.all().order_by('-id')
    x=request.GET.get('abc')
    pdata=""
    if x is not None:
        pdata=products.objects.filter(category=x)
    else:
        pdata = products.objects.all().order_by('-id')
    return render(request, "user/products.html", {"cat": cdata, "products": pdata,"noofitemsincart":noofitemsincart})


def signup(request):
    noofitemsincart = addtocart.objects.all().count()

    if request.method == 'POST':
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        mobile = request.POST.get("mobile", "")
        password = request.POST.get("passwd", "")
        address = request.POST.get("address", "")
        picname = request.FILES['fu']
        d=profile.objects.filter(email=email)
        if d.count()>0:
            return HttpResponse("<script>alert('you are already register....');window.location.href='/user/signup/'</script>")
        else:
            profile(name=name, mobile=mobile, email=email, passwd=password, address=address, ppic=picname).save()
            return HttpResponse("<script>alert('you are register successfully....');window.location.href='/user/signup/'</script>")
    return render(request, "user/signup.html",{"noofitemsincart":noofitemsincart})


def signin(request):
    noofitemsincart = addtocart.objects.all().count()

    if request.method == 'POST':
        uname = request.POST.get('email', "")
        pwd = request.POST.get('password', "")
        checkuser = profile.objects.filter(email=uname, passwd=pwd)
        if (checkuser):
            request.session["userid"]=uname
            return HttpResponse("<script>alert('you are login successfully....');window.location.href='/user/signin/'</script>")
        else:
            return HttpResponse("<script>alert('please enter valid email & password....');window.location.href='/user/signin/'</script>")
    return render(request, 'user/signin.html',{"noofitemsincart":noofitemsincart})

def viewdetails(request):
    noofitemsincart = addtocart.objects.all().count()

    a=request.GET.get('msg')
    data=products.objects.filter(id=a)
    return render(request, "user/viewdetails.html",{"d":data,"noofitemsincart":noofitemsincart})

def process(request):
    noofitemsincart = addtocart.objects.all().count()

    userid=request.session.get('userid')
    pid=request.GET.get('pid')
    btn=request.GET.get('bn')
    print(userid,pid,btn)
    if userid is not None:
        if btn=='cart':
            checkcartitem=addtocart.objects.filter(pid=pid,userid=userid)
            #print(pid,checkcartitem.count())
            if checkcartitem.count()==0:
                addtocart(pid=pid,userid=userid,status=True,cdate=datetime.datetime.now()).save()
                return HttpResponse("<script>alert('This Item is successfully added in cart');window.location.href='/user/home/'</script>")

            else:
                return HttpResponse("<script>alert('This Item is Already Added To The Cart.....');window.location.href='/user/home/'</script>")
        elif btn=='order':
            order(pid=pid,userid=userid,remarks="pending",status=True,odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('your order is confirmed.....');window.location.href='/user/myorders/'</script>")


        elif btn=='orderfromcart':
            res=addtocart.objects.filter(pid=pid,userid=userid)
            res.delete()
            order(pid=pid,userid=userid,remarks="Pending",status=True,odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('your order is confirmed.....');window.location.href='/user/myorders/'</script>")
        return render(request, 'user/process.html', {"alreadylogin": True,"noofitemsincart":noofitemsincart})

    else:
        return HttpResponse("<script>window.location.href='/user/signin/'</script>")


def logout(request):
    del request.session['userid']
    return HttpResponse("<script>window.location.href='/user/home/'</script>")

def cart(request):
    noofitemsincart = addtocart.objects.all().count()

    cartdata=""
    if request.session.get('userid'):
        userid=request.session.get('userid')
        cursor=connection.cursor()
        cursor.execute("select c.*,p.* from user_addtocart c,user_products p where p.id=c.pid and userid='"+str(userid)+"'")
        cartdata=cursor.fetchall()

        pid=request.GET.get('pid')
        if request.GET.get('pid'):
            res=addtocart.objects.filter(id=pid,userid=userid)
            res.delete()
            return HttpResponse("<script>alert('your product has been removed successfully');window.location.href='/user/cart/'</script>")


    return render(request,'user/cart.html/',{"cart":cartdata,"noofitemsincart":noofitemsincart})