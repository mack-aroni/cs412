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

    def get_friends(self):
        friends = PocketFriend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        friend_profiles = [f.profile1 if f.profile2 == self else f.profile2 for f in friends]
        return friend_profiles

    def get_friend_requests(self):
        requests = PocketFriendRequest.objects.filter(to_profile=self)
        requests = requests.order_by('timestamp')
        return requests

    def get_pending_friend_requests(self):
        requests = PocketFriendRequest.objects.filter(from_profile=self)
        requests = requests.order_by('timestamp')
        return requests

    def get_friend_suggestions(self):
        friends = PocketFriend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        friend_profiles = [f.profile1 if f.profile2 == self else f.profile2 for f in friends]
        non_friends = PocketProfile.objects.exclude(id=self.id).exclude(id__in=[profile.id for profile in friend_profiles])
        return non_friends

    def get_trades(self):
        trades = TradeRequest.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        trades = trades.order_by('timestamp')
        return trades

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

class PocketFriendRequest(models.Model):
    from_profile = models.ForeignKey(PocketProfile, related_name='sent_requests', on_delete=models.CASCADE)
    to_profile = models.ForeignKey(PocketProfile, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_profile} sent a friend request to {self.to_profile}'

class PocketFriend(models.Model):
    '''Encapsulate the relation between a PocketProfile and another PocketProfile'''

    profile1 = models.ForeignKey(PocketProfile, related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey(PocketProfile, related_name="profile2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile1} is friends with {self.profile2}'
    
class TradeRequest(models.Model):
    profile1 = models.ForeignKey("PocketProfile", on_delete=models.CASCADE, related_name="trade_sender")
    profile2 = models.ForeignKey("PocketProfile", on_delete=models.CASCADE, related_name="trade_receiver")
    timestamp = models.DateTimeField(auto_now=True)
    card1 = models.ForeignKey("OwnedBy", on_delete=models.CASCADE, related_name="sender_card")
    card2 = models.ForeignKey(
        "OwnedBy",
        on_delete=models.CASCADE,
        related_name="receiver_card",
        null=True,
        blank=True
    )
    send_acc = models.BooleanField(blank=True, default=False)
    rcv_acc = models.BooleanField(blank=True, default=False)
    canceled = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return f"Trade from {self.profile1} to {self.profile2} (cards: {self.card1} -> {self.card2})"
