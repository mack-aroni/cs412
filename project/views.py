# File: views.py
# Author: Ethan Macheder (emach@bu.edu) April 15, 2025
# Description: 

from .models import *
from .forms import *
from django.views.generic import View, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView

from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

class LoginOrProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')
        return redirect('login')

class TempHome(LoginRequiredMixin, ListView):
    '''TEMP VIEW'''
    model = PocketProfile
    template_name = 'project/temp_home.html'
    context_object_name = 'pocket_profiles'

    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')

class CardCatalogView(LoginRequiredMixin, ListView):
    model = OwnedBy
    template_name = 'project/card_catalog.html'
    context_object_name = 'cards'

    def get_profile(self):
        return PocketProfile.objects.get(user=self.request.user)

    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')

    def get_queryset(self):
        '''Apply filters based on form fields.'''
        
        queryset = OwnedBy.objects.filter(profile=self.get_profile())
        form = FilterCardForm(self.request.GET)

        if form.is_valid():
            mode = form.cleaned_data.get('mode')
            poke_stages = form.cleaned_data.get('poke_stages')
            poke_types = form.cleaned_data.get('poke_types')
            trainer_types = form.cleaned_data.get('trainer_types')
            search_name = form.cleaned_data.get('search_name', '').strip()
            boosters = form.cleaned_data.get('boosters')
            rarity = form.cleaned_data.get('rarities')

            if search_name:
                queryset = queryset.filter(card__name__icontains=search_name)

            if  boosters:
                queryset = queryset.filter(card__booster__in=boosters)

            if rarity:
                queryset = queryset.filter(card__rarity__in=rarity)

            if 'pokemon' in mode:
                if poke_stages:
                    queryset = queryset.filter(card__card_type__in=poke_stages)
                if poke_types:
                    queryset = queryset.filter(card__poke_type__in=poke_types)

            if 'trainer' in mode:
                if trainer_types:
                    queryset = queryset.filter(card__card_type__in=trainer_types)
        
        return queryset

    def get_context_data(self, **kwargs):
        '''Pass form and result count to the template.'''
        context = super().get_context_data(**kwargs)
        context["form"] = FilterCardForm(self.request.GET)
        context["result_count"] = self.get_queryset().count()
        return context
