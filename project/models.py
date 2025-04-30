# File: models.py
# Author: Ethan Machleder (emach@bu.edu) April 15, 2025
# Description: 
# Defines the database models for the PocketCards project.
# Models include PocketProfile (user profile), Card (individual collectible cards),
# OwnedBy (ownership relationship between users and cards), PocketFriendRequest and PocketFriend 
# (friendship system), and TradeRequest (trading cards between users)

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class PocketProfile(models.Model):
    '''Encapsulate the idea of a PocketProfile owned by a user.'''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this PocketProfile object.'''
        return f'{self.user}'
    
    def get_card_images(self):
        '''Return a list of image URLs for cards owned by this profile.'''
        cards = OwnedBy.objects.filter(profile=self)
        card_images = [c.card.card_image_url for c in cards]
        return card_images

    def get_friends(self):
        '''Return a list of PocketProfiles that are friends with this profile.'''
        friends = PocketFriend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        friend_profiles = [f.profile1 if f.profile2 == self else f.profile2 for f in friends]
        return friend_profiles

    def get_friend_requests(self):
        '''Return a list of incoming friend requests to this profile, sorted by time.'''
        requests = PocketFriendRequest.objects.filter(to_profile=self)
        requests = requests.order_by('timestamp')
        return requests
        
    def get_pending_friend_requests(self):
        '''Return a list of outgoing friend requests sent by this profile, sorted by time.'''
        requests = PocketFriendRequest.objects.filter(from_profile=self)
        requests = requests.order_by('timestamp')
        return requests

    def get_friend_suggestions(self):
        '''Suggest users who are not yet friends with this profile.'''
        friends = PocketFriend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        friend_profiles = [f.profile1 if f.profile2 == self else f.profile2 for f in friends]
        non_friends = PocketProfile.objects.exclude(id=self.id).exclude(id__in=[profile.id for profile in friend_profiles])
        return non_friends

    def get_trades(self):
        '''Return all trades involving this profile, sorted by time.'''
        trades = TradeRequest.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        trades = trades.order_by('timestamp')
        return trades

class Card(models.Model):
    '''Encapsulate the idea of a Card.'''

    cid = models.TextField(blank=False, default="")  # Card ID within its pack
    pack = models.TextField(blank=False, default="")  # Specific pack (e.g., base, jungle)
    booster = models.TextField(blank=False)  # Booster type (e.g., Pikachu)

    name = models.TextField(blank=False, default="")  # Name of the card
    rarity = models.TextField(blank=False)  # Rarity symbol or label
    poke_type = models.TextField(blank=False)  # Type (e.g., Water, Fire)
    card_type = models.TextField(blank=False)  # "Pokemon", "Trainer", etc.
    card_image_url = models.URLField(blank=False)  # URL to the image of the card

    def __str__(self):
        '''Return a string representation of this Card object.'''
        return f'{self.pack}|{self.cid}|{self.name}'

class OwnedBy(models.Model):
    '''Encapsulate the relation between a PocketProfile and a Card it owns.'''

    profile = models.ForeignKey(PocketProfile, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    count = models.IntegerField(blank=True, default=1)  # Number of copies

    def __str__(self):
        '''Return a string representation of this OwnedBy relation.'''
        return f'{self.profile} owns {self.card} ({self.count})'

class PocketFriendRequest(models.Model):
    '''Model representing a friend request between PocketProfiles.'''

    from_profile = models.ForeignKey(PocketProfile, related_name='sent_requests', on_delete=models.CASCADE)
    to_profile = models.ForeignKey(PocketProfile, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this friend request.'''
        return f'{self.from_profile} sent a friend request to {self.to_profile}'

class PocketFriend(models.Model):
    '''Encapsulate the friendship between two PocketProfiles.'''

    profile1 = models.ForeignKey(PocketProfile, related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey(PocketProfile, related_name="profile2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this friendship.'''
        return f'{self.profile1} is friends with {self.profile2}'
    
class TradeRequest(models.Model):
    '''Represents a trade request between two PocketProfiles.'''

    profile1 = models.ForeignKey("PocketProfile", on_delete=models.CASCADE, related_name="trade_sender")
    profile2 = models.ForeignKey("PocketProfile", on_delete=models.CASCADE, related_name="trade_receiver")
    timestamp = models.DateTimeField(auto_now=True)

    card1 = models.ForeignKey("OwnedBy", on_delete=models.CASCADE, related_name="sender_card")  # Sender's card
    card2 = models.ForeignKey(  # Optional receiver's card for two-way trades
        "OwnedBy",
        on_delete=models.CASCADE,
        related_name="receiver_card",
        null=True,
        blank=True
    )

    send_acc = models.BooleanField(blank=True, default=False)  # Whether sender accepted
    rcv_acc = models.BooleanField(blank=True, default=False)   # Whether receiver accepted
    canceled = models.BooleanField(blank=True, default=False)  # Whether the trade was canceled

    def __str__(self):
        '''Return a string representation of this trade request.'''
        return f"Trade from {self.profile1} to {self.profile2} (cards: {self.card1} -> {self.card2})"
