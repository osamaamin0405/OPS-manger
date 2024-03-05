from random import randint, random
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from .models import SalesesManger
from django.http.response import JsonResponse

import sys
sys.path.append("..")
from helpers.functions import checkAccsess

# Create your views here.


def checkSalseCodeDoesNotExist(salseCode):
    sales = False
    try:
        salse = SalesesManger.objects.get(salesCode=salseCode)
    except SalesesManger.DoesNotExist:
        sales = True
        return sales


def checkSalseByID(id):
    try:
        salse = SalesesManger.objects.get(id=id)
        return salse
    except SalesesManger.DoesNotExist:
        return False


def addsalesemanger(request: HttpRequest):
    if checkAccsess(request) == False:
        return redirect("/")
    if request.method == "POST":
        postData = request.POST
        name = postData['salesname']
        code = int(postData['salescode'])
        if checkSalseCodeDoesNotExist(code):
            print(postData)
            try:
                id = randint(0, 200) * 1000 * code
                salse = SalesesManger.objects.create(
                    name=name, salesCode=code, id=id)
                ress = {"error": False, "succsessCode": 20,
                        "succsessText": f"Salses Manger {salse.name}  Added Succsessfuly"}
                return JsonResponse(ress, safe=False)
            except Exception as e:
                print(e)
                ress = {"error": True, "errorCode": 22,
                        "errorText": f"Some Thing Happend Please Check Sales Code Lenth and Try Agin"}
            return JsonResponse(ress, safe=False)
        else:
            ress = {"error": True, "errorCode": 21,
                    "errorText": f"This Salse Code {code} Is Exist"}
            return JsonResponse(ress, safe=False)
    elif request.method == "GET":
        return render(request, "addsales.html", {"title": "Add Sales Manger", "session": request.session})


def editSalesManger(request: HttpRequest):

    if checkAccsess(request) == False:
        return redirect("/")

    if request.method == "POST":
        psotDate = request.POST
        name = psotDate['salesname']
        code = psotDate['salescode']
        id = psotDate['salseid']
        if checkSalseCodeDoesNotExist(code):
            salse: SalesesManger = SalesesManger.objects.get(id=id)
            salse.name = name
            salse.salesCode = code
            salse.save()
            ress = {"error": False, "succsessCode": 20,
                    "succsessText": f"Salses Manger {salse.name}  Edited Succsessfuly"}
            return JsonResponse(ress, safe=False)
        else:
            ress = {"error": True, "errorCode": 21,
                    "errorText": f"This Salse Code {code} Is Exist"}
            return JsonResponse(ress, safe=False)

    return render(request, "editsales.html", {"len": 2, "session": request.session, "salesmangers": SalesesManger.objects.all()})


def deletesalasemanger(request: HttpRequest):
    if checkAccsess(request) == False:
        return redirect("/")

    if request.method == "POST":
        psotDate = request.POST
        name = psotDate['salesname']
        code = psotDate['salescode']
        id = psotDate['salseid']
        try:
            salse: SalesesManger = SalesesManger.objects.get(id=id)
            salse.delete()
            ress = {"error": False, "succsessCode": 20,
                    "succsessText": f"Salses Manger {salse.name}  Deleted Succsessfuly", "reload": True}
            return JsonResponse(ress, safe=False)
        except SalesesManger.DoesNotExist:
            ress = {"error": True, "errorCode": 22,
                    "errorText": f"This Salse id {id} Dose Not Exist", }
            return JsonResponse(ress, safe=False)

    return render(request, "editsales.html", {"title": "Delete Sales Manger", "len": 2, "session": request.session, "salesmangers": SalesesManger.objects.all()})
