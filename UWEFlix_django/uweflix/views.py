from multiprocessing import context
from sys import float_repr_style
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import ContextPopException
from django.views.generic import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
#from uweflix.decorators import unauthenticated_user
from .models import *
from django.utils.timezone import datetime
from .forms import *
#from .decorators import unauthenticated_user
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import Group
from django.contrib import messages




def home(request):
    return render(request, 'uweflix/index.html')

def am_home(request):
    return render(request, 'uweflix/am_home.html')

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


def registerPage(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            group=Group.objects.get(name='Student')
            user=form.save()
            group.user_set.add(user)

    context = {'form':form}
    return render(request, 'uweflix/register.html', context)

def register_clubrep(request):
    userForm = CustomUserCreationForm()
    crForm = RegisterClubRepForm()
    context = {'user_form': userForm,
               'cr_form': crForm}
    if request.method == "POST":
        userForm = CustomUserCreationForm(request.POST)
        crForm = RegisterClubRepForm(request.POST)
        if userForm.is_valid():
            if crForm.is_valid():
                newUser = userForm.save()
                club = crForm.cleaned_data['club']
                crNum = crForm.cleaned_data['club_rep_num']
                dob = crForm.cleaned_data['dob']
                ClubRep.objects.create(user=newUser, club=club, club_rep_num=crNum, dob=dob)
                print("yes")
            else:
                print("cr no")
        else:
            print("user no")
    return render(request, 'uweflix/register_cr.html', context)

#@unauthenticated_user
def login(request):
    if request.method == 'POST':
        un = request.POST['username'] #Gets Username
        pw = request.POST['password'] #Gets Password
        user = authenticate(username=un, password=pw)
        if user is not None:
            if user.groups.filter(name='Student').exists():
                return render (request, "uweflix/student_home.html")
            elif user.groups.filter(name='Club Rep').exists():
                return render (request, "uweflix/club_rep_home.html")
            elif user.groups.filter(name='Account Manager').exists():
                return render (request, "uweflix/am_home.html")
            elif user.groups.filter(name='Cinema Manager').exists():
                return render (request, "uweflix/Cinema_manager_home.html")
        else:
            messages.error(request, "Bad Credentials")
    return render(request, "uweflix/logIn.html")

def logout(request):
    return render(request, 'uweflix/logout.html')

def userpage(request):
    context = {}
    return render(request, 'uweflix/user.html', context)

def payment(request): # Will also take showing_id as a param once showing page is completed!
    showing = Showing.objects.get(id=1)
    customer = Customer.objects.filter(id=1)
    form = PaymentForm()
    context = {
        "showing": showing,
        "customer_data": customer,
        "form": form
    }
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            total_cost = float(form["total_cost"].data)
            adult_tickets = int(form["adult_tickets"].data)
            student_tickets = int(form["student_tickets"].data)
            child_tickets = int(form["child_tickets"].data)
            total_tickets = adult_tickets + student_tickets + child_tickets
            payment_option = form.cleaned_data.get("payment_options")
            if showing.remaining_tickets < total_tickets: #If there is NOT enough tickets
                print("Not enough tickets remaining to make this booking.")
            else:
                if 'accountType' in request.session:  # If signed in
                    #print(form.cleaned_data.get("payment_options"))
                    if (request.session['accountType'] == "st" or request.session['accountType'] == "cr"):
                        #Club reps and students
                        user = Customer.objects.get(username=request.session['username'])
                    if payment_option == 'credit' and user.credit >= total_cost: # If paying with credit
                        user.credit -= total_cost
                        user.save()
                        paying = True
                    elif request.session['accountType'] == "cr" and payment_option == "tab":
                        paying = False
                    else:
                        return redirect("/error/")
                elif payment_option == "nopay":
                    user = None
                    paying = False
                else:
                    return render(request, "uweflix/error.html")
                new_transaction = Transaction.objects.create(customer=user, date=datetime.today(), cost=total_cost, is_settled=paying)
                for i in range(adult_tickets):
                    Ticket.objects.create(transaction=new_transaction, showing=showing, ticket_type="adult")
                for i in range(student_tickets):
                    Ticket.objects.create(transaction=new_transaction, showing=showing, ticket_type="student")
                for i in range(child_tickets):
                    Ticket.objects.create(transaction=new_transaction, showing=showing, ticket_type="child")
                showing.remaining_tickets -= (adult_tickets + student_tickets + child_tickets)
                showing.save()
                print("Success")
                return render(request, "uweflix/thanks.html")
        else:
            return render(request, 'uweflix/payment.html', context={'form':form, "show_showing": showing, "customer_data": customer})

    return render(request, 'uweflix/payment.html', context)

def thanks(request):
    render(request, "uweflix/thanks.html")

def error(request):
    render(request, "uweflix/error.html")

def topup(request):
    if 'accountType' in request.session:
        if request.session['accountType'] == "cr":
            userObject = ClubRep
        elif request.session['accountType'] == "st":
            userObject = Customer
        else:
            return redirect('home') 
        if request.method == 'POST':
            topUpValue = request.POST.get("topUpValue")
            loggedInRep = userObject.objects.get(username = request.session['username'])
            loggedInRep.credit = loggedInRep.credit + round(float(topUpValue), 2)
            loggedInRep.save()
        return render(request, "uweflix/topup.html")   
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

def transaction_test(request):
    if request.method == "GET":
        customer = Customer.objects.get(id=1)
        transaction = Transaction.newTransaction(customer, 15.00, False)
        print(f"Transaction number {transaction.id} created.")
        transaction2 = Transaction.getTransaction(transaction.id)
        print(f"Transaction number {transaction2.id} retrieved.")
        print(f"Old Transaction details: {transaction2.cost}, {transaction2.is_settled}.")
        transaction2 = Transaction.updateTransaction(transaction2.id, 20.00, True)
        print(f"New Transaction details: {transaction2.cost}, {transaction2.is_settled}.")
        Transaction.deleteTransaction(transaction2.id)
        print(f"Transaction deleted.")
    return render(request, "uweflix/transaction_test.html")

#def addClub(request):#
#    context = {}
#    form = addClubForm(request.POST or None)

#    if request.method == "POST":
#        if form.is_valid():
#            form.save()
#            messages.success(request, "Club successfully registered.")
#            return redirect('/addFilm')

#    context['form'] = form
#    return render(request, "Uweflix/addClub.html", context)

#@allowed_users(allowed_roles=['cinemaManagers'])
#def addRep(request):
#    context = {}
#    form = addRepForm(request.POST or None)

#    if request.method == "POST":
#        if form.is_valid():
#            user = form.save(commit=False)

#            user.save()

#            user_group = Group.objects.get(name="studentReps")
#            user.groups.add(user_group)

#            messages.success(request, "Rep successfully added.")
#            return redirect('/addRep')

#    context['form'] = form
#    return render(request, "Uweflix/addRep.html", context)
