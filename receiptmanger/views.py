from adduser.models import AdminUsers
from datetime import datetime
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpRequest, JsonResponse
from categorey.models import Categorys
import json
from .models import ReciptsManger
import random
from product.models import Products
from product.views import updateprod, createprod
# Create your views here.


def addreceipt(request: HttpRequest):

    if request.method == "POST":
        postDate = request.POST
        print(postDate)
        postDate = json.loads(postDate['data'])
        if postDate[-1] == "" or postDate[-1] == "0":
            return JsonResponse({"error": True, "errorText": "من فضلك اختر القسم"})
        data = json.dumps(postDate)
        rec = ReciptsManger.objects.create(
            id=random.randint(0, 5000) * datetime.now().timestamp(),
            json=str(data),
            items=int(postDate[-2]),
            catename=int(postDate[-1]),
            addeduser=request.session['id'],
            total=postDate[-3],
        )
        rec.save()
        return JsonResponse({"error": False, "succsessText": "تم إضافة الفاتورة بنجاح"})
    allcats = Categorys.objects.all()
    return render(request, "addrecipt.html", {"title": "Add Receipt", "session": request.session, "tags": allcats})


def editreceipt(request: HttpRequest, id):

    if request.method == "POST":
        postDate = request.POST
        print(postDate)
        postDate = json.loads(postDate['data'])
        if postDate[-1] == "" or postDate[-1] == "0":
            return JsonResponse({"error": True, "errorText": "من فضلك اختر القسم"})
        data = json.dumps(postDate)
        rec = None
        try:
            rec = ReciptsManger.objects.get(id=id)
        except ReciptsManger.DoesNotExist:
            return JsonResponse({"error": True, "succsessText": "هذا المنتج غير متوفر"})
        rec.json = str(data)
        rec.items = int(postDate[-2])
        rec.catename = int(postDate[-1])
        rec.addeduser = request.session['id']
        rec.total = postDate[-3]
        rec.save()
        return JsonResponse({"error": False, "succsessText": "تم تعديل الفاتورة بنجاح"})

    recipt: ReciptsManger = None
    try:
        recipt = ReciptsManger.objects.get(id=id)
    except ReciptsManger.DoesNotExist:
        return redirect("/")

    data = []
    dataJson = json.loads(recipt.json)
    recprods = dataJson[0: -3]
    for i in recprods:
        recobj = {
            "name": i['name'],
            "count": i["count"],
            "price": i["price"],
            "barcode": i["barcode"],
            "incr": i['incr'],
            "pyprice": i["pyprice"],
            "mincount": i["mincount"]
        }
        data.append(recobj)
    items = dataJson[-2]
    total = dataJson[-3]
    cates = dataJson[-1]
    return render(request, "editrecipt.html", {"title": "تعديل فاتورة", "session": request.session, "data": data, "items": items, "total": total, "categ": cates, "tags": Categorys.objects.all(), "recid": id})


def allreceipt(request: HttpRequest):

    if request.method == "POST":
        allReceipts = ReciptsManger.objects.all()
        data = []
        catname = "Note found"
        addeduser = "Not found"
        for i in allReceipts:
            try:
                catname = Categorys.objects.get(id=int(i.catename)).name
            except Categorys.DoesNotExist:
                pass
            try:
                addeduser = AdminUsers.objects.get(id=i.addeduser).name
            except AdminUsers.DoesNotExist:
                pass
            recobj = {
                "id": i.id,
                "date": i.date,
                "items": i.items,
                "catename": catname,
                "addeduser": addeduser,
                "total": i.total,
                "optin": f"""
                    <div class="row">
                        <div class="col-lg-12 col-12">
                            <a style='width:100%'  href="/editrecipt/{i.id}" class="btn btn-primary">
                                تعديل
                            </a>
                        </div>
                    </div>
                """
            }
            data.append(recobj)
        return JsonResponse({"data": data})

    return render(request, "allrecepts.html", {"title": "كل الفواتير", "session": request.session})


def addandsave(request: HttpRequest):

    if(request.method == "POST"):
        postDate = request.POST
        id = postDate['id']
        print(postDate)
        postDate = json.loads(postDate['data'])
        if postDate[-1] == "" or postDate[-1] == "0":
            return JsonResponse({"error": True, "errorText": "من فضلك اختر القسم"})
        data = json.dumps(postDate)
        rec = ReciptsManger.objects.get(id=int(id))
        rec.json = str(data)
        rec.items = int(postDate[-2])
        rec.catename = int(postDate[-1])
        rec.addeduser = request.session['id']
        rec.total = postDate[-3]
        rec.save()
        jsonDatat = postDate[0: -3]
        for i in jsonDatat:
            prod = None
            if i['barcode'] != '' and i['barcode'] != "0":
                try:
                    prod: Products = Products.objects.get(
                        productCode=int(i['barcode']))
                    prod.realcount = prod.realcount + int(i['count'])
                    prod.recpry = float(i['price'])
                    prod.addeduser = request.session['id']
                    prod.incr = float(i['incr'])
                    prod.bougthprice = int(i['price']) / prod.realcount
                    prod.payprice = int(i['pyprice'])
                    prod.save()
                except Products.DoesNotExist:
                    id = random.randint(0, 840654) * datetime.now().timestamp()
                    createprod(id=id,
                               name=i['name'],
                               catnam=postDate[-1],
                               selsid=0,
                               addeduser=request.session['id'],
                               prcode=int(i['barcode']),
                               prbprice=(float(i['price']) / int(i['count'])),
                               prpyprice=float(i['pyprice']),
                               mcount=int(i['mincount']),
                               rcount=int(i['count']),
                               recpry=float(i['price']),
                               incr=float(i['incr']),
                               img="",
                               qrcode="")
        rec.save()
        return JsonResponse({"error": False, "succsessText": "تمت العملية بنجاح"})
    else:
        return redirect("/")


def deleterec(reques: HttpRequest):
    if reques.method == "POST":
        postData = reques.POST
        try:
            prod = ReciptsManger.objects.get(id=int(postData['id']))
            prod.delete()
            return JsonResponse({"error": False, "succsessText": "تم حذف الفاتورة بنجاح"}, safe=False)
        except ReciptsManger.DoesNotExist:
            return JsonResponse({"error": True, "errorText": "هذا المنتج غير متوفر"})

    return redirect("/")
