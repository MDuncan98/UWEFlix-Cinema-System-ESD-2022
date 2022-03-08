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
    return render(request, 'uweflix/add_film.html', context) 

def login(request):
    if request.method == "POST":
        request.POST.get('username') #Gets Username
        request.POST.get('password') # Gets Password
    return render(request, 'uweflix/login.html')