from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from django.template import ContextPopException
from .models import *

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

def view_accounts(request):
    return render(request, 'uweflix/view_accounts.html')