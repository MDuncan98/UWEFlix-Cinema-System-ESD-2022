from multiprocessing import context
from sys import float_repr_style
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import ContextPopException
from django.views.generic import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
import calendar
#from uweflix.decorators import unauthenticated_user
from .models import *
from datetime import datetime as dt
from .forms import *
#from .decorators import unauthenticated_user
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages


def home(request):
    return render(request, 'uweflix/index.html')

def am_home(request):
    return render(request, 'uweflix/am_home.html')

def club_rep_home(request):
    return render(request, 'uweflix/club_rep_home.html')

def cinema_manager_home(request):
    return render(request, 'uweflix/cinema_manager_home.html')

def student_home(request):
    return render(request, 'uweflix/student_home.html')

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


def registerPage(request):
    form = CustomUserCreationForm()
    customer_form = RegisterStudentForm()
    context = {
        'form': form,
        'customer_form': customer_form
    }
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        customer_form = RegisterStudentForm(request.POST)
        if form.is_valid():
            if customer_form.is_valid():
                dob = customer_form.cleaned_data['dob']
                user=form.save()
                #user.is_active = False
                student = Customer.objects.create(user=user, dob=dob)
                group=Group.objects.get(name='Student')
                group.user_set.add(user)
                return render(request, 'uweflix/index.html')
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
            request.session['user_id'] = user.id
            if user.groups.filter(name='Student').exists():
                request.session['user_group'] = "Student"
                request.session['credit'] = Customer.objects.get(user=user.id).credit
                return render (request, "uweflix/student_home.html")
            elif user.groups.filter(name='Club Rep').exists():
                request.session['user_group'] = "Club Rep"
                request.session['credit'] = ClubRep.objects.get(user=user).credit
                return render (request, "uweflix/club_rep_home.html")
            elif user.groups.filter(name='Account Manager').exists():
                request.session['user_group'] = "Account Manager"
                return render (request, "uweflix/am_home.html")
            elif user.groups.filter(name='Cinema Manager').exists():
                request.session['user_group'] = "Cinema Manager"
                return render (request, "uweflix/Cinema_manager_home.html")
        else:
            messages.error(request, "Bad Credentials")
    return render(request, "uweflix/login.html")

def logout(request):
    try:
        del request.session['user_id']
        del request.session['user_group']
        del request.session['credit']
    except KeyError:
        pass
    finally:
        return redirect("/login/")

def userpage(request):
    context = {}
    return render(request, 'uweflix/user.html', context)

def payment(request, showing): # Will also take showing_id as a param once showing page is completed!
    showing = Showing.objects.get(id=showing)
    #customer = Customer.objects.filter(id=1)
    form = PaymentForm()
    context = {
        "showing": showing,
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
                return render(request, "uweflix/error.html")
            else:
                if 'user_id' in request.session:  # If signed in
                    user_type = request.session['user_group']
                    #print(form.cleaned_data.get("payment_options"))
                    if (user_type == "Student" or user_type == "Club Rep"):
                        #Club reps and students
                        user = Customer.objects.get(user=request.session['user_id'])
                    if payment_option == 'credit' and user.credit >= total_cost: # If paying with credit
                        user.credit -= total_cost
                        request.session['credit'] = user.credit
                        user.save()
                        paying = True
                    elif user_type == "Club Rep" and payment_option == "tab" or payment_option == "nopay":
                        paying = False
                    else:
                        return render(request, "uweflix/error.html")
                elif payment_option == "nopay":
                    user = None
                    paying = False
                else:
                    return render(request, "uweflix/error.html")
                new_transaction = Transaction.objects.create(customer=user, date=dt.today(), cost=total_cost, is_settled=paying)
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
            return render(request, 'uweflix/payment.html', context={'form':form, "show_showing": showing})

    return render(request, 'uweflix/payment.html', context)

def thanks(request):
    render(request, "uweflix/thanks.html")

def error(request):
    render(request, "uweflix/error.html")

def topup(request):
    if 'user_group' in request.session:
        if request.session['user_group'] == "Club Rep":
            userObject = ClubRep
        elif request.session['user_group'] == "Student":
            userObject = Customer
        else:
            return redirect('home') 
        if request.method == 'POST':
            topUpValue = request.POST.get("topUpValue")
            loggedInRep = userObject.objects.get(user = request.session['user_id'])
            loggedInRep.credit = loggedInRep.credit + round(float(topUpValue), 2)
            request.session['credit'] = loggedInRep.credit
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
            date__year = dt.now().year,
            date__month = dt.now().month
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)
        return context

def set_payment_details(request):
    form = AccessClubForm()
    context = {'form': form}
    if request.method == "POST":
        form = AccessClubForm(request.POST)
        if form.is_valid():
            club_id = form.cleaned_data['club']
            club_obj = Club.objects.get(id=club_id)
            club_obj.card_number = form.cleaned_data['card_number']
            month = form.cleaned_data['expiry_month']
            year = form.cleaned_data['expiry_year']
            formatted_date = f"{year}-{month}-{calendar.monthrange(int(year), int(month))[1]}"
            club_obj.card_expiry_date = formatted_date
            club_obj.save()
    return render(request, "uweflix/set_payment.html", context)

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
