# File: models.py
# Author: Ethan Machleder (emach@bu.edu) April 15, 2025
# Description: 

from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse

class PocketProfile(models.Model):
    '''Encapsulate the idea of a PocketProfile by some user'''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this PocketProfile object'''
        return f'{self.user}'
    
    def get_card_images(self):
        cards = OwnedBy.objects.filter(profile=self)
        card_images = [c.card.card_image_url for c in cards]
        return card_images


class Card(models.Model):
    '''Encapsulate the idea of a Card'''

    cid = models.TextField(blank=False,default="")
    pack = models.TextField(blank=False, default="")
    booster = models.TextField(blank=False)

    name = models.TextField(blank=False, default="")
    rarity = models.TextField(blank=False)
    poke_type = models.TextField(blank=False)
    card_type = models.TextField(blank=False)
    card_image_url = models.URLField(blank=False)

    def __str__(self):
        '''Return a string representation of this Card object'''
        return f'{self.pack}|{self.cid}|{self.name}'

class OwnedBy(models.Model):
    '''Encapsulate the relation between a PocketProfile owning a Card'''

    profile = models.ForeignKey(PocketProfile, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    count = models.IntegerField(blank=True, default=1)

    def __str__(self):
        '''Return a string representation of this OwnedBy relation'''
        return f'{self.profile} owns {self.card}({self.count})'

class PocketFriend(models.Model):
    '''Encapsulate the relation between a PocketProfile and another PocketProfile'''

    profile1 = models.ForeignKey("PocketProfile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("PocketProfile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)