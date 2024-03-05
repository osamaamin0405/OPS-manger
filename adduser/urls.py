from django.urls import path
from .views import adduser, editusers, deletusers
urlpatterns = [
    path("adduser", adduser),
    path("editusers", editusers),
    path("editusers/<int:id>", editusers),
    path("deletusers", deletusers),
    path("deletusers/<int:id>", deletusers)
]
