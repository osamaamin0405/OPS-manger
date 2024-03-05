from datetime import datetime
from os import error
from os.path import samefile
from django.http.response import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.http.request import HttpRequest
from categorey.models import Categorys
from sales_manger.models import SalesesManger
import random
from .models import Products
from .models import Qrcodes
from helpers.functions import checkAccsess
# Create your views here.

import base64


def prcodeexisi(code):
    try:
        pr = Products.objects.get(productCode=code)
        return True
    except Products.DoesNotExist:
        return False


def createprod(id, name, catnam, selsid, addeduser, prcode, prbprice, prpyprice, mcount, rcount, img, qrcode, recpry, incr):
    if prcodeexisi(prcode) != True:
        Products.objects.create(id=id,
                                name=name,
                                salesname=selsid,
                                catename=catnam,
                                addeduser=addeduser,
                                bougthprice=prbprice,
                                payprice=prpyprice,
                                minconut=mcount,
                                realcount=rcount,
                                productimge=img,
                                productCode=prcode, recpry=recpry, incr=incr)
        if qrcode != "":
            from django.core.files.base import ContentFile
            format, imgstr = qrcode.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))
            filename = str(id) + "." + ext
            data.name = filename
            Qrcodes.objects.create(id=id, qrfiel=data)
        return {"error": False, "succsessCode": 40, "succsessText": f"Product {name} Added Succsessfuly"}
    else:
        return {"error": True, "errorCode": 41, "errorText": f"Product {prcode} Is Exist"}


def updateprod(id, name, prcode, catnam, selsid, prbprice, prpyprice, mcount, rcount, img, recpry, incr):
    try:
        prod: Products = Products.objects.get(id=id)
        prod.name = name
        prod.productCode = prcode
        prod.catename = prod.catename if catnam == 0 or catnam == "" else catnam
        prod.salesname = prod.salesname if selsid == 0 or selsid == "" else selsid
        prod.bougthprice = prbprice
        prod.payprice = prpyprice
        prod.minconut = mcount
        prod.realcount = rcount
        prod.recpry = recpry
        prod.incr = incr
        if img != "":
            prod.productimge = img
        prod.save()
        return {"error": False, "succsessCode": 40, "succsessText": f"المنتج {name} تم تعديله بنجاح"}
    except Products.DoesNotExist:
        return {"error": True, "errorCode": 41, "errorText": f"هذا المنتج {id} غير متوفر"}


def addproduct(request: HttpRequest):
    if checkAccsess(request) == False:
        return redirect("/")
    if request.method == "POST":
        postData = request.POST
        name = postData['prname']
        catname = int(postData['catename'])
        selsid = int(postData['catselc'])
        prcode = postData['prodcode']
        incr = int(postData['incra'])
        id = random.randint(0, 1000) + int(prcode) + \
            int(datetime.now().timestamp())
        qrcode = request.POST["qrcode"]
        prbprice = float(postData['prbuprice'])
        prpyprice = float(postData['prpypric'])
        mcount = int(postData["mincount"])
        rcount = int(postData['rcount'])
        image = ""
        try:
            image = request.FILES['productimage']
        except:
            image = ""
        recpry = prbprice
        prbprice = prbprice / rcount
        error = False
        errormsg = ""
        if prbprice < 1:
            error = True
            errormsg = "The Bought Price Less Than 1"
        elif prpyprice <= prbprice:
            error = True
            errormsg = "Pay Price Must Be More Than Bought Price"
        else:
            error = False
            errormsg = ""

        if error == False:
            masg = createprod(id=id,
                              name=name,
                              catnam=catname,
                              selsid=selsid,
                              prcode=prcode,
                              prbprice=prbprice,
                              prpyprice=prpyprice,
                              mcount=mcount,
                              rcount=rcount,
                              img=image,
                              addeduser=request.session['id'], qrcode=qrcode, recpry=recpry, incr=incr)

            return JsonResponse(masg)
        else:
            return JsonResponse({"error": True, "errorText": errormsg}, safe=False)

    return render(request, "addProdact.html", {"session": request.session, "title": "Add Product", "categotys": Categorys.objects.all(), "salsesnames": SalesesManger.objects.all()})


