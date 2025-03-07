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

    def get_images(self):
        '''Return all Images associated with this StatusMessage'''
        status_images = StatusImage.objects.filter(status_message=self)
        images = [status_image.image for status_image in status_images]  # Extract the Image objects
        return images

class Image(models.Model):
    '''Encapsulate the idea of an Image used by some user'''

    # data attributes of an Image:
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this Image object'''
        return f'{self.image_file}'

class StatusImage(models.Model):
    '''Encapsulate the idea of an Status used by some user of an Image'''
    
    # data attributes of a StatusImage:
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    image = models.ForeignKey("Image", on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this StatusImage object'''
        return f'{self.status_message.message} ({self.image.image_file})'