from datetime import datetime, timedelta, date
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http.request import HttpRequest
from .models import PayedProducts
from product.models import Products
from adduser.models import AdminUsers
import random
from helpers.functions import checkAccsess
from django.utils import timezone
import json

# Create your views here.


def addpayedprod(request: HttpRequest):

    if request.method == "POST":
        postDate = request.POST
        print(postDate['data'])
        postDate = json.loads(postDate['data'])
        prods = postDate[0: -2]
        total = postDate[-2]
        discound = postDate[-1]
        opn = int(random.randint(0, 1000) * datetime.now().timestamp())
        pyp: PayedProducts = PayedProducts()
        for i in prods:
            prod: Products = Products.objects.get(id=int(i['id']))
            prod.realcount = prod.realcount - int(i['count'])
            prod.recpry = prod.bougthprice * prod.realcount
            prod.save()
            pyp.id = int(opn + datetime.now().timestamp())
            pyp.opNum = opn
            pyp.productID = pyp.productID + "," + i['id']
            pyp.price = str(str(pyp.price) + "," + str(i['price']))
            pyp.discound = float(discound)
            pyp.total = str(pyp.total) + "," + \
                str(float(prod.payprice) * float(i['count']))
            pyp.count = str(pyp.count) + "," + str(i['count'])
            pyp.lastTotal = float(total)
            pyp.payeduser = request.session['id']
        pyp.save()
        return JsonResponse({"error": False, "succsessText": "تمت العملية بنجاح", "print": True, "opn": opn, "payeduser": request.session['id'], "reload": True})
    else:
        return redirect("/")


def getAllSales(request: HttpRequest):

    if checkAccsess(request) == False:
        return redirect("/")
    today = datetime.now()
    yesterday = datetime.date(today - timedelta(days=1))
    last_d_filter = datetime.date(today)
    if request.method == "POST":
        saleses: PayedProducts = PayedProducts.objects.all()
        resspons = []
        for sales in saleses:
            user = ""
            try:
                user = AdminUsers.objects.get(id=int(sales.payeduser)).name
            except AdminUsers.DoesNotExist:
                user = "Defualt"

            try:
                prodobj = {
                    "id": sales.id,
                    "code": sales.opNum,
                    "date": sales.date,
                    "puser": user,
                    "discound": sales.discound,
                    "total": sales.lastTotal - sales.discound,
                    "options": f"""

                        <div class="row">
                            <div class='col-12 col-lg-12'>
                                <a style='width:100%'  href="/editpayedprod/{sales.id}" class="btn btn-primary">
                                    تعديل
                                </a>
                            </div>
                        </div>
                    
                    """
                }
            except Products.DoesNotExist:
                pass
            resspons.append(prodobj)
        return JsonResponse({"data": resspons}, safe=False)

    return render(request, "allsales.html", {"title": "All Sales", "session": request.session})


