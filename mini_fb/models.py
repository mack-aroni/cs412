# File: models.py
# Author: Ethan Macheder (emach@bu.edu) 
# Description: This file defines the models used in the mini_fb app.
# Models represent the database schema for the application.
# These include the Profile, StatusMessage, Image, StatusImage, and Friend models.

from django.db import models
from django.urls import reverse


class Profile(models.Model):
    '''Encapsulate the idea of a Profile by some user'''

    # Data attributes of a profile:
    fname = models.TextField(blank=False)  # First name of the user
    lname = models.TextField(blank=False)  # Last name of the user
    city = models.TextField(blank=False)   # City where the user resides
    email = models.TextField(blank=False)  # Email address of the user
    profile_image_url = models.URLField(blank=True)  # Profile image URL (optional)

    def __str__(self):
        '''Return a string representation of this Profile object'''
        return f'{self.fname} {self.lname}'

    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_profile', kwargs={'pk': self.pk})

    def get_status_messages(self):
        '''Return all of the StatusMessages about this Profile.'''
        status_messages = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
        return status_messages

    def get_friends(self):
        '''Return all of the Friends of this Profile.'''
        # Search for all friends of the profile
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))

        # Filter for "other" Friend
        friend_profiles = [f.profile1 if f.profile2 == self else f.profile2 for f in friends]

        return friend_profiles

    def add_friend(self, other):
        '''Add another Profile as a Friend'''
        
        # Check for adding self as a friend
        if self == other:
            return
        
        # Check for existing Friend relation
        existing_friendship = Friend.objects.filter(
            (models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self))
        ).exists()
        
        # Else create new Friend relation
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

    def get_news_feed(self):
        '''Return a combined list of StatusMessages for this Profile and all of their Friends.'''
        # Get the status messages for this profile
        profile_statuses = StatusMessage.objects.filter(profile=self)
        
        # Get all the friends of this profile
        friends = self.get_friends()
        
        # Get the status messages for each friend
        friend_statuses = StatusMessage.objects.filter(profile__in=friends)
        
        # Combine the status messages (Profile's and Friends')
        all_statuses = profile_statuses | friend_statuses
        
        # Return the combined and ordered status messages by timestamp (most recent first)
        return all_statuses.order_by('-timestamp')


class StatusMessage(models.Model):
    '''Encapsulate the idea of a StatusMessage by some user'''

    # Data attributes of a StatusMessage:
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)  # User's profile associated with the message
    message = models.TextField(blank=False)  # Status message text
    timestamp = models.DateTimeField(auto_now=True)  # Timestamp of when the status was posted

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

    # Data attributes of an Image:
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)  # User's profile associated with the image
    image_file = models.ImageField(blank=True)  # The image file
    timestamp = models.DateTimeField(auto_now=True)  # Timestamp of when the image was uploaded
    caption = models.TextField(blank=False)  # Caption for the image

    def __str__(self):
        '''Return a string representation of this Image object'''
        return f'{self.image_file}'


class StatusImage(models.Model):
    '''Encapsulate the idea of a Status used by some user of an Image'''
    
    # Data attributes of a StatusImage:
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)  # Status message associated with the image
    image = models.ForeignKey("Image", on_delete=models.CASCADE)  # Image associated with the status

    def __str__(self):
        '''Return a string representation of this StatusImage object'''
        return f'{self.status_message.message} ({self.image.image_file})'


class Friend(models.Model):
    '''Encapsulate the idea of a Friend by some user'''
    
    # Data attributes of a Friend:
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")  # First user in the friendship
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")  # Second user in the friendship
    timestamp = models.DateTimeField(auto_now=True)  # Timestamp of when the friendship was created

    def __str__(self):
        '''Return a string representation of this Friend object'''
        return f'{self.profile1} & {self.profile2}'