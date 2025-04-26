# File: views.py
# Author: Ethan Macheder (emach@bu.edu) April 15, 2025
# Description: 

import random

from .models import *
from .forms import *
from django.views.generic import View, ListView, FormView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView

from django.shortcuts import redirect, render
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

class CreatePocketProfile(CreateView):
    form_class = CreatePocketProfileForm  # The form class to use for profile creation
    template_name = "project/register.html"  # Template for creating a new profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()  # Add UserCreationForm to context
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)  # Reconstruct user form

        if user_form.is_valid():  
            user = user_form.save()  # Save new User
            login(self.request, user)  # Log in new User
            form.instance.user = user  # Assign User to Profile
            return super().form_valid(form)  # Save Profile

        # If user_form is invalid, re-render page with errors
        return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

    def get_success_url(self):
        """Redirect to the user's profile page after successful profile creation."""
        return reverse('profile')

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

        queryset = queryset.order_by('card__cid')
        return queryset

    def get_context_data(self, **kwargs):
        '''Pass form and result count to the template.'''
        context = super().get_context_data(**kwargs)
        context["form"] = FilterCardForm(self.request.GET)
        context["result_count"] = self.get_queryset().count()
        return context

class PackSelectView(LoginRequiredMixin, FormView):
    form_class = PackSelectForm
    template_name = 'project/pack_select.html'

    def get_profile(self):
        return PocketProfile.objects.get(user=self.request.user)

    def form_valid(self, form):
        form = PackSelectForm(self.request.POST)
        if form.is_valid():
            selected_pack = [form.cleaned_data['pack_type'], 'Shared']
            print(f"User selected pack: {selected_pack}")

            options = list(Card.objects.filter(booster__in=selected_pack).order_by('?'))
            opened_cards = random.sample(options, 5)

            RARITY_ORDER = {'♕': 8,'☆☆☆': 7,'☆☆': 6,'☆': 5,'◊◊◊◊': 4,'◊◊◊': 3,'◊◊': 2,'◊': 1,}            
            opened_cards = sorted(opened_cards, key=lambda card: RARITY_ORDER.get(card.rarity, 0))

            profile = self.get_profile()
            for c in opened_cards:
                relation, created = OwnedBy.objects.get_or_create(profile=profile, card=c)
                if not created:
                    relation.count += 1
                relation.save()

            return render(self.request, 'project/pack_opened.html', {
                'cards': opened_cards,
                'pack_name': selected_pack[0],
            })

        return redirect('packs')

