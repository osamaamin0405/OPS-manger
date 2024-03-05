from django.urls import path
from .views import addrecipt,editrecipt,editreciptByid,deleterecipt,deletereciptByid
urlpatterns = [
    path("addrecipt", addrecipt),
    path("editrecipt", editrecipt),
    path("editrecipt/<int:id>", editreciptByid),
    path("deleterecipt", deleterecipt),
    path("deletereciptbyid/<int:id>", deletereciptByid)
]
