from django.urls import path
from .views import login, logOut, home
urlpatterns = [
    path("", login),
    path("logout", logOut),
    path("home", home),
    path("login", login)
]