def is_leap_year(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def get_lapse():
    last_month = datetime.today().month
    current_year = datetime.today().year

    # is last month a month with 30 days?
    if last_month in [9, 4, 6, 11]:
        lapse = 30

    # is last month a month with 31 days?
    elif last_month in [1, 3, 5, 7, 8, 10, 12]:
        lapse = 31

    # is last month February?
    else:
        if is_leap_year(current_year):
            lapse = 29
        else:
            lapse = 30

    return lapse


def getMonth(request: HttpRequest):

    if checkAccsess(request) == False:
        return redirect("/")
    month_filter = date.today().replace(
        year=date.today().year, month=date.today().month, day=1)
    if request.method == "POST":
        saleses: PayedProducts = PayedProducts.objects.filter(
            date__gte=month_filter)
        resspons = []
        for sales in saleses:
            user = ""
            try:
                user = AdminUsers.objects.get(id=int(sales.payeduser)).name
            except AdminUsers.DoesNotExist:
                user = "Defualt"
            prodobj = {}
            try:
                prodobj = {
                    "id": sales.id,
                    "code": sales.opNum,
                    "date": sales.date,
                    "puser": user,
                    "discound": sales.discound,
                    "total": sales.lastTotal - sales.discound,
                    "options": f"""

                        <div class="row">
                            <div class='col-12 col-lg-12'>
                                <a style='width:100%'  href="/editpayedprod/{sales.id}" class="btn btn-primary">
                                    تعديل
                                </a>
                            </div>
                        </div>
                    
                    """
                }
            except Products.DoesNotExist:
                pass
            resspons.append(prodobj)
        return JsonResponse({"data": resspons}, safe=False)

    return render(request, "monthlysales.html", {"title": "Monthly Sales", "session": request.session})


def getDay(request: HttpRequest):

    if checkAccsess(request) == False:
        return redirect("/")
    today = datetime.now()
    yesterday = datetime.date(today - timedelta(days=1))
    last_d_filter = datetime.date(today)
    if request.method == "POST":
        saleses: PayedProducts = PayedProducts.objects.filter(
            date__gte=last_d_filter)
        resspons = []
        for sales in saleses:
            user = ""
            try:
                user = AdminUsers.objects.get(id=int(sales.payeduser)).name
            except AdminUsers.DoesNotExist:
                user = "Defualt"
            try:
                prodobj = {
                    "id": sales.id,
                    "code": sales.opNum,
                    "date": sales.date,
                    "puser": user,
                    "discound": sales.discound,
                    "total": sales.lastTotal - sales.discound,
                    "options": f"""

                        <div class="row">
                            <div class='col-12 col-lg-12'>
                                <a style='width:100%'  href="/editpayedprod/{sales.id}" class="btn btn-primary">
                                    تعديل
                                </a>
                            </div>
                        </div>
                    
                    """
                }
            except Products.DoesNotExist:
                pass
            resspons.append(prodobj)
        return JsonResponse({"data": resspons}, safe=False)


def editpayedprod(request: HttpRequest, id):

    if request.method == "POST":
        post = request.POST
        print(post)
        postDate = json.loads(post['data'])
        postDelete = json.loads(post['deletedIds'])
        print(postDelete, postDate)
        prods = postDate[0: -2]
        total = postDate[-2]
        discound = postDate[-1]
        pyp: PayedProducts = PayedProducts.objects.get(id=id)
        reccount = pyp.count.split(",")[1:]
        pyp.count = ""
        pyp.productID = ""
        pyp.price = ""
        pyp.total = ""
        for e, i in enumerate(prods):
            prodyp = 0
            try:
                prod: Products = Products.objects.get(
                    id=int(i['id']))
                try:
                    count = int(i["count"]) - int(reccount[e])
                except Exception as e:
                    count = int(i['count'])
                prod.realcount = prod.realcount - count
                prod.recpry = prod.bougthprice * prod.realcount
                prodyp = prod.payprice
                prod.save()
            except Products.DoesNotExist:
                pass
            pyp.productID = pyp.productID + "," + i['id']
            pyp.price = str(str(pyp.price) + "," + str(i['price']))
            pyp.discound = float(discound)
            pyp.total = str(pyp.total) + "," + \
                str(float(prodyp) * float(i['count']))
            pyp.count = str(pyp.count) + "," + str(i['count'])
            pyp.lastTotal = float(total)
        pyp.payeduser = request.session['id']
        pyp.save()
        for i in postDelete:
            print(i)
            try:
                prod: Products = Products.objects.get(id=int(i['id']))
                prod.realcount = prod.realcount + int(i['count'])
                prod.recpry = prod.realcount * prod.bougthprice
                prod.save()
            except Products.DoesNotExist:
                pass

        print(pyp.count)
        return JsonResponse({"error": False, "succsessText": "تمت العملية بنجاح", "print": True, "opn": pyp.opNum, "payeduser": request.session['id'], "reload": True})

    prodsinrec = []
    recipt: PayedProducts = None
    try:
        recipt = PayedProducts.objects.get(id=id)
    except:
        return redirect("/allsales")

    prodsids = recipt.productID.split(",")[1:]
    counts = recipt.count.split(",")[1:]
    totals = recipt.total.split(",")[1:]
    for i, prid in enumerate(prodsids):
        product: Products = None
        try:
            product = Products.objects.get(id=int(prid))
            prdobj = {
                "id": product.id,
                "name": product.name,
                "price": product.payprice,
                "count": counts[i],
                "total": totals[i]
            }
            prodsinrec.append(prdobj)
        except Products.DoesNotExist:
            pass

    return render(request, "editpayed.html", {"title": "تعديل فاتور", "session": request.session, "allprods": Products.objects.all(), "recpr": prodsinrec, "lastotal": recipt.lastTotal, "discound": recipt.discound, "id": id})


def deleterecept(request: HttpRequest):

    if request.method == "POST":
        postDate = request.POST
        print(postDate['id'])
        postDelete = json.loads(postDate['deletedIds'])[0:-2]
        for i in postDelete:
            print(i)
            try:
                prod: Products = Products.objects.get(id=int(i['id']))
                prod.realcount = prod.realcount + int(i['count'])
                prod.recpry = prod.realcount * prod.bougthprice
                prod.save()
            except Products.DoesNotExist:
                pass
        try:
            recipt = PayedProducts.objects.get(id=int(postDate['id']))
            recipt.delete()
        except PayedProducts.DoesNotExist:
            return JsonResponse({"error": True, "errorText": "هذه الفاتورة قد تم هذفحها "}, safe=False)
        return JsonResponse({"error": False, "succsessText": "تم حذف الفاتورة بنجاح", "reload": True})

    return redirect("/allsales")
