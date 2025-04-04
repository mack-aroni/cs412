from django import forms
from .models import Voter

class FilterVoterForm(forms.ModelForm):
    '''A form to add an Voter to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Voter
        fields = []

    PARTY_CHOICES = [('', 'Any')] + [(p.strip(), p.strip()) for p in Voter.objects.values_list('party_affiliation', flat=True).distinct()]
    YEAR_CHOICES = [(str(y), str(y)) for y in range(1920, 2025)]
    SCORE_CHOICES = [('', 'Any')] + [(str(s), str(s)) for s in range(6)]

    party_affiliation = forms.ChoiceField(choices=PARTY_CHOICES, required=False, label="Party Affiliation")
    voter_score = forms.ChoiceField(choices=SCORE_CHOICES, required=False, label="Voter Score")
    min_birth_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False, label="Born After")
    max_birth_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False, label="Born Before")

    voted_20state = forms.BooleanField(required=False, label="Voted in 2020 State Election")
    voted_21town = forms.BooleanField(required=False, label="Voted in 2021 Town Election")
    voted_21primary = forms.BooleanField(required=False, label="Voted in 2021 Primary")
    voted_22general = forms.BooleanField(required=False, label="Voted in 2022 General Election")
    voted_23town = forms.BooleanField(required=False, label="Voted in 2023 Town Election")