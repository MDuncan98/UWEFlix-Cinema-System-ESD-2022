from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField('Date of birth')
    email = models.EmailField()
    password = models.CharField(max_length=50)

class ClubRep(Customer):
    club_rep_num = models.CharField(max_length=50)


# Create your models here.
