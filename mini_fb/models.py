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

    def get_friends(self):
        '''Return all of the Friends of this Profile.'''

        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        friend_profiles = [f.profile1 if f.profile2 == self else f.profile2 for f in friends]
        return friend_profiles

    def add_friend(self, other):
        '''Add another Profile as a Friend'''
        if self == other:
            return
        
        existing_friendship = Friend.objects.filter(
            (models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self))
        ).exists()
        
        if not existing_friendship:
            Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        '''Return all Profiles who are not Friends of this Profile.'''

        # Get all the friends of this profile
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))

        # Get a list of profiles that are friends with this profile
        friend_profiles = [f.profile1 if f.profile2 == self else f.profile2 for f in friends]

        # Get all profiles excluding the current profile and the friends list
        non_friends = Profile.objects.exclude(id=self.id).exclude(id__in=[profile.id for profile in friend_profiles])

        return non_friends
    
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

class Friend(models.Model):
    '''Encapsulate the idea of a Friend by some user'''
    
    # data attributes of a Friend:
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)


    def __str__(self):
        '''Return a string representation of this Friend object'''
        return f'{self.profile1} & {self.profile2}'