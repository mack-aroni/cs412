# File: project/forms.py
# Author: Ethan Machleder (emach@bu.edu) April 21, 2025
# Description: 

from django import forms
from .models import *

class FilterCardForm(forms.Form):
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
        choices = [(c.strip(), c.strip()) for c in Card.objects.exclude(poke_type='').values_list('poke_type', flat=True).distinct()],
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
    PACK_CHOICES = [(c.strip(), c.strip()) for c in Card.objects.exclude(booster='Shared').values_list('booster', flat=True).distinct()]
    
    pack_type = forms.ChoiceField(choices=PACK_CHOICES, widget=forms.RadioSelect, required=False)

class CreatePocketProfileForm(forms.ModelForm):
    '''A form to add an PocketProfile to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = PocketProfile
        fields = ['profile_image_url']