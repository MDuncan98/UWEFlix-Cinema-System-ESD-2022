from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import ContextPopException
from django.views.generic import *
from .models import *
from django.utils.timezone import datetime
from .forms import PaymentForm

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
        un = request.POST.get('username') #Gets Username
        pw = request.POST.get('password') # Gets Password
        try:
            acc = Account.objects.get(username=un)  # Get account from database
            if (acc.password == pw):  # If entered password matches one from account object
                if (acc.account_type == 'cm'):  # Cinema Manager
                    return render(request, 'uweflix/add_film.html')
                if (acc.account_type == 'am'):  # Accounts Manager
                    return render(request, 'uweflix/view_accounts.html')
                if (acc.account_type == 'cr'):  # Cinema Manager
                    return render(request, 'uweflix/viewings.html')
                if (acc.account_type == 'st'):  # Student
                    return render(request, 'uweflix/viewings.html')
        except:
            #More useful error message to be shown to user can be added
            print("error")
    return render(request, 'uweflix/login.html')

def payment(request): # Will also take showing_id as a param once showing page is completed!
    showing = Showing.objects.filter(id=1)
    customer = Customer.objects.filter(account_ptr_id=5)
    form = PaymentForm()
    context = {
        "show_showing": showing,
        "customer_data": customer,
        "form": form
    }
        #   PROCEED with payment function:
        #   tr = NEW Transaction object, date = today, customer = cust, cost = cost
        #   IF child/student/adult tickets > 0
        #       FOR each ticket type
        #           CREATE new ticket object, ticket_type x, transaction tr
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            print("Success")
            # GET Account data
            # IF paying with credit
            #   IF acc_balance >= total cost
            #       PROCEED with payment (true)
            #   ELSE
            #       ERROR(Not enough credit!)
            # ELIF paying later (club rep), or paying on the day
            #   PROCEED with payment (false)
            # Payment Logic will go here once prerequestites are completed
            return render(request, "uweflix/thanks.html")
        else:
            return render(request, 'uweflix/payment.html', context={'form':form, "show_showing": showing, "customer_data": customer})
            
    return render(request, 'uweflix/payment.html', context)

def thanks(request):
    render(request, "uweflix/thanks.html")

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
