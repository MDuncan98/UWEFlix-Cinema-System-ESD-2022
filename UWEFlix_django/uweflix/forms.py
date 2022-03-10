from django import forms
from uweflix.models import ClubRep

class EnterClubRepForm(forms.ModelForm):
    class Meta:
        model = ClubRep
        