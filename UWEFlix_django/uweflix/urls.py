from django.urls import path
from uweflix import views

urlpatterns = [
    path("", views.home, name="home"),
    path("viewings/", views.viewings, name="viewings"),
    path("add_film/", views.add_film, name="add_film"),
    path("login/", views.login, name="login"),
    path("view_accounts/", views.view_accounts, name="view_accounts")
]