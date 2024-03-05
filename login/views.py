
import sys
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login
sys.path.append("..")
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from adduser.models import AdminUsers
from product.models import Products
from payedProducts.models import PayedProducts
# Create your views here.


def getUser(name):
    user = None
    try:
        user = AdminUsers.objects.get(name=name)
    except AdminUsers.DoesNotExist:
        user = "NotFoundUser"
    return user


from datetime import datetime, timedelta


def payedmonyandincome():
    today = datetime.now()
    yesterday = datetime.date(today - timedelta(days=1))
    last_d_filter = datetime.date(today)
    saleses = PayedProducts.objects.filter(
        date__gte=last_d_filter)
    monysave = 0
    income = 0

    for sales in saleses:
        prodids = sales.productID.split(",")[1:]
        totals = sales.total.split(",")[1:]
        prices = sales.price.split(",")[1:]
        counts = sales.count.split(",")[1:]
        for e, i in enumerate(prodids):
            total = float(totals[e])
            monysave += total
            prod = 0
            try:
                prod = Products.objects.get(
                    id=int(i)).bougthprice
            except Products.DoesNotExist:
                pass
            income += round((float(prices[e]) -
                             float(prod)) * int(counts[e]), 3)

    return (round(monysave, 3), income)


def home(request):
    allprods = Products.objects.all()
    alerts = 0
    for prod in allprods:
        mincount = prod.minconut
        rcount = prod.realcount
        if mincount >= rcount:
            alerts = alerts + 1
    ms, inc = payedmonyandincome()
    print(make_password('123456'))
    if(request.session['id'] != None and request.session['name'] != None):
        return render(request, "index.html", {"session": request.session, "allprods": allprods, "alerts": alerts, "monys": ms, "inc": inc})
    else:
        return redirect("/login")


@csrf_protect
def login(request):
    if request.method == "POST":
        name = request.POST["username"]
        password = request.POST["password"]
        user = getUser(name)
        if user == "NotFoundUser" or (check_password(password, encoded=user.password) == False):
            return render(request, "login.html", {
                "LoginError": "Username Or Email Note Found"})
        request.session["id"] = user.id
        request.session["name"] = user.name
        request.session["permissions"] = user.premission
        request.session["userImgae"] = str(
            user.userImgae).replace("uploads/", "")
        request.session["dataCreated"] = str(user.dataCreated)
        request.session["loginTime"] = str(datetime.now())
        return render(request, "index.html", {"session": request.session})
    elif request.method == "GET":
        try:
            if(request.session['id'] != None and request.session['name'] != None):
                return redirect("/home")
        except:
            pass
        return render(request, "login.html", {})


def logOut(request):
    request.session.clear()
    request.session.clear_expired()
    request.COOKIES.clear()
    request.session["id"] = None
    request.session["name"] = None
    return redirect("/")
