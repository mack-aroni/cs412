from .models import *
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import *
from django.urls import reverse

class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog profiles.'''
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file

class ShowProfilePageView(DetailView):
    '''Show the details for one profile.'''
    model = Profile
    template_name = 'mini_fb/show_profile.html' ## reusing same template!!
    context_object_name = 'profile'

# define a subclass of CreateView to handle creation of Profile objects
class CreateProfileView(CreateView):
    '''A view to handle creation of a new Profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Profile object (POST)
    '''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"


class CreateStatusMessageView(CreateView):
    '''A view to create a new status message and save it to the database.'''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the article to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Comment
        object before saving it to the database.
        '''

		# instrument our code to display form fields: 
        print(f"CreateStatusMessageView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # attach this article to the comment
        form.instance.profile = profile # set the FK

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
        
        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
        
            
    # show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''

        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        return reverse('show_profile', kwargs={'pk':pk})
        
class UpdateProfileView(UpdateView):
    '''A view to update an Profile and save it to the database.'''
    
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        print(f'UpdateProfileView: form.cleaned_data={form.cleaned_data}')

        return super().form_valid(form)

class DeleteStatusMessageView(DeleteView):
    '''A view to delete a StatusMessage and remove it from the database.'''

    template_name = "mini_fb/delete_status_form.html"
    model = StatusMessage
    context_object_name = 'message'
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''

        # get the pk for this message
        pk = self.kwargs.get('pk')
        message = StatusMessage.objects.get(pk=pk)
        
        # find the Profile to which this StatusMessage is related by FK
        profile = message.profile
        
        # reverse to show the Profile page
        return reverse('show_profile', kwargs={'pk':profile.pk})

class UpdateStatusView(UpdateView):
    '''A view to update an StatusMessage and save it to the database.'''
    
    model = StatusMessage
    form_class = UpdateStatusForm
    template_name = "mini_fb/update_status_form.html"
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        print(f'UpdateStatusView: form.cleaned_data={form.cleaned_data}')

        return super().form_valid(form)

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''

        # get the pk for this message
        pk = self.kwargs.get('pk')
        message = StatusMessage.objects.get(pk=pk)
        
        # find the Profile to which this StatusMessage is related by FK
        profile = message.profile
        
        # reverse to show the Profile page
        return reverse('show_profile', kwargs={'pk':profile.pk})