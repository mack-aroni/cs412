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
        choices=[('◊','◊'), ('◊◊','◊◊'), ('◊◊◊','◊◊◊'), ('☆','☆'), ('☆☆','☆☆'), ('☆☆☆','☆☆☆'), ("Crown Rare", "Crown Rare")],
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