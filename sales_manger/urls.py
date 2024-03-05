from django.urls import path
from .views import addsalesemanger, editSalesManger, deletesalasemanger
urlpatterns = [
    path("addsalesmanger", addsalesemanger),
    path("editsalesmanger", editSalesManger),
    path("deletesalasemanger", deletesalasemanger),

]
