def updateSession(request, user):
    request.session["id"] = user.id
    request.session["name"] = user.name
    #request.session["permissions"] = user.premission
    request.session["userImgae"] = str(
        user.userImgae).replace("uploads/", "")
    request.session["dataCreated"] = str(user.dataCreated)
    return (request.session, user)


def checkAccsess(request):
    accses = True
    try:
        if(str(request.session['permissions']) != str(1)):
            accses = False
            return accses
    except:
        accses = False
    try:
        if(request.session['id'] == None or request.session['name'] == None):
            accses = False
            return accses
        accses = True
    except:
        accses = False
    return accses
