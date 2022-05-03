from multiprocessing import context
from sys import float_repr_style
from urllib import request
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
from django.http import Http404
from django.utils import timezone


def home(request):
    return render(request, 'uweflix/index.html')

def am_home(request):
    transactions = Transaction.objects.filter(date = dt.today())
    transactions = transactions.count()
    context = {
        'transactions': transactions
    }
    return render(request, 'uweflix/am_home.html', context)

def club_rep_home(request):
    return render(request, 'uweflix/club_rep_home.html')

def cinema_manager_home(request):
    #if request.user.is_authenticated:
        if request.session['user_group'] == "Cinema Manager":
            context = {}
            restrictions = Screen.objects.first().apply_covid_restrictions
            context = {
                'restrictions_bool' : restrictions
            }
            if request.method == "POST":
                for screen in Screen.objects.all():
                    Screen.updateScreen(screen.id, not screen.apply_covid_restrictions)
                    context = {
                        'restrictions_bool' : screen.apply_covid_restrictions
                    }
            return render(request, 'uweflix/cinema_manager_home.html', context)
        else:
            return redirect('/')
    #else:
        #return redirect('/')

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
                try:
                    image = request.FILES.get('image')
                    film.image = image
                except:
                    pass
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
                user.is_active = False
                student = Customer.objects.create(user=user, dob=dob)
                group=Group.objects.get(name='Student')
                group.user_set.add(user)
                return render(request, 'uweflix/viewings.html')
    return render(request, 'uweflix/register.html', context)

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
                return render (request, "uweflix/cinema_manager_home.html")
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

def payment(request, showing):
    showing = Showing.getShowing(id=showing)
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
                    if (user_type == "Student" or user_type == "Club Rep"):
                        #Club reps and students
                        user = Customer.objects.get(user=request.session['user_id'])
                        if payment_option == 'credit' and user.credit >= total_cost: # If paying with credit
                            user.credit -= total_cost
                            request.session['credit'] = user.credit
                            user.save()
                            paying = True
                        elif user_type == "Club Rep" and payment_option == "tab":
                            paying = False
                        elif payment_option == "nopay":
                            return redirect(f'/pay_with_card/?user={user.id}&cost={total_cost}&adult={adult_tickets}&student={student_tickets}&child={child_tickets}&showing={showing.id}')
                        else:
                            context = {'error': "Credit error: You do not have sufficient credit to make this order, please add funds and try again."}
                            return render(request, "uweflix/error.html", context)
                    else:
                        context = {'error': "Account based error: Your account type is not permitted to purchase tickets. Please change accounts and try again."}
                        return render(request, "uweflix/error.html", context)
                elif payment_option == "nopay":  # Regular customer pays with card
                    print("hello")
                    return redirect(f'/pay_with_card/?user={0}&cost={total_cost}&adult={adult_tickets}&student={student_tickets}&child={child_tickets}&showing={showing.id}')
                else:
                    context = {'error': "As a regular customer, you may only make purchases via credit card. Please go back and select this option."}
                    return render(request, "uweflix/error.html", context)
                new_transaction = Transaction.newTransaction(user, total_cost, paying)
                for i in range(adult_tickets):
                    Ticket.newTicket(new_transaction, showing, "adult")
                for i in range(student_tickets):
                    Ticket.newTicket(new_transaction, showing, "student")
                for i in range(child_tickets):
                    Ticket.newTicket(new_transaction, showing, "child")
                showing.remaining_tickets -= (adult_tickets + student_tickets + child_tickets)
                showing.save()
                request.session['screen'] = showing.screen.id
                request.session['transaction'] = new_transaction.id
                request.session['film'] = showing.film.title
                request.session['age_rating'] = showing.film.age_rating
                request.session['date'] = showing.time.strftime("%d/%m/%y")
                request.session['time'] = showing.time.strftime("%H:%M")
                request.session['successful_purchase'] = True
                return redirect('/thanks')
        else:
            return render(request, 'uweflix/payment.html', context={'form':form, "showing": showing})
    return render(request, 'uweflix/payment.html', context)

