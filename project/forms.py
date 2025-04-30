# File: project/forms.py
# Author: Ethan Machleder (emach@bu.edu) April 21, 2025
# Description: Defines Django form classes for user interactions in the project app.
# Includes forms for card filtering, pack selection, profile creation, and trade options.

from django import forms
from .models import *

class FilterCardForm(forms.Form):
    '''Form for filtering cards by multiple user-specified criteria.'''
    
    MODE_CHOICES = [
        ('pokemon', 'Pokemon'),
        ('trainer', 'Trainer'),
    ]

    search_name = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Search by Card Name...'}),
        label="Card Name"
    )

    boosters = forms.MultipleChoiceField(
        choices=[('Pikachu', 'Pikachu'), ('Mewtwo', 'Mewtwo'), ('Charizard', 'Charizard'), ('Shared', 'Shared')],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Booster"
    )

    rarities = forms.MultipleChoiceField(
        choices=[('◊','◊'), ('◊◊','◊◊'), ('◊◊◊','◊◊◊'), ('☆','☆'), ('☆☆','☆☆'), ('☆☆☆','☆☆☆'), ("♕", "♕")],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Rarity"
    )

    mode = forms.MultipleChoiceField(
        choices=MODE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Card Category"
    )

    poke_stages = forms.MultipleChoiceField(
        choices=[('Basic', 'Basic'), ('Stage 1', 'Stage 1'), ('Stage 2', 'Stage 2')],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Pokemon Stages"
    )

    poke_types = forms.MultipleChoiceField(
        choices=[(c.strip(), c.strip()) for c in Card.objects.exclude(poke_type='').values_list('poke_type', flat=True).distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Pokemon Types"
    )

    trainer_types = forms.MultipleChoiceField(
        choices=[('Item', 'Item'), ('Supporter', 'Supporter')],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Trainer Types"
    )

class PackSelectForm(forms.Form):
    '''Form to allow user to select a pack type from available boosters.'''

    PACK_CHOICES = [(c.strip(), c.strip()) for c in Card.objects.exclude(booster='Shared').values_list('booster', flat=True).distinct()]
    
    pack_type = forms.ChoiceField(
        choices=PACK_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )

class CreatePocketProfileForm(forms.ModelForm):
    '''Form to create a PocketProfile with profile image input.'''

    class Meta:
        model = PocketProfile
        fields = ['profile_image_url']

class TradeOptionsForm(forms.Form):
    '''Form for filtering cards when managing or creating trades.'''

    search_name = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Search by Card Name...'}),
        label="Card Name"
    )
