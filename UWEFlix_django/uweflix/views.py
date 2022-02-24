from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'uweflix/index.html')

def viewings(request):
    return render(request, 'uweflix/viewings.html')   