def pay_with_card(request):
    form = CardPaymentForm()
    context = {
        'user': request.GET.get('user'),
        'cost': request.GET.get('cost'),
        'adult': request.GET.get('adult'),
        'student': request.GET.get('student'),
        'child': request.GET.get('child'),
        'showing': request.GET.get('showing'),
        'form':form
    }
    if request.method=="POST":
        form = CardPaymentForm(request.POST)
        if form.is_valid():
            id = int(context['user'])
            user=None
            if id == 0:
                pass
            else:
                user= Customer.objects.get(id= context['user'])
            total_cost = float(context['cost'])
            adult_tickets = int(context['adult'])
            child_tickets = int(context['child'])
            student_tickets = int(context['student'])
            showing = Showing.getShowing(int(context['showing']))
            new_transaction = Transaction.newTransaction(user, total_cost, True)
            for i in range(adult_tickets):
                Ticket.newTicket(new_transaction, showing, "adult")
            for i in range(student_tickets):
                Ticket.newTicket(new_transaction, showing, "student")
            for i in range(child_tickets):
                Ticket.newTicket(new_transaction, showing, "child")
            showing.remaining_tickets -= (adult_tickets + student_tickets + child_tickets)
            showing.save()
            request.session['screen'] = showing.screen.id
            request.session['transaction'] = new_transaction.id
            request.session['film'] = showing.film.title
            request.session['age_rating'] = showing.film.age_rating
            request.session['date'] = showing.time.strftime("%d/%m/%y")
            request.session['time'] = showing.time.strftime("%H:%M")
            request.session['successful_purchase'] = True
            return redirect('/thanks')
        else: return render(request,"uweflix/pay_with_card.html",{'form':form})

    return render(request,"uweflix/pay_with_card.html",context)

    """Form that takes 16 digit card number, expiry date, security code.
    If form is valid, do code below."""

    """new_transaction = Transaction.newTransaction(user, total_cost, paying)
                for i in range(adult_tickets):
                    Ticket.newTicket(new_transaction, showing, "adult")
                for i in range(student_tickets):
                    Ticket.newTicket(new_transaction, showing, "student")
                for i in range(child_tickets):
                    Ticket.newTicket(new_transaction, showing, "child")
                showing.remaining_tickets -= (adult_tickets + student_tickets + child_tickets)
                showing.save()
                request.session['screen'] = showing.screen.id
                request.session['transaction'] = new_transaction.id
                request.session['film'] = showing.film.title
                request.session['age_rating'] = showing.film.age_rating
                request.session['date'] = showing.time.strftime("%d/%m/%y")
                request.session['time'] = showing.time.strftime("%H:%M")
                request.session['successful_purchase'] = True
                return redirect('/thanks')"""
    return render(request, "uweflix/pay_with_card.html", context)

def thanks(request):
    if 'successful_purchase' not in request.session:
        raise Http404("Forbidden access to this page.")
    del request.session['successful_purchase']
    return render(request, "uweflix/thanks.html")

def error(request):
    return render(request, "uweflix/error.html")

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

def view_accounts(request):
    return render(request, "uweflix/view_accounts.html")

def daily_transactions(request):
    form = DatePickerForm()
    titleText = "Please select a day to view transactions for:"
    context = {
        'form': form,
        'title_text': titleText}
    if request.method == "POST":
        form = DatePickerForm(request.POST)
        if form.is_valid():
            selectedDate = dt.today()
            if "search" in request.POST:
                selectedDate = form.cleaned_data['date']
            elif "today" in request.POST:
                selectedDate = dt.today()
            transaction_list = Transaction.objects.filter(date = selectedDate)
            if not transaction_list:
                titleText = f"There were no transactions made on {str(selectedDate)}"
                context = {
                    'form': form,
                    'title_text': titleText
                }
            else:
                context = {
                    'selected_date': selectedDate,
                    'transaction_list': transaction_list,
                    'form': form
                }
        return render(request, "uweflix/daily_transactions.html", context)
    else:
        return render(request, "uweflix/daily_transactions.html", context)

