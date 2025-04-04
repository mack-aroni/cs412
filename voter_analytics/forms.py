# File: voter_analytics/forms.py
# Author: Ethan Machleder (emach@bu.edu) May 4, 2025
# Description: Defines a form for filtering Voter records based on
# multiple criteria including party affiliation, birth year, score, and
# participation in specific elections.

from django import forms
from .models import Voter

class FilterVoterForm(forms.Form):
    '''A form to filter Voter records based on user-specified criteria.'''

    class Meta:
        '''This form is not tied to model form saving, so Meta is unused here.'''
        model = Voter
        fields = []

    # Dynamically populate party choices from distinct values in the database
    PARTY_CHOICES = [('', 'Any')] + [
        (p.strip(), p.strip()) for p in Voter.objects.values_list('party_affiliation', flat=True).distinct()
    ]

    # Define birth year choices from 1920–2024
    YEAR_CHOICES = [('', 'Any')] + [(str(y), str(y)) for y in range(1920, 2025)]

    # Voter score choices from 0–5
    SCORE_CHOICES = [('', 'Any')] + [(str(s), str(s)) for s in range(6)]

    # Dropdown to select a party affiliation (optional)
    party_affiliation = forms.ChoiceField(
        choices=PARTY_CHOICES,
        required=False,
        label="Party Affiliation"
    )

    # Dropdown to select a voter score (optional)
    voter_score = forms.ChoiceField(
        choices=SCORE_CHOICES,
        required=False,
        label="Voter Score"
    )

    # Filter for minimum year of birth (inclusive)
    min_birth_year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        required=False,
        label="Born After"
    )

    # Filter for maximum year of birth (inclusive)
    max_birth_year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        required=False,
        label="Born Before"
    )

    # Boolean filters for election participation
    voted_20state = forms.BooleanField(
        required=False,
        label="Voted in 2020 State Election"
    )
    voted_21town = forms.BooleanField(
        required=False,
        label="Voted in 2021 Town Election"
    )
    voted_21primary = forms.BooleanField(
        required=False,
        label="Voted in 2021 Primary"
    )
    voted_22general = forms.BooleanField(
        required=False,
        label="Voted in 2022 General Election"
    )
    voted_23town = forms.BooleanField(
        required=False,
        label="Voted in 2023 Town Election"
    )
