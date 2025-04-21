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

# Create your views here.

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

class CardCatalogView(ListView):
    model = Card
    template_name = 'project/card_catalog.html'
    context_object_name = 'card_list'

    def get_queryset(self):
        '''Apply filters based on form fields.'''
        queryset = Card.objects.all()
        form = FilterCardForm(self.request.GET)

        if form.is_valid():
            mode = form.cleaned_data.get('mode')
            poke_stages = form.cleaned_data.get('poke_stages')
            poke_types = form.cleaned_data.get('poke_types')
            trainer_types = form.cleaned_data.get('trainer_types')

            if mode == 'pokemon':
                if poke_stages:
                    print(poke_stages)
                    queryset = queryset.filter(card_type__in=poke_stages)
                if poke_types:
                    queryset = queryset.filter(poke_type__in=poke_types)

            elif mode == 'trainer':
                if trainer_types:
                    queryset = queryset.filter(card_type__in=trainer_types)

        return queryset

    def get_context_data(self, **kwargs):
        '''Pass form and result count to the template.'''
        context = super().get_context_data(**kwargs)
        context["form"] = FilterCardForm(self.request.GET)
        context["result_count"] = self.get_queryset().count()
        return context