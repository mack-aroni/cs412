# File: views.py
# Author: Ethan Macheder (emach@bu.edu) Feb 21, 2025
# Description: This file defines the views used in the mini_fb app.
# Views handle the interaction between the user and the database.
# They define the logic to display, create, update, delete, and manage data
# within the app. This includes handling profiles, status messages, and friends.

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

class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog profiles.'''
    model = Profile  # Retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'  # Template to use for displaying profiles
    context_object_name = 'profiles'  # Name used to access the profiles in the template file

class ShowProfilePageView(DetailView):
    '''Show the details for one profile.'''
    model = Profile  # The Profile model we are working with
    template_name = 'mini_fb/show_profile.html'  # Template for displaying a single profile
    context_object_name = 'profile'  # Name used to access the profile in the template file

class ShowFriendSuggestionsView(DetailView):
    '''Show the friend suggestions for one profile.'''
    model = Profile  # The Profile model we are working with
    template_name = 'mini_fb/friend_suggestions.html'  # Template for displaying friend suggestions
    context_object_name = 'profile'  # Name used to access the profile in the template file

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class ShowNewsFeedView(DetailView):
    '''Show the news feed for one profile.'''
    model = Profile  # The Profile model we are working with
    template_name = 'mini_fb/news_feed.html'  # Template for displaying the profile's news feed
    context_object_name = 'profile'  # Name used to access the profile in the template file

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class CreateProfileView(CreateView):
    '''A view to handle creation of a new Profile.
    (1) Display the HTML form to user (GET)
    (2) Process the form submission and store the new Profile object (POST)
    '''

    form_class = CreateProfileForm  # The form class to use for profile creation
    template_name = "mini_fb/create_profile_form.html"  # Template for creating a new profile

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''A view to update a Profile and save it to the database.'''
    
    model = Profile  # The Profile model we are working with
    form_class = UpdateProfileForm  # The form class to use for updating profiles
    template_name = "mini_fb/update_profile_form.html"  # Template for updating a profile
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        print(f'UpdateProfileView: form.cleaned_data={form.cleaned_data}')
        return super().form_valid(form)

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view to create a new status message and save it to the database.'''

    form_class = CreateStatusMessageForm  # The form class to use for creating status messages
    template_name = "mini_fb/create_status_form.html"  # Template for creating a new status message

    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        
        # Calling the superclass method
        context = super().get_context_data()

        # Retrieve the PK from the URL pattern and find the associated profile
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # Add the profile to the context dictionary
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Comment
        object before saving it to the database.
        '''

        # Instrument our code to display form fields
        print(f"CreateStatusMessageView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # Retrieve the PK from the URL pattern and attach the Profile
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile  # Set the foreign key to the profile

        # Save the StatusMessage object
        sm = form.save()

        # Retrieve uploaded files
        files = self.request.FILES.getlist('files')  
        print(f"Uploaded files: {files}")

        # Process each uploaded file
        for file in files:
            image = Image(profile=profile, image_file=file)
            image.save()  # Save Image object to DB

            status_image = StatusImage(status_message=sm, image=image)
            status_image.save()  # Save StatusImage object to link StatusMessage and Image
        
        # Delegate the work to the superclass method form_valid
        return super().form_valid(form)
        
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''

        # Retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # Call reverse to generate the URL for this Profile
        return reverse('show_profile', kwargs={'pk': pk})

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''A view to delete a StatusMessage and remove it from the database.'''

    template_name = "mini_fb/delete_status_form.html"  # Template for deleting a status message
    model = StatusMessage  # The StatusMessage model we are working with
    context_object_name = 'message'  # Name used to access the message in the template file
    
    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')

    def get_success_url(self):
        '''Return the URL to which we should be directed after the delete.'''

        # Get the pk for this message
        pk = self.kwargs.get('pk')
        message = StatusMessage.objects.get(pk=pk)
        
        # Find the Profile to which this StatusMessage is related by FK
        profile = message.profile
        
        # Reverse to show the Profile page
        return reverse('show_profile', kwargs={'pk': profile.pk})

class UpdateStatusView(LoginRequiredMixin, UpdateView):
    '''A view to update a StatusMessage and save it to the database.'''
    
    model = StatusMessage  # The StatusMessage model we are working with
    form_class = UpdateStatusForm  # The form class to use for updating status messages
    template_name = "mini_fb/update_status_form.html"  # Template for updating a status message
    
    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        
        # Calling the superclass method
        context = super().get_context_data()

        # Retrieve the PK from the URL pattern and find the associated profile
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # Add the profile to the context dictionary
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''
        Handle the form submission to update a StatusMessage object.
        '''
        print(f'UpdateStatusView: form.cleaned_data={form.cleaned_data}')
        return super().form_valid(form)

    def get_success_url(self):
        '''Return the URL to which we should be directed after the update.'''

        # Get the pk for this message
        pk = self.kwargs.get('pk')
        message = StatusMessage.objects.get(pk=pk)
        
        # Find the Profile to which this StatusMessage is related by FK
        profile = message.profile
        
        # Reverse to show the Profile page
        return reverse('show_profile', kwargs={'pk': profile.pk})

class AddFriendView(View):
    '''A view to add a Profile as a Friend to the database.'''

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def dispatch(self, request, friend_pk, *args, **kwargs):

        # INTERMEDIATE SOLUTION
        if not request.user.is_authenticated:
            # Redirect to the login page
            return reverse('login')  

        # Retrieve the profiles using their primary keys
        crofile1 = self.get_object()
        profile2 = Profile.objects.get(pk=friend_pk)

        # Add profile2 as a friend to profile1
        profile1.add_friend(profile2)

        # Redirect to the profile page of profile1
        return redirect(reverse('show_profile', kwargs={'pk': profile1.pk}))
