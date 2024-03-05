from datetime import datetime
from django.db import models
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from .models import AdminUsers
import random
import django.db.utils
from django.contrib.auth.hashers import make_password
import sys
sys.path.append("..")
from helpers.functions import updateSession, checkAccsess

# Create your views here.


def userIsExist(val):
    finded = False

    try:
        user = AdminUsers.objects.get(name=val)
        finded = user
    except AdminUsers.DoesNotExist:
        finded = False
    return finded


def userIsExistWithId(val):
    finded = False

    try:
        user = AdminUsers.objects.get(id=val)
        finded = user
    except AdminUsers.DoesNotExist:
        finded = False
    return finded


@csrf_protect
def adduser(request: HttpRequest):
    if checkAccsess(request) == False:
        return redirect("/")
    id = random.randint(0, 16514) * 1000
    if(request.method == "POST"):
        postData = request.POST
        user = userIsExist(val=postData['username'])

        if user:
            htmlError = f"""<div class="form-group">
                    <div class="alert alert-danger" role="alert">
                        <strong>This User Is Exist</strong>
                        <a href='/useredir/{user.id}'> Edit This User </a>
                    </div>
                </div>"""
            ress = {"error": True, "errorText": "This User Is Exist",
                    "ErrorCode": 5, "UserFindeID": user.id, "htmlError": htmlError}
            return JsonResponse(safe=False, data=ress)
        else:
            name = postData['username']
            permation = postData['userpermation']
            password = make_password(postData['userpass'])
            image = request.FILES['userimage']
            try:
                user = AdminUsers.objects.create(id=id,
                                                 name=name,
                                                 password=password, premission=permation,
                                                 userImgae=image,
                                                 )
            except django.db.utils.IntegrityError:
                user = AdminUsers.objects.create(id=id * 45,
                                                 name=name,
                                                 password=password, premission=permation,
                                                 userImgae=image,
                                                 )
            ress = {"error": False, "succsessText": f"User {user.name} Added Succsesfuly",
                    "succsesscode": 6, "UserFindeID": user.id, }
            return JsonResponse(safe=False, data=ress)

    return render(request, "adduser.html", {"title": "Add User", "permaions": ["admin", "Date Input"], "session": request.session})


def edituser(request):
    if request.method == "POST":
        postData = request.POST
        user: AdminUsers
        try:
            user = AdminUsers.objects.get(id=postData['id'])
        except AdminUsers.DoesNotExist:
            ress = {"error": True, "errorText": f"User Dose Not Exisst",
                    "errorCode": 8}
            return JsonResponse(safe=False, data=ress)
        try:
            name = postData['username']
            permation = postData['userpermation']
            password = ""
            if postData['userpass'] != "":
                password = make_password(postData['userpass'])
            image = ""
            try:
                image = request.FILES['userimage']
            except:
                pass
            if name != "" or request.session['name'] == name:
                user.name = name
            if permation != "":
                user.premission = permation
            if image != "":
                import os
                try:
                    path = "%s" % (user.userImgae)
                    os.remove(path)
                except:
                    pass
                user.userImgae = image
            if password != "":
                user.password = password
            user.save()
            if int(request.session['id']) == int(postData['id']):
                updateSession(request=request, user=user)
                ress = {"error": False, "redirect": "/logout", "succsessText": f"User {user.name} Edit Suucsessfly",
                        "succsesscode": 7, "UserFindeID": user.id, }
                return JsonResponse(ress)
            htmlSuccses = f"""<div class="form-group">
                        <div class="alert alert-succsess" role="alert">
                            <strong>User {user.name} Edir Succsessfuly</strong>
                        </div>
                    </div>"""
            ress = {"error": False, "succsessText": f"User {user.name} Edit Suucsessfly",
                    "succsesscode": 7, "UserFindeID": user.id, "succsessHtml": htmlSuccses}
            return JsonResponse(safe=False, data=ress)
        except Exception as e:
            print(e)
            htmlError = f"""<div class="form-group">
                        <div class="alert alert-danger" role="alert">
                            <strong>Some Thing Wan't Warring</strong>
                        </div>
                    </div>"""
            ress = {"error": True, "errorText": "Can't Edit This User or User Name Is Exist",
                    "ErrorCode": 6, "UserFindeID": user.id, "htmlError": htmlError}
            return JsonResponse(safe=False, data=ress)
    return render(request, "edituser.html", {"title": "Edit User", "session": request.session, "permaions": ["admin", "Date Input"], "users": AdminUsers.objects.all(), "len": 2})


