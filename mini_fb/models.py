from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the idea of an Profile by some user'''

    # data attributes of a profile:
    fname = models.TextField(blank=False)
    lname = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=True)
    
    def __str__(self):
        '''Return a string representation of this Profile object'''
        return f'{self.fname} {self.lname}'

    def get_status_messages(self):
        '''Return all of the StatusMessages about this Profile.'''

        status_messages = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
        return status_messages
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_profile', kwargs={'pk':self.pk})

class StatusMessage(models.Model):
    '''Encapsulate the idea of an StatusMessage by some user'''

    # data attributes of a StatusMessage:
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this StatusMessage object'''
        return f'{self.message} {self.timestamp}'
