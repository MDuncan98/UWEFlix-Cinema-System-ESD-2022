from django import forms
from uweflix.models import *

"""class EnterClubRepForm(forms.ModelForm):
    class Meta:
        model = ClubRep"""

class PaymentForm(forms.Form):
    payment_choices = [('credit', 'Pay with Credit'), 
                       ('nopay', 'Pay at Cinema on the day'), 
                       ('tab', 'Add to monthly bill (Club Reps only)')]
    payment_options = forms.ChoiceField(choices=payment_choices, widget = forms.RadioSelect)
    discount_code = forms.CharField(required=False, max_length=8)
