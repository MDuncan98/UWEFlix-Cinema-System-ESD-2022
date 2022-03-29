from django import forms
from uweflix.models import *
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe

"""class EnterClubRepForm(forms.ModelForm):
    class Meta:
        model = ClubRep"""

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