def editProduct(request: HttpRequest):
    if checkAccsess(request=request) == False:
        return redirect("/")
    if request.method == "POST":
        postData = request.POST
        name = postData['prname']
        catname = int(postData['catename'])
        selsid = int(postData['catselc'])
        id = postData['prid']
        prbprice = float(postData['prbuprice'])
        prpyprice = float(postData['prpypric'])
        mcount = int(postData["mincount"])
        rcount = postData.get("rcount")
        rcount = int(rcount)
        prcode = int(postData['prcode'])
        recpry = float(postData['recpry'])
        incr = float(postData['incra'])
        image = ""
        print(rcount, mcount)
        try:
            image = request.FILES['productimage']
        except:
            image = ""

        
        msg = updateprod(id=id, name=name, catnam=catname, selsid=selsid, prbprice=prbprice,
                         prpyprice=prpyprice, mcount=mcount, rcount=rcount, img=image, incr=incr, prcode=prcode, recpry=recpry)
        return JsonResponse(msg)

    else:
        primg = Products.objects.first().productimge
        primg = str(primg).replace("uploads/", "")
        return render(request, "editproduct.html", {"session": request.session, "title": "Edit Product", "allprod": Products.objects.all(), "len": 2, "categotys": Categorys.objects.all(), "salsesnames": SalesesManger.objects.all(), "prdimg": primg})


def editProductByid(request: HttpRequest, id):
    if checkAccsess(request=request) == False:
        return redirect("/")
    if request.method == "POST":
        postData = request.POST
        name = postData['prname']
        catname = int(postData['catename'])
        selsid = int(postData['catselc'])
        id = id
        prbprice = float(postData['prbuprice'])
        prpyprice = float(postData['prpypric'])
        mcount = int(postData["mincount"])
        rcount = postData.get("rcount")
        rcount = int(rcount)
        prcode = int(postData['prcode'])
        recpry = float(postData['recpry'])
        incr = float(postData['incra'])
        image = ""
        try:
            image = request.FILES['productimage']
        except:
            image = ""
        error = False
        errormsg = ""
        if prbprice < 1:
            error = True
            errormsg = "The Bought Price Less Than 1"
        elif prpyprice <= prbprice:
            error = True
            errormsg = "Pay Price Must Be More Than Bought Price"
        else:
            error = False
            errormsg = ""
        if error == False:
            msg = updateprod(id=id, name=name, catnam=catname, selsid=selsid, prbprice=prbprice,
                             prpyprice=prpyprice, mcount=mcount, rcount=rcount, img=image)
            return JsonResponse(msg, safe=False)
        else:
            return JsonResponse(errormsg,safe=False)
    else:
        try:
            primg = Products.objects.get(id=id).productimge
            primg = str(primg).replace("uploads/", "")
        except Products.DoesNotExist:
            return redirect("/editproduct")
        return render(request, "editproduct.html", {"session": request.session, "title": "Edit Product", "allprod": Products.objects.get(id=id), "len": 1, "categotys": Categorys.objects.all(), "salsesnames": SalesesManger.objects.all(), "prdimg": primg, "id": id})


def paydefinded(request: HttpRequest):

    if(checkAccsess(request) == False):
        return redirect("/")

    if(request.method == "POST"):
        postData = request.POST
        id = postData['prid']
        count = postData['count']
        try:
            prod: Products = Products.objects.get(id=id)
            lastcount = prod.realcount
            prod.realcount = int(count) + int(lastcount)
            prod.save()
            msg = {"error": False,
                   "succsessText": f"This Product id {id} Not Found", "reload": True}
            return JsonResponse(msg, safe=False)
        except Products.DoesNotExist:
            msg = {"error": True, "errorText": f"This Product id {id} Not Found", }
            return JsonResponse(msg, safe=False)

    return render(request, "paydefined.html", {"session": request.session, "title": "Pay Defined Product", "allprod": Products.objects.all(), "len": 2, })


def getProdByScannerID(request: HttpRequest):
    if request.method == "POST":
        postDate = request.POST
        scanid = postDate['code']
        try:
            prod: Products = Products.objects.get(productCode=scanid)
            primag = prod.productimge
            primag = str(primag).replace("uploads/", "")
            sales = 0
            try:
                sd = float(prod.salesname)
                sales = SalesesManger.objects.get(id=int(sd)).id
            except SalesesManger.DoesNotExist:
                pass
            cate = 0
            try:
                cd = float(prod.catename)
                cate = Categorys.objects.get(id=int(cd)).id
            except Categorys.DoesNotExist:
                cate = 0
            prodobj = {"error": False,
                       "successcode": 50,
                       "succsessText": "تم إيجاد المنتج",
                       "product": {
                           "id": prod.id,
                           "name": prod.name,
                           "prcode": prod.productCode,
                           "primage": str(prod.productimge),
                           "mcount": prod.minconut,
                           "rcount": prod.realcount,
                           "boughtprice": prod.bougthprice,
                           "paypric": prod.payprice,
                           "sales": sales,
                           "category": cate,
                           "recpry": prod.recpry,
                           "incr": prod.incr
                       }
                       }
            return JsonResponse(prodobj, safe=False)
        except Products.DoesNotExist:
            return JsonResponse(
                {"error": True, "errorText": f"هذا المنتج غير موجود في قاعدة البينات"},safe=False)
    else:
        return Http404()


