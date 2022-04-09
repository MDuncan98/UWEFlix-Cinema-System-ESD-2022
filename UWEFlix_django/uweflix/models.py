from email import charset
from pyexpat import model
from tokenize import String
from xml.dom.minidom import CharacterData
from django.db import models
from django.contrib.auth.models import *
import datetime

class User(AbstractUser):
    pass

class Customer(models.Model):  # Student accounts
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField('Date of birth')
    credit = models.FloatField(default=0.00)

class Transaction(models.Model):  # Database for storing all of the 'accounts' to be analysed by Account Manager
    customer = models.ForeignKey(Customer, blank=True, null=True, default=None, on_delete=models.SET_DEFAULT)  # User responsible for the transaction
    date = models.DateField()  # Date of transaction
    cost = models.FloatField()  # Cost of transaction
    is_settled = models.BooleanField()  # Whether the transaction has been paid

    def newTransaction(cust, cost, is_paid): #CREATE
        try:
            transaction = Transaction.objects.create(customer=cust, date=datetime.today(), cost=cost, is_settled=is_paid)
            return transaction
        except:
            print("Transaction object could not be created.")

    def getTransaction(id): #READ
        try:
            transaction = Transaction.objects.get(id=id)
            return transaction
        except:
            print("No transaction exists with that transaction ID.")

    def updateTransaction(id, *transaction_data): #UPDATE
        try:
            for data_item in transaction_data:
                if isinstance(data_item, Customer):
                    Transaction.objects.filter(pk=id).update(customer=data_item)
                elif isinstance(data_item, datetime.date):
                    Transaction.objects.filter(pk=id).update(date=data_item)
                elif isinstance(data_item, float):
                    Transaction.objects.filter(pk=id).update(cost=data_item)
                elif isinstance(data_item, bool):
                    Transaction.objects.filter(pk=id).update(is_settled=data_item)
                else:
                    print(f"Data item {data_item} does not conform to any of the required input types." +
                    "\nThis value could not be updated.")
            return Transaction.objects.get(id=id)
        except:
            print("An error occurred when updating this object.")

    def deleteTransaction(id): #DELETE
        try:
            transaction = Transaction.objects.get(id=id)
            transaction.delete()
        except:
            print("This transaction does not exist, or had an issue being deleted.")

class Film(models.Model):
    title = models.CharField(max_length=100)
    age_rating = models.CharField(max_length=3)
    """Age Ratings:
        - U
        - PG
        - 12
        - 12A
        - 15
        - 18"""
    duration = models.CharField(max_length=3)
    # Store duration in minutes only (e.g. 120)
    trailer_desc = models.CharField(max_length=500)

    def __str__(self):
        return self.title

    def newShowing(screen, film, ticketsLeft, socialDis):#CREATE
        try:
            showing = Showing.objects.create(screen=screen, film=film, time=datetime.today, remaining_tickets=ticketsLeft, apply_covid_restrictions=False)
            return showing
        except:
            print("Showing object could not be created")

    def getShowing(id):#READ
        try:
            showing = showing.object.get(id=id)
            return showing
        except:
            print("No showing exists with that showing ID.")

    def filmShowing(id, *showing_data): #UPDATE
        try:
            for data_item in showing_data:
                if isinstance(data_item, Screen):
                    Showing.objects.filter(pk=id).update(screen=data_item)
                elif isinstance(data_item, Film):
                    Showing.objects.filter(pk=id).update(film=data_item)
                elif isinstance(data_item, float):
                    Showing.object.filter(pk=id).update(time=data_item)
                elif isinstance(data_item, int):
                    Showing.objects.filter(pk=id).update(remaining_tickets=data_item)
                elif isinstance(data_item, bool):
                    Showing.objects.filter(pk=id).update(apply_covid_restrictions=False)
                else:
                    print(f"Data item {data_item} does not confrom to any of the  required input types." +
                          "\nThis value could not be updated.")
            return Showing.objects.get(id=id)
        except:
            print("An error occurred when updating this object.")

    def deleteShowing(id): #DELETE
        try:
            showing = showing.objects.get(id=id)
            showing.delete()
        except:
            print("This film Showing has Successfully been deleted.")

class Screen(models.Model):
    capacity = models.IntegerField()
    apply_covid_restrictions =  models.BooleanField()

    def newScreen(seats, covidRestrictions): #Create
        try:
            screen = Screen.objects.create(capacity=seats, apply_covid_restrictions=covidRestrictions)
            return screen
        except:
            print("Screen cannot be created, perhaps you are missing some parameters?")

    def getScreen(id): #Read
        try:
            screen = Screen.objects.get(id=id)
            return screen
        except:
            print("Screen cannot be found, perhaps you have entered an incorrect id?")

    def updateScreen(id, fieldToEdit): #Update
        try:
            for field in fieldToEdit:
                if isinstance(field, int):
                    Screen.objects.filter(id=id).update(capacity=field)
                elif isinstance(field, bool):
                    Screen.objects.filter(id=id).update(apply_covid_restrictions=field)
            return Screen.objects.get(id=id)
        except:
            print("Screen cannot be found, perhaps you have entered an invalid field type?")

    def removeScreen(id): #Delete
        try:
            screen = Screen.objects.get(id=id)
            screen.delete()
        except:
            print("Screen cannot be found, perhaps you have entered an incorrect id?")