def customer_statements(request):
    form = SearchClubRepForm()
    context = {'form':form}
    if request.method == "POST":
        form = SearchClubRepForm(request.POST)
        if form.is_valid():
            clubrep = ClubRep.objects.get(club_rep_num=form.cleaned_data['clubrep_choice'])
            trange = form.cleaned_data['timerange_choice']
            if trange == 'Month':
                transaction_list = Transaction.objects.filter(
                    customer=clubrep,
                    date__year = dt.now().year,
                    date__month = dt.now().month
                )
            elif trange == "Year":
                transaction_list = Transaction.objects.filter(
                    customer=clubrep,
                    date__year = dt.now().year
                )
            context = {
                'club_rep_num': clubrep.club_rep_num,
                'transaction_list': transaction_list,
                'form': form
            }
        return render(request, 'uweflix/customer_statements.html', context)
    else:
        return render(request, 'uweflix/customer_statements.html', context)

def settle_payments(request):
    context = {}
    if request.session["user_group"] == "Club Rep":
        club_rep = ClubRep.objects.get(user_id=request.session["user_id"])
        transaction_list = Transaction.objects.filter(
                customer=club_rep,
                date__year = dt.now().year,
                date__month = dt.now().month,
                is_settled = False
            )
        context = {
            'transactions': transaction_list,
            'club_rep': club_rep.club_rep_num
            }
        if request.method == "POST":
            for transaction in transaction_list:
                #Need to discuss the 'paying' aspect of this.
                transaction.is_settled = True
                transaction.save()   
        return render(request, 'uweflix/settle_payments.html', context)
    else:
        return redirect('home')

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
        else:
            context = {'form': form}
    return render(request, "uweflix/set_payment.html", context)

def add_club(request):
    context = {}
    form = addClubForm()
    if request.method == "POST":
        form = addClubForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            clubName = form.cleaned_data['name']
            clubStreetNumber = form.cleaned_data['street_number']
            clubStreet = form.cleaned_data['street']
            clubCity = form.cleaned_data['city']
            clubPostcode = form.cleaned_data['post_code']
            clubLandlineNumber = form.cleaned_data['landline_number']
            clubMobileNumber = form.cleaned_data['mobile_number']
            clubEmail = form.cleaned_data['email']
            Club.newClub(clubName, clubStreetNumber, clubStreet, clubCity, clubPostcode, clubLandlineNumber, clubMobileNumber, clubEmail)
            messages.success(request, "Club successfully registered.")
            return redirect('/cinema_manager_home')

    context['form'] = form
    return render(request, "Uweflix/add_club.html", context)

def add_rep(request):
    context = {}
    userForm = ClubRepCreationForm()
    form = addRepForm()
    if request.method == "POST":
        userForm = ClubRepCreationForm(request.POST)
        form = addRepForm(request.POST)
        if userForm.is_valid():
            if form.is_valid():
                user = userForm.save(commit=False)
                dob = form.cleaned_data['dob']
                club = form.cleaned_data['club']
                clubRepNum = 1
                if ClubRep.objects.exists():
                    clubRepNum = int(ClubRep.objects.all().last().club_rep_num) + 1
                crUsername = ("%04d" % (clubRepNum,))
                user.username = crUsername
                user.save()
                newCr = ClubRep.objects.create(user=user, club=club, dob=dob, club_rep_num=clubRepNum)
                userGroup = Group.objects.get(name="Club Rep")
                user.groups.add(userGroup)
                request.session['new_cr'] = newCr.club_rep_num
                request.session['new_club'] = newCr.club.name
                request.session['successful_creation'] = True
                return redirect("/rep_success")
    context['form'] = form
    context['userform'] = userForm
    return render(request, "uweflix/add_rep.html", context)

def rep_success(request):
    if 'successful_creation' not in request.session:
        raise Http404("Forbidden access to this page.")
    del request.session['successful_creation']
    return render(request, "uweflix/rep_success.html")

