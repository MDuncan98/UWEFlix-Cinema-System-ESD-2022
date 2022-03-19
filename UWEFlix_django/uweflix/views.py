from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import ContextPopException
from django.views.generic import ListView
from .models import *
from django.utils.timezone import datetime

def home(request):
    return render(request, 'uweflix/index.html')

def viewings(request):
    films = Film.objects.all()
    context = {'films':films}
    return render(request, 'uweflix/viewings.html', context)   

def add_film(request):
    context = {}
    if request.method == "POST":
        ages = {"U", "PG", "12", "12A", "15", "18"}
        title = request.POST.get('title')
        age_rating = request.POST.get('age_rating')
        duration = request.POST.get('duration')
        trailer_desc = request.POST.get('trailer_desc')
        if (duration.isdigit()):
            if(age_rating in ages):
                film = Film()
                film.title = title
                film.age_rating = age_rating
                film.duration = duration
                film.trailer_desc = trailer_desc
                film.save()
            else:
                print("Invalid Age Rating")
        else:
            print("Duration is not a valid number")
    return render(request, 'uweflix/add_film.html', context) 

def login(request):
    if request.method == "POST":
        request.POST.get('username') #Gets Username
        request.POST.get('password') # Gets Password
        # IF account_type = 'cm'
            #redirect to add film page
        # ELIF ... 'am'
        #   #
    return render(request, 'uweflix/login.html')

def payment(request):
    return render(request, 'uweflix/payment.html')


class TransactionListView(ListView):  # Logic for the View Accounts page
    model = Transaction

    def get_queryset(self):
        query = self.request.GET.get('search_accounts')
        object_list = Transaction.objects.filter(  # Search for specified account transactions within the last month
            customer=query,
            date__year = datetime.now().year,
            date__month = datetime.now().month
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)
        return context
