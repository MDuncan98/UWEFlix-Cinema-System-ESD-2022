from django import forms
from uweflix.models import *
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

"""class EnterClubRepForm(forms.ModelForm):
    class Meta:
        model = ClubRep"""

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username',)

class RegisterClubRepForm(forms.ModelForm):
    class Meta:
        model = ClubRep
        fields = ('club', 'club_rep_num', 'dob')
    dob = forms.DateField(widget=forms.DateInput())

class RegisterStudentForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('dob',)

class AccessClubForm(forms.Form):
    club_choices = ((None, "Select a club:"),)
    month_choices = ()
    year_choices = ()
    current_year = 2022 #find a programmatical way of getting this
    for i in range(Club.objects.all().count()):
        tmp = ((Club.objects.get(id=i+1).id, Club.objects.get(id=i+1).name),)
        club_choices += tmp
    for i in range(12):
        choice_string = ""
        if i < 9:
            choice_string += "0"
        tmp = ((i+1, choice_string+str(i+1)),)
        month_choices += tmp
    for i in range(15):
        tmp = ((current_year+i,current_year+i),)
        year_choices += tmp
    club = forms.ChoiceField(choices=club_choices)
    card_number = forms.DecimalField(max_digits=16, decimal_places=0)
    expiry_month = forms.ChoiceField(choices=month_choices)
    expiry_year = forms.ChoiceField(choices=year_choices)

class PaymentForm(forms.Form):
    adult_tickets = forms.IntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ],required=False, initial=0)
    student_tickets = forms.IntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ],required=False, initial=0)
    child_tickets = forms.IntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ],required=False, initial=0)
    total_cost=forms.FloatField(label="Total Cost: ", disabled=True, required=False)
    payment_choices = [(None, 'Select an option:'),
                    ('credit', 'Pay with Credit'), 
                    ('nopay', 'Pay at Cinema on the day'),
                    ('tab', 'Add to monthly bill (Club Reps only)')]
    payment_options = forms.ChoiceField(choices=payment_choices, widget=forms.Select(attrs={}))
    discount_code = forms.CharField(required=False, max_length=8, widget=forms.TextInput(attrs={}))
    def clean(self):
        adult_tickets = self.cleaned_data.get('adult_tickets')
        student_tickets = self.cleaned_data.get('student_tickets')
        child_tickets = self.cleaned_data.get('child_tickets')
        if adult_tickets == 0 and student_tickets == 0 and child_tickets == 0:
            raise forms.ValidationError("You must purchase at least one ticket type.")
        return self.cleaned_data

    def __setchoices__(self, newvalue):
        self.payment_choices = newvalue


#class addClubForm(forms.ModelForm):
#    class Meta:
#        model = Club
#        fields = "__all__"

#class addRepForm(forms.ModelForm):
#    class Meta:
#        model = Representative
#        fields = "__all__"
#        widgets = {
#        'dob': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
#        }
