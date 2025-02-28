from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to add an Profile to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = ['fname', 'lname', 'city', 'email', 'profile_image_url']

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add an StatusMessage to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = StatusMessage
        fields = ['message']