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

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a Profile to the database.'''

    class Meta:
        '''associate this form with the Profile model.'''
        model = Profile
        fields = ['city', 'email', 'profile_image_url']

class UpdateStatusForm(forms.ModelForm):
    '''A form to update a StatusMessage to the database.'''

    class Meta:
        '''associate this form with the StatusMessage model.'''
        model = StatusMessage
        fields = ['message']