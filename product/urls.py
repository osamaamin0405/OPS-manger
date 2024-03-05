from django.urls import path
from django.urls.conf import include
from .views import addproduct, editProduct, paydefinded, getProdByScannerID, getallProdaut, alertProduct, editProductByid, deleteProduct
urlpatterns = [
    path('addproduct', addproduct),
    path("editproduct", editProduct),
    path("editproduct/<int:id>", editProductByid),
    path("delprod", deleteProduct),
    path("paydefined", paydefinded),
    path("scannerProd", getProdByScannerID),
    path("allproduct", getallProdaut),
    path("alertproducts", alertProduct)
]