def getallProdaut(request: HttpRequest):

    if checkAccsess(request) == False:
        return redirect("/")

    if request.method == "POST":
        prods: Products = Products.objects.all()
        resspons = []
        for prod in prods:
            primag = prod.productimge
            primag = str(primag).replace("uploads/", "")
            date = str(prod.date).split(" ")
            catename = "لايوجد"
            try:
                catename = Categorys.objects.get(id=int(prod.catename)).name
            except:
                catename = "لايوجد"
            prodobj = {
                "id": prod.id,
                "name": prod.name,
                "date": date[0] + " " + date[1].split(".")[0],
                "prcode": f"""
                    <div class='row'>
                        <div style='text-align:center' class="col-lg-12 col-1"> {prod.productCode} </div>
                        <div style='text-align:center' class='col-lg-12 col-12'>
                            <div class='print-qrcode btn btn-light' data-print='#qr-{prod.id}'>
                                <i class="fas fa-print"></i>
                            </div>
                            <img id='qr-{prod.id}' width='38px' height='38px' src="/static/qrcodes/{prod.id}.png" alt='qrcode'/>
                        </div>
                    </div>
                """,
                "mcount": prod.minconut,
                "rcount": prod.realcount,
                "boughtprice": prod.bougthprice,
                "paypric": prod.payprice,
                "catename": catename,
                "option": f"""
                    <div class="row">
                        <div class="col-lg-12 col-12">
                            <a style='width:100%'  href="/editproduct/{prod.id}" type="submit" class="btn btn-primary">
                                تعديل
                            </a>
                        </div>
                    </div>
                """
            }

            resspons.append(prodobj)
        return JsonResponse({"data": resspons}, safe=False)
    return render(request, "allproduct.html", {"allproduct": Products.objects.all(), "session": request.session, "title": "All Product"})


def alertProduct(request: HttpRequest):

    if checkAccsess(request) == False:
        return redirect("/")

    if request.method == "POST":
        prods: Products = Products.objects.all()
        resspons = []
        for prod in prods:
            mincount = prod.minconut
            rcount = prod.realcount
            if mincount >= rcount:
                date = str(prod.date).split(" ")
                prodobj = {
                    "id": prod.id,
                    "name": prod.name,
                    "date": date[0] + " " + date[1].split(".")[0],
                    "prcode": f"""
                        <div class='row'>
                            <div style='text-align:center' class="col-lg-12 col-1"> {prod.productCode} </div>
                            <div style='text-align:center' class='col-lg-12 col-12'>
                                <div class='print-qrcode btn btn-light' data-print='#qr-{prod.id}'>
                                    <i class="fas fa-print"></i>
                                </div>
                                <img id='qr-{prod.id}' width='38px' height='38px' src="/static/qrcodes/{prod.id}.png" alt='qrcode'/>
                            </div>
                        </div>
                    """,
                    "mcount": prod.minconut,
                    "rcount": prod.realcount,
                    "boughtprice": prod.bougthprice,
                    "paypric": prod.payprice,
                    "option": f"""
                        <div class="row">
                            <div class="col-lg-12 col-12">
                                <a style='width:100%'  href="/editproduct/{prod.id}" type="submit" class="btn btn-primary">
                                    تعديل
                                </a>
                            </div>
                        </div>
                    """
                }

                resspons.append(prodobj)
        return JsonResponse({"data": resspons}, safe=False)
    return render(request, "alertsproduct.html", {"session": request.session, "title": "Products Alert"})


def deleteProduct(request: HttpRequest):

    if(request.method == "POST"):
        postData = request.POST
        print(postData)
        try:
            id = postData['prid']
            prod = Products.objects.get(id=int(id))
            prod.delete()
        except Products.DoesNotExist:
            return JsonResponse({"error": True, "errorText": "هذا المنتج غير موجود او قد تم حذفه"})
        return JsonResponse({"error": False, "succsess": True, "succsessText": "تم حذف المنتج بنجاح", "reload": True},safe=False)
    return redirect("/")