def addClubAccount(request):
    """context = {}
    form = addClubAccountForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():

           form.save()

            #user_group = Group.objects.get(name="studentReps")
            #user.groups.add(user_group)

           messages.success(request, "Rep successfully added.")
           return redirect('/add_account')

    context['form'] = form"""
    return render(request, "Uweflix/add_account.html", context)

def review_students(request, userID):
    print(userID)
    students = User.objects.filter(is_active=False)
    studentChoice = students.first()
    if userID == 0 and studentChoice is not None:
        return redirect('review_students', userID=studentChoice.id)
    if userID != 0:
        studentChoice = User.objects.get(id = userID)
    context = {
        'students' : students,
        'chosenStudent' : studentChoice,
        'urlID' : userID
    }
    if (request.method == "POST"):
        name = request.POST.get('name')
        if name == "changeStudent":
            studentID = request.POST['ReviewStudentForm']
            studentChoice = User.objects.get(id = studentID)
            return redirect('review_students', userID=studentChoice.id)
        else:
            if name == "acceptStudent":
                User.objects.filter(id=userID).update(is_active=True)
            elif name == "denyStudent":
                studentChoice.delete()
            students = User.objects.filter(is_active=False)
            studentChoice = students.first()
            return redirect('review_students', userID=0)
    return render(request, "UweFlix/review_students.html", context)
def view_order_history(request):
    form = DateIntervalForm()
    titleText = "Please select a date range to view transactions for:"
    context = {
        'form': form,
        'title_text': titleText}
    if request.method == "POST":
        form = DateIntervalForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            transaction_list = Transaction.objects.filter(date__range = (startDate, endDate))
            if not transaction_list:
                titleText = f"There were no transactions made in your date range"
                context = {
                    'form': form,
                    'title_text': titleText
                }
            else:
                context = {
                    'start_date': startDate,
                    'end_date': endDate,
                    'transaction_list': transaction_list,
                    'form': form
                }
            form = DateIntervalForm()
        return render(request, "UweFlix/view_order_history.html", context)
    else:
        return render(request, "UweFlix/view_order_history.html", context)



def change_ticket_prices(request):
    form = ChangePriceForm()
    context = {
        'form':form
    }
    if request.method=="POST":
        form = ChangePriceForm (request.POST)
        if form.is_valid():
            Prices.changePrices(form.cleaned_data['adult'],form.cleaned_data['student'], form.cleaned_data['child'])
            adult,student,child=Prices.getCurrentPrices()
            print(adult)

def request_cancellation(request):
    now = timezone.now()
    user = None
    showingsToCancel = []
    adultTickets = []
    childTickets = []
    studentTickets = []
    if request.session["user_group"] == "Club Rep":
        user = ClubRep.objects.get(user_id=request.session["user_id"])
    elif request.session["user_group"] == "Student":
        user = Customer.objects.get(user=request.session["user_id"])
    if user is not None:
        transaction_list = Transaction.objects.filter(customer=user, request_to_cancel=False)
        for purchase in transaction_list:
            allTickets = Ticket.objects.filter(transaction=purchase)
            ticket = allTickets.first()
            if ticket is not None:
                showingTime = ticket.showing.time
                if showingTime > now:
                    showingsToCancel.append(ticket)
                    adultTickets.append(len(allTickets.filter(ticket_type="adult")))
                    childTickets.append(len(allTickets.filter(ticket_type="child")))
                    studentTickets.append(len(allTickets.filter(ticket_type="student")))
    zippedList = zip(showingsToCancel, adultTickets, childTickets, studentTickets)
    context = {
        'zipped': zippedList
    }
    if request.method == "POST":
        requestedTransaction = Transaction.objects.filter(id=request.POST.get('transaction_number'))
        requestedTransaction.update(request_to_cancel=True)
        return redirect('request_cancellation') 
    return render(request, "UweFlix/request_cancellation.html", context)

