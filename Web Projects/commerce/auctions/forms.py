from django import forms
from .models import Listing, User, Bid, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ['user']
