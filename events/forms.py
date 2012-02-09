from django import forms
from .models import EventUsers

class RsvpForm(forms.ModelForm):

    class Meta:
        model = EventUsers
        fields = ('rsvp',)
