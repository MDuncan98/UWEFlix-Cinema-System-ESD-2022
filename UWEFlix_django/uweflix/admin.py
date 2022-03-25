from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Account)
admin.site.register(Film)
admin.site.register(Customer)
admin.site.register(ClubRep)
admin.site.register(Showing)