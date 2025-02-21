from django.db import models

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
        return f'{self.fname} {self.lname}, {self.email}'