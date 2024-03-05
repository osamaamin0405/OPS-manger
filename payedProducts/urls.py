from django.urls import path
from .views import addpayedprod, getAllSales, getMonth, getDay, editpayedprod, deleterecept
urlpatterns = [
    path('addpayedprod', addpayedprod),
    path("allsales", getAllSales),
    path("monthlysales", getMonth),
    path("todaysales", getDay),
    path("editpayedprod/<int:id>", editpayedprod),
    path("delepayeded", deleterecept)
]
