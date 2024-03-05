from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import JsonResponse
import sys
sys.path.append("..")
from helpers.functions import checkAccsess
from .models import Categorys
from random import randint
# Create your views here.


def checkCateCodeDoesNotExist(catecode):
    sales = False
    try:
        salse = Categorys.objects.get(catcode=catecode)
    except Categorys.DoesNotExist:
        sales = True
        return sales


def addcategory(request: HttpRequest):
    if checkAccsess(request) == False:
        return redirect("/")
    if request.method == "POST":
        postData = request.POST
        name = postData['catname']
        code = int(postData['catcode'])
        if checkCateCodeDoesNotExist(code):
            print(postData)
            try:
                id = randint(0, 200) * 1000 * code
                cate = Categorys.objects.create(
                    name=name, catcode=code, id=id)
                ress = {"error": False, "succsessCode": 30,
                        "succsessText": f"Category {cate.name} Added Succsessfuly"}
                return JsonResponse(ress, safe=False)
            except Exception as e:
                print(e)
                ress = {"error": True, "errorCode": 22,
                        "errorText": f"Some Thing Happend Please Check Sales Code Length and Try Agin"}
                return JsonResponse(ress, safe=False)
        else:
            ress = {"error": True, "errorCode": 31,
                    "errorText": f"This Category code {code} Is Exist"}
            return JsonResponse(ress, safe=False)
    elif request.method == "GET":
        return render(request, "addCategory.html", {"session": request.session, "title": "Add Category"})


def editCategory(request: HttpRequest):

    if checkAccsess(request) == False:
        return redirect("/")

    if request.method == "POST":
        psotDate = request.POST
        name = psotDate['catname']
        code = psotDate['catecode']
        id = psotDate['catid']
        if checkCateCodeDoesNotExist(code):
            category: Categorys = Categorys.objects.get(id=id)
            category.name = name
            category.catcode = code
            category.save()
            ress = {"error": False, "succsessCode": 33,
                    "succsessText": f"Category {category.name} Has ben Edit Succsessfuly"}
            return JsonResponse(ress, safe=False)
        else:
            ress = {"error": True, "errorCode": 34,
                    "errorText": f"This Category Code {code} Is Exist"}
            return JsonResponse(ress, safe=False)

    return render(request, "editcategory.html", {"title": "Edit Category", "len": 2, "session": request.session, "categorys": Categorys.objects.all()})


def deletecategorty(request: HttpRequest):
    if checkAccsess(request) == False:
        return redirect("/")

    if request.method == "POST":
        psotDate = request.POST
        name = psotDate['catname']
        code = psotDate['catecode']
        id = psotDate['catid']
        try:
            category: Categorys = Categorys.objects.get(id=id)
            category.delete()
            ress = {"error": False, "succsessCode": 35,
                    "succsessText": f"Category {name}  Deleted Succsessfuly", "reload": True}
            return JsonResponse(ress, safe=False)
        except Categorys.DoesNotExist:
            ress = {"error": True, "errorCode": 22,
                    "errorText": f"This Category id {id} Dose Not Exist", }
            return JsonResponse(ress, safe=False)

    return render(request, "editcategory.html", {"title": "Edit Category", "len": 2, "session": request.session, "salesmangers": Categorys.objects.all()})
