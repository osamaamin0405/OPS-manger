from django.urls import path
from .views import addreceipt, editreceipt, allreceipt, addandsave, deleterec
urlpatterns = [
    path('addrecipt', addreceipt),
    path("editrecipt/<int:id>", editreceipt),
    path("allreceipts", allreceipt),
    path("addandsavereceipt", addandsave),
    path("deleterec", deleterec)
]
