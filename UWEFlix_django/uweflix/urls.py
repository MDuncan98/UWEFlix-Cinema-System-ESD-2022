from django.urls import path
from uweflix import views
from uweflix.models import *

transaction_list_view = views.TransactionListView.as_view(
    queryset = Transaction.objects.order_by("-date"),
    context_object_name="transaction_list",
    template_name="uweflix/view_accounts.html",
)


urlpatterns = [
    path("", views.home, name="home"),
    path("viewings/", views.viewings, name="viewings"),
    path("add_film/", views.add_film, name="add_film"),
    path("login/", views.login, name="login"),
    path("topup/", views.topup, name="topup"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.registerPage, name="registerPage"),
    path("register_cr/", views.register_clubrep, name="register_clubrep"),
    path("payment/", views.payment, name="payment"),
    path("view_accounts/", transaction_list_view, name="view_accounts"),
    path("thanks/", views.thanks, name="thanks"),
    path("error/", views.error, name="error"),
    path("am_home/", views.am_home, name="accounts_home"),
    path("user/", views.userpage, name="user-page"),
    path("transaction_test/", views.transaction_test, name="transaction_test"),
]