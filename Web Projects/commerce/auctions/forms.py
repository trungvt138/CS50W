from django import forms
from .models import Listing, User, Bid, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'starting_bid': forms.NumberInput(attrs={'step': 0.01}),
        }

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['image_url'].required = False