class Showing(models.Model):
    screen = models.ForeignKey(Screen, default=1, on_delete=models.CASCADE)
    film = models.ForeignKey(Film,on_delete=models.CASCADE)
    time = models.DateTimeField()
    remaining_tickets = models.IntegerField(default=150)  # NEEDS TO BE ASSIGNED TO THE SCREEN CAPACITY SOMEHOW!

    def newShowing(screen, film, ticketsLeft, socialDis):#CREATE
        try:
            showing = Showing.objects.create(screen=screen, film=film, time=datetime.today, remaining_tickets=ticketsLeft, apply_covid_restrictions=False)
            return showing
        except:
            print("Showing object could not be created")

    def getShowing(id):#READ
        try:
            showing = showing.object.get(id=id)
            return showing
        except:
            print("No showinf exists with that showing ID.")

    def filmShowing(id, *showing_data): #UPDATE
        try:
            for data_item in showing_data:
                if isinstance(data_item, Screen):
                    Showing.objects.filter(pk=id).update(screen=data_item)
                elif isinstance(data_item, Film):
                    Showing.objects.filter(pk=id).update(film=data_item)
                elif isinstance(data_item, float):
                    Showing.object.filter(pk=id).update(time=data_item)
                elif isinstance(data_item, int):
                    Showing.objects.filter(pk=id).update(remaining_tickets=data_item)
                elif isinstance(data_item, bool):
                    Showing.objects.filter(pk=id).update(apply_covid_restrictions=False)
                else:
                    print(f"Data item {data_item} does not confrom to any of the  required input types." +
                          "\nThis value could not be updated.")
            return Showing.objects.get(id=id)
        except:
            print("An error occurred when updating this object.")

    def deleteShowing(id): #DELETE
        try:
            showing = showing.objects.get(id=id)
            showing.delete()
        except:
            print("This film Showing has Successfully been deleted.")


class Ticket(models.Model):  # Individual ticket booking database
    transaction = models.ForeignKey(Transaction, default=1, on_delete=models.SET_DEFAULT)
    showing = models.ForeignKey(Showing, default=1, on_delete=models.SET_DEFAULT)  # Screen the booking is being viewed at
    ticket_type = models.CharField(max_length=7)

    def newTicket(trans, show, type): #Create
        try:
            ticket = Ticket.objects.create(transaction=trans, showing=show, ticket_type=type)
            return ticket
        except:
            print("Ticket cannot be created, perhaps you are missing a parameter?")

    def getTicket(id): #Read
        try:
            ticket = Ticket.objects.get(id=id)
            return ticket
        except:
            print("Ticket cannot be found, perhaps you have entered an incorrect id?")

    def updateTicket(id, fieldToEdit): #Update
        try:
            for field in fieldToEdit:
                if isinstance(field, Transaction):
                    Ticket.objects.filter(id=id).update(transaction=field)
                elif isinstance(field, Showing):
                    Ticket.objects.filter(id=id).update(showing=field)
                elif isinstance(field, String):
                    Ticket.objects.filter(id=id).update(ticket_type=field)
            return Ticket.objects.get(id=id)
        except:
            print("Ticket cannot be updated, perhaps you have entered an invalid field type?")

    def removeTicket(id): #Delete
        try:
            ticket = Ticket.objects.get(id=id)
            ticket.delete()
        except:
            print("Ticket cannot be found, perhaps you have entered an invalid id?")


class Club(models.Model):
    name = models.CharField(max_length=100)
    #Address details
    street_number = models.IntegerField()
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    post_code = models.CharField(max_length=8)
    #Contact details
    landline_number = models.CharField(max_length=11)
    mobile_number = models.CharField(max_length=11)
    email = models.EmailField()
    #Payment details
    card_number = models.IntegerField(blank=True, null=True)
    card_expiry_date = models.DateField(blank=True, null=True)
    discount_rate = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def newClub(name, card_number, card_expiry_date, discount_rate): #Create
        try:
            club = Club.objects.create(name=name, card_number=card_number, card_expiry_date=card_expiry_date, discount_rate=discount_rate)
            return club
        except:
            print("Club can't be created")

    def getClub(id): #Read
        try:
            club = Club.objects.get(id=id)
            return club
        except:
            print("Club can't be found")

    def updateClub(id, *club_data): #Update
        try:
            for data_item in club_data:
                if data_item == 'name':
                    Club.objects.filter(id=id).update(name=data_item)
                elif data_item == 'card_number':
                    Club.objects.filter(id=id).update(card_number=data_item)
                elif data_item == 'card_expiry_date':
                    Club.objects.filter(id=id).update(card_expiry_date=data_item)
                elif data_item == 'discount_rate':
                    Club.objects.filter(id=id).update(discount_rate=data_item)
            return Club.objects.filter(id=id)
        except:
           print(f"Data item {data_item} does not conform to any of the required input types." +
                    "\nThis value could not be updated.")

    def removeClub(id): #Delete
        try:
            club = Club.objects.get(id=id)
            club.delete()
        except:
            print("Club can't be found, therefore can't be deleted")


class ClubRep(Customer):
    club = models.ForeignKey(Club, null=True, on_delete=models.CASCADE)
    club_rep_num = models.CharField(max_length=8)
    #first_name = models.CharField(max_length=30)
    #last_name = models.CharField(max_length=30)
    #dob1 = models.DateField(("dob"), default=datetime.date.today)
    #"A unique Club Representative number and unique password is allocated to the
    #Club Representative."
    #Therefore:
    #- Unique CR number = username (inherited from User model), ensure that username is numbers only
    #- Unique CR password = password (inherited from User model)
# Create your models here.