def edituserById(request, id):
    if request.method == "POST":
        postData = request.POST
        try:
            user: AdminUsers = AdminUsers.objects.get(id=id)
            try:
                name = postData['username']
                permation = postData['userpermation']
                password = ""
                if postData['userpass'] != "":
                    password = make_password(postData['userpass'])
                image = ""
                try:
                    image = request.FILES['userimage']
                except:
                    pass
                if name != "" or request.session['name'] == name:
                    user.name = name
                if permation != "":
                    user.premission = permation
                if image != "":
                    import os
                    os.remove(user.userImgae)
                    user.userImgae = image
                if password != "":
                    user.password = password
                user.save()
                if int(request.session['id']) == int(id):
                    updateSession(request=request, user=user)
                    ress = {"error": False, "redirect": "/logout", "succsessText": f"User {user.name} Edit Suucsessfly",
                            "succsesscode": 7, "UserFindeID": user.id, }
                    return JsonResponse(ress)
                htmlSuccses = f"""<div class="form-group">
                                <div class="alert alert-succsess" role="alert">
                                    <strong>User {user.name} Edir Succsessfuly</strong>
                                </div>
                            </div>"""
                ress = {"error": False, "succsessText": f"User {user.name} Edit Suucsessfly",
                        "succsesscode": 7, "UserFindeID": user.id, "succsessHtml": htmlSuccses}
                return JsonResponse(safe=False, data=ress)
            except Exception as e:
                print(e)
                htmlError = f"""<div class="form-group">
                                <div class="alert alert-danger" role="alert">
                                    <strong>Some Thing Wan't Warring</strong>
                                </div>
                            </div>"""
                ress = {"error": True, "errorText": "Can't Edit This User or User Name Is Exist",
                        "ErrorCode": 6, "UserFindeID": user.id, "htmlError": htmlError}
                return JsonResponse(safe=False, data=ress)
        except AdminUsers.DoesNotExist:
            return JsonResponse({"error": True, "errorText": "Invalid User ID"})
    return render(request, "edituser.html", {"title": "Edit User", "session": request.session, "permaions": ["admin", "Date Input"], "users": AdminUsers.objects.get(id=id), "len": 1})


@csrf_protect
def editusers(request: HttpRequest, id=1):
    if checkAccsess(request) == False:
        return HttpResponseRedirect("/home")
    if id == 1:
        return edituser(request)
    else:
        return edituserById(request, id)


def deletuser(request: HttpRequest):
    if request.method == "POST":
        postData = request.POST
        id = postData['id']
        user = AdminUsers.objects.get(id=id)
        name = user.name
        id = user.id
        user.delete()
        if int(request.session['id']) == int(id):
            ress = {"error": False, "redirect": "/logout", "succsessText": f"User {name} Was Deleted Suucsessfly",
                    "succsesscode": 10, "UserFindeID": id, }
            return JsonResponse(ress)
        else:
            ress = {"error": False, "succsessText": f"User {name} Was Deleted Suucsessfly",
                    "succsesscode": 11, "UserFindeID": id, }
            return JsonResponse(ress)
    else:
        return redirect("/")


def deletuserByID(request, id):
    if request.method == "POST":
        id = id
        try:
            user = AdminUsers.objects.get(id=id).delete()
            if int(request.session['id']) == int(id):
                ress = {"error": False, "redirect": "/logout", "succsessText": f"User {user.name} Was Deleted Suucsessfly",
                        "succsesscode": 10, "UserFindeID": user.id, }
                return JsonResponse(ress)
            else:
                ress = {"error": False, "succsessText": f"User {user.name} Was Deleted Suucsessfly",
                        "succsesscode": 11, "UserFindeID": user.id, }
                return JsonResponse(ress)
        except AdminUsers.DoesNotExist:
            ress = {"error": True, "errorText": "this user id not found",
                    "errorcode": 12, }
            return JsonResponse(ress)
    else:
        return redirect("/")


def deletusers(request, id=1):
    if checkAccsess == False:
        return HttpResponseRedirect("/")
    if id == 1:
        deletuser(request)
    elif id != 1:
        deletuserByID(request, id)
    else:
        return redirect("/")
