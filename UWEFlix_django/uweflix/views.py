from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import ContextPopException
from django.views.generic import *
from django import forms
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
    showing = Showing.objects.get(id=1)
    customer = Customer.objects.filter(account_ptr_id=5)
    form = PaymentForm()
    context = {
        "showing": showing,
        "customer_data": customer,
        "form": form
    }
        #   PROCEED with payment function:
        #   tr = NEW Transaction object, date = today, customer = cust, cost = cost
        #   IF child/student/adult tickets > 0
        #       FOR each ticket type
        #           CREATE new ticket object, ticket_type x, transaction tr
    if request.method == 'POST':
        POST = request.POST.copy()
        form = PaymentForm(request.POST)
        if form.is_valid():
            if 'accountType' in request.session:
                #print(form.cleaned_data.get("payment_options"))
                if (request.session['accountType'] == "st" or request.session['accountType'] == "cr") and form.cleaned_data.get("payment_options") == 'credit':
                    #Club reps and students paying with credit
                    user = Customer.objects.get(username=request.session['username'])
                    total_cost = float(form["total_cost"].data)
                    if user.credit >= total_cost:
                        print("Transaction can be made")
                        user.credit -= total_cost
                        adult_tickets = int(form["adult_tickets"].data)
                        student_tickets = int(form["student_tickets"].data)
                        child_tickets = int(form["child_tickets"].data)
                        new_transaction = Transaction.objects.create(customer=user, date=datetime.today(), cost=total_cost, is_settled=True)
                        for i in range(adult_tickets):
                            Ticket.objects.create(transaction=new_transaction, showing=showing, ticket_type="adult")
                        for i in range(student_tickets):
                            Ticket.objects.create(transaction=new_transaction, showing=showing, ticket_type="student")
                        for i in range(child_tickets):
                            Ticket.objects.create(transaction=new_transaction, showing=showing, ticket_type="child")
                        showing.remaining_tickets -= (adult_tickets + student_tickets + child_tickets)
                        showing.save()
                        user.save()
                        print("Success")
                        return render(request, "uweflix/thanks.html")
                    else:
                        return render(request, "uweflix/error.html")
                elif (request.session['accountType'] == "cr" and form.cleaned_data.get("payment_options") == 'tab'):  # Club rep pay in advance
                    user = Customer.objects.get(username=request.session['username'])
                    total_cost = float(form["total_cost"].data)
                    adult_tickets = int(form["adult_tickets"].data)
                    student_tickets = int(form["student_tickets"].data)
                    child_tickets = int(form["child_tickets"].data)
                    new_transaction = Transaction.objects.create(customer=user, date=datetime.today(), cost=total_cost, is_settled=False)
                    for i in range(adult_tickets):
                        Ticket.objects.create(transaction=new_transaction, showing=showing, ticket_type="adult")
                    for i in range(student_tickets):
                        Ticket.objects.create(transaction=new_transaction, showing=showing, ticket_type="student")
                    for i in range(child_tickets):
                        Ticket.objects.create(transaction=new_transaction, showing=showing, ticket_type="child")
                    showing.remaining_tickets -= (adult_tickets + student_tickets + child_tickets)
                    showing.save()
                    user.save()
                    print("Success")
                    return render(request, "uweflix/thanks.html")
                elif (form.cleaned_data.get("payment_options") == 'nopay'):  # Not working yet
                    total_cost = float(form["total_cost"].data)
                    adult_tickets = int(form["adult_tickets"].data)
                    student_tickets = int(form["student_tickets"].data)
                    child_tickets = int(form["child_tickets"].data)
                    new_transaction = Transaction.objects.create(date=datetime.today(), cost=total_cost, is_settled=False)
                    for i in range(adult_tickets):
                        Ticket.objects.create(transaction=new_transaction, showing=showing, ticket_type="adult")
                    for i in range(student_tickets):
                        Ticket.objects.create(transaction=new_transaction, showing=showing, ticket_type="student")
                    for i in range(child_tickets):
                        Ticket.objects.create(transaction=new_transaction, showing=showing, ticket_type="child")
                    showing.remaining_tickets -= (adult_tickets + student_tickets + child_tickets)
                    showing.save()
        else:
            return render(request, 'uweflix/payment.html', context={'form':form, "show_showing": showing, "customer_data": customer})
            
    return render(request, 'uweflix/payment.html', context)

def thanks(request):
    render(request, "uweflix/thanks.html")

def error(request):
    render(request, "uweflix/payment/error.html")

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
