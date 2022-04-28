from django.urls import path
from uweflix import views
from uweflix.models import *



urlpatterns = [
    path("", views.viewings, name="home"),
    path("viewings/", views.viewings, name="viewings"),
    path("showings/<int:film>/", views.showings, name="showings_by_film"),
    path("add_film/", views.add_film, name="add_film"),
    path("login/", views.login, name="login"),
    path("topup/", views.topup, name="topup"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.registerPage, name="registerPage"),
    path("register_cr/", views.register_clubrep, name="register_clubrep"),
    path("payment/<int:showing>/", views.payment, name="payment"),
    path("pay_with_card/", views.pay_with_card, name="pay_with_card"),
    path("view_accounts/", views.view_accounts, name="view_accounts"),
    path("daily_transactions/", views.daily_transactions, name="daily_transactions"),
    path("customer_statements/", views.customer_statements, name="customer_statements"),
    path("thanks/", views.thanks, name="thanks"),
    path("user/", views.userpage, name="user-page"),
    path("add_club/", views.add_club, name="add_club"),
    path("add_rep/", views.add_rep, name="add_rep"),
    path("club_rep_home/", views.club_rep_home, name="club_rep_home"),
    path("cinema_manager_home/", views.cinema_manager_home, name="cinema_manager_home"),
    path("student_home/", views.student_home, name="student_home"),
    path("set_payment/", views.set_payment_details, name="set_payment"),
    path("am_home/", views.am_home, name="am_home"),
    path("add_account/", views.addClubAccount, name="add_account"),
    path("settle_payments/", views.settle_payments, name="settle_payments"),
    path("review_students/<int:userID>", views.review_students, name="review_students"),
]