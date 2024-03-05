from django.urls import path
from .views import addcategory, editCategory, deletecategorty
urlpatterns = [
    path("addcategory", addcategory),
    path("editcategory", editCategory),
    path("deletecategory", deletecategorty)
]
