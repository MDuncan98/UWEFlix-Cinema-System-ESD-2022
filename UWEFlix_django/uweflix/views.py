from multiprocessing import context
from turtle import title
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import ContextPopException
from django.views.generic import *

#from uweflix.decorators import unauthenticated_user
from .models import *
from django.utils.timezone import datetime
from .forms import PaymentForm
#from .decorators import unauthenticated_user
#from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import Group
#from django.contrib import messages


def home(request):
    return render(request, 'uweflix/index.html')

def viewings(request):
    films = Film.objects.all()
    context = {'films':films}
    return render(request, 'uweflix/viewings.html', context)

def showings(request, film):
    showings = Showing.objects.filter(film=film).order_by('time')
    film = Film.objects.get(pk=film)
    context = {'showings':showings, 'film':film}
    return render(request, 'uweflix/showings.html', context)

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

#@unauthenticated_user
def login(request):
    if request.method == 'POST':
        un = request.POST['username'] #Gets Username
        pw = request.POST['password'] #Gets Password
        try:
            acc = Account.objects.get(username=un)#Get account from database
            if (acc.password == pw): #If entered password matches one from account object
                request.session['username'] = un
                request.session['accountType'] = acc.account_type
                if (acc.account_type == 'cm'): # Cinema Manager
                    return render(request, 'uweflix/add_film.html')
                if (acc.account_type == 'am'): # Accounts Manager
                    return render(request, 'uweflix/view_accounts.html')
                if (acc.account_type == 'cr'): # Cinema Manager
                    return render(request, 'uweflix/viewings.html')
                if (acc.account_type == 'st'): # Student
                    return render(request, 'uweflix/viewings.html')
        except:
            #More useful error message to be shown to user can be added
            print("error")

    return render(request, "uweflix/logIn.html")

def userpage(request):
    context = {}
    return render(request, 'uweflix/user.html', context)

def payment(request): # Will also take showing_id as a param once showing page is completed!
    showing = Showing.objects.filter(id=1)
    form = PaymentForm()
    context = {
        "show_showing": showing,
        "form": form
    }
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            print("Success")
            return render(request, "uweflix/thanks.html")
            # Payment Logic will go here once prerequestites are completed
            #return redirect('uweflix/thanks.html')
        else:
            return render(request, 'uweflix/payment.html', context={'form':form, "show_showing": showing})

    return render(request, 'uweflix/payment.html', context)

def thanks(request):
    render(request, "uweflix/thanks.html")

def topup(request):
    if 'accountType' in request.session:
        if request.session['accountType'] == "cr":
            if request.method == 'POST':
                topUpValue = request.POST.get("topUpValue")
                loggedInRep = ClubRep.objects.get(username = request.session['username'])
                loggedInRep.credit = loggedInRep.credit + round(float(topUpValue), 2)
                loggedInRep.save()
            return render(request, "uweflix/topup.html")
        else:
            
            return redirect('home')    
    else:
        return redirect('home')

"""class PaymentView(TemplateView):
    model = Showing
    template_name = "uweflix/payment.html"
    form_class = PaymentForm
    success_url = ""

    def form_valid(self, form):
        print("Success")
        return super().form_valid(form)

    def get_queryset(self):
        object_list = Showing.objects.filter(id=1)
        return object_list

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context['showing'] = Showing.objects.filter(id=1)
        return context"""

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
