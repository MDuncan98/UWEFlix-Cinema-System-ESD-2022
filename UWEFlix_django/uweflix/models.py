from django.db import models

class Account(models.Model):  # Database for storing user account information
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    account_type = models.CharField(max_length=2)
    """Account types:
        - cm = Cinema Manager
        - am = Accounts Manager
        - cr = Club Representative
        - st = Student"""

class Customer(Account):  # Student accounts
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField('Date of birth')
    email = models.EmailField()
    is_validated = models.BooleanField(default=0)
    credit = models.FloatField(default=0.00)

class Transaction(models.Model):  # Database for storing all of the 'accounts' to be analysed by Account Manager
    # transaction_id = order/reference number
    customer = models.ForeignKey(Customer, default=1, on_delete=models.SET_DEFAULT)  # User responsible for the transaction
    date = models.DateField()  # Date of transaction
    cost = models.FloatField()  # Cost of transaction
    is_settled = models.BooleanField()  # Whether the transaction has been paid

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
    
class Ticket(models.Model):  # Individual ticket booking database
    transaction = models.ForeignKey(Transaction, default=1, on_delete=models.SET_DEFAULT)
    # showing = models.ForeignKey(Showing, default=1, on_delete=models.SET_DEFAULT)  # Screen the booking is being viewed at
    ticket_type = models.CharField(max_length=7)


class ClubRep(Customer):
    club_rep_num = models.CharField(max_length=50)

    """def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)"""


# Create your models here.
