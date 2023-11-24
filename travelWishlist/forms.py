from django import forms
from .models import Place

class NewPlaceForm(forms.ModelForm):
     # get place and when visited.

    class Meta:
        model = Place
        fields = ('name', 'visited')


class TripReviewForm:
    pass