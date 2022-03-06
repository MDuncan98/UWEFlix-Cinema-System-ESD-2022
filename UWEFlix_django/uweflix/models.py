from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    account_type = models.CharField(max_length=2)
    """Account types:
        - cm = Cinema Manager
        - am = Accounts Manager
        - cr = Club Representative"""

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
   


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField('Date of birth')
    email = models.EmailField()
    password = models.CharField(max_length=50)

class ClubRep(Customer):
    club_rep_num = models.CharField(max_length=50)


# Create your models here.
