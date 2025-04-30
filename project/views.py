# File: views.py
# Author: Ethan Macheder (emach@bu.edu) April 15, 2025
# Description: This file defines the views used in the card_collection app.
# Views handle the interaction between the user and the database.
# They define the logic to display, filter, and manage card records,
# including handling pack selections, card details, and user-submitted filters.

import random

from .models import *
from .forms import *
from django.views.generic import View, ListView, FormView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView

from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

class LoginOrProfileView(View):
    def get(self, request):
        # Redirect authenticated users to their profile or to create one if not found
        if request.user.is_authenticated:
            profile = request.user.pocketprofile_set.first()
            if profile:
                return redirect('pocket_profile', pk=profile.id)
            return redirect('create_profile')
        # Unauthenticated users go to login
        return redirect('login')

class CreatePocketProfile(CreateView):
    """
    View to create a new PocketProfile for a user.
    This view handles both user creation and profile creation in a single form.
    """
    form_class = CreatePocketProfileForm  # Form for creating a PocketProfile
    template_name = "project/register.html"  # Template for the registration page

    def get_context_data(self, **kwargs):
        """
        Add the UserCreationForm to the context for the template.
        If the user form is not already in the context, initialize and add it.
        """
        # Get the default context from the superclass
        context = super().get_context_data(**kwargs)
        
        # Add UserCreationForm to the context if not already present
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        
        return context

    def form_valid(self, form):
        """
        Save the user and their profile when the form is valid.
        After saving, log the user in and associate the profile with the user.
        """
        # Create and validate the UserCreationForm
        user_form = UserCreationForm(self.request.POST)
        
        if user_form.is_valid():
            # Save the user and log them in
            user = user_form.save()
            login(self.request, user)
            
            # Associate the profile with the created user
            form.instance.user = user
            
            # Call the superclass's form_valid method to save the profile
            return super().form_valid(form)
        
        # If the user creation fails, redisplay the form with error messages
        return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

    def get_success_url(self):
        """Redirect to the profile page after successful registration"""
        return reverse('profile')

class CardCatalogView(LoginRequiredMixin, ListView):
    # Define the model and template for the view
    model = Card
    template_name = 'project/card_catalog.html'
    context_object_name = 'cards'

    def get_login_url(self):
        """Returns the URL to redirect to the login page"""
        return reverse('login')

    def get_profile(self):
        """Retrieves the PocketProfile associated with the current user"""
        return PocketProfile.objects.get(user=self.request.user)

    def get_queryset(self):
        """
        Retrieves a queryset of Card objects filtered based on user input
        from the filter form.
        """
        # Initialize the form with GET data
        form = FilterCardForm(self.request.GET)
        queryset = Card.objects.all()  # Start with all Card objects

        if form.is_valid():
            # Extract cleaned data from the form
            mode = form.cleaned_data.get('mode')
            poke_stages = form.cleaned_data.get('poke_stages')
            poke_types = form.cleaned_data.get('poke_types')
            trainer_types = form.cleaned_data.get('trainer_types')
            search_name = form.cleaned_data.get('search_name', '').strip()
            boosters = form.cleaned_data.get('boosters')
            rarity = form.cleaned_data.get('rarities')

            # Apply filters based on form input
            if search_name:
                queryset = queryset.filter(name__icontains=search_name)  # Filter by name
            if boosters:
                queryset = queryset.filter(booster__in=boosters)  # Filter by booster
            if rarity:
                queryset = queryset.filter(rarity__in=rarity)  # Filter by rarity
            if 'pokemon' in mode:
                # If filtering for Pokémon cards, apply stage and type filters
                if poke_stages:
                    queryset = queryset.filter(card_type__in=poke_stages)
                if poke_types:
                    queryset = queryset.filter(poke_type__in=poke_types)
            if 'trainer' in mode:
                # If filtering for Trainer cards, apply trainer type filter
                if trainer_types:
                    queryset = queryset.filter(card_type__in=trainer_types)

        # Return the filtered queryset ordered by card ID
        return queryset.order_by('cid')

    def get_context_data(self, **kwargs):
        """
        Adds the filter form and ownership statistics to the context
        to be rendered in the template.
        """
        # Get the default context from the superclass
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()  # Get the current user's profile
        context["form"] = FilterCardForm(self.request.GET)  # Include the filter form in context
        context["filter_open"] = bool(self.request.GET)  # Determine if any filters are applied

        # Retrieve the owned cards for the current user
        owned_cards = OwnedBy.objects.filter(profile=profile)
        owned_map = {o.card_id: o.count for o in owned_cards}  # Create a mapping of card ID to count
        context["owned_map"] = owned_map

        # Get the queryset of cards to display
        queryset = self.object_list
        context["total_unique_cards"] = queryset.count()  # Total number of unique cards

        # Find the intersection of owned cards and filtered cards
        owned_card_ids = owned_cards.values_list('card_id', flat=True)
        filtered_card_ids = queryset.values_list('id', flat=True)
        intersection = set(owned_card_ids) & set(filtered_card_ids)

        # Add statistics about owned cards to the context
        context["total_unique_cards_owned"] = len(intersection)  # Total owned unique cards
        context["total_cards"] = sum(owned_map[c] for c in intersection)  # Total owned cards count

        return context

class PackSelectView(LoginRequiredMixin, FormView):
    """
    View for handling the selection and opening of a booster pack.
    This view processes the user's selected pack type and opens a pack of cards,
    displaying the opened cards sorted by rarity.
    """
    form_class = PackSelectForm  # Form for selecting a booster pack
    template_name = 'project/pack_select.html'  # Template for selecting the pack

    def get_login_url(self):
        """Return the URL required for login"""
        return reverse('login')

    def get_profile(self):
        """Retrieve the PocketProfile associated with the current logged-in user"""
        return PocketProfile.objects.get(user=self.request.user)

    def form_valid(self, form):
        """
        Handle the process of opening a booster pack when the form is valid.
        This method selects a random set of cards from the selected booster pack,
        sorts them by rarity, and updates the user's ownership of the opened cards
        """
        # Initialize the form with POST data and validate
        form = PackSelectForm(self.request.POST)
        if form.is_valid():
            # Select the pack type and create a query to retrieve cards
            selected_pack = [form.cleaned_data['pack_type'], 'Shared']
            options = list(Card.objects.filter(booster__in=selected_pack).order_by('?'))
            
            # Randomly select 5 cards from the available options
            opened_cards = random.sample(options, 5)

            # Define the order of rarities for sorting the opened cards
            RARITY_ORDER = {'♕': 8, '☆☆☆': 7, '☆☆': 6, '☆': 5, '◊◊◊◊': 4, '◊◊◊': 3, '◊◊': 2, '◊': 1}
            # Sort the opened cards based on the rarity
            opened_cards = sorted(opened_cards, key=lambda card: RARITY_ORDER.get(card.rarity, 0))

            # Get the current user's profile to track card ownership
            profile = self.get_profile()
            
            # Update the ownership of the opened cards
            for c in opened_cards:
                relation, created = OwnedBy.objects.get_or_create(profile=profile, card=c)
                if not created:
                    relation.count += 1  # Increment the card count if already owned
                relation.save()

            # Render the pack opening result page with the opened cards
            return render(self.request, 'project/pack_opened.html', {
                'cards': opened_cards,
                'pack_name': selected_pack[0],
            })

        # If the form is not valid, redirect to the packs selection page
        return redirect('packs')

class TradeHubView(LoginRequiredMixin, DetailView):
    """
    View for displaying the trade hub of a user's PocketProfile.
    This view provides the details of a user's profile, allowing interaction with trade features.
    """
    model = PocketProfile  # The model representing the user's profile
    template_name = 'project/trade_hub.html'  # Template to display the trade hub
    context_object_name = 'profile'  # The context variable name used in the template

    def get_login_url(self):
        '''Return the URL required for login'''
        return reverse('login')

class FriendSuggestionListView(LoginRequiredMixin, DetailView):
    """
    View to display friend suggestions for the user's PocketProfile.
    The view provides potential friend suggestions based on the user's profile.
    """
    model = PocketProfile  # The model representing the user's PocketProfile
    template_name = 'project/friend_suggestions.html'  # Template to display the friend suggestions
    context_object_name = 'profile'  # The context variable name used in the template to refer to the user's profile

    def get_login_url(self):
        """Return the URL required for login"""
        return reverse('login')

    def get_profile(self):
        """Retrieve the PocketProfile associated with the current logged-in user"""
        return PocketProfile.objects.get(user=self.request.user)

class FriendRequestListView(LoginRequiredMixin, DetailView):
    """
    View to display the list of friend requests for the user's PocketProfile.
    The view shows the current pending friend requests for the logged-in user.
    """
    model = PocketFriend  # The model representing friend requests
    template_name = 'project/friend_requests.html'  # Template to display the friend requests
    context_object_name = 'profile'  # The context variable name used in the template to refer to the user's profile

    def get_login_url(self):
        """Return the URL required for login if the user is not authenticated"""
        return reverse('login')

    def get_object(self):
        """Retrieve the PocketProfile associated with the current logged-in user"""
        return PocketProfile.objects.get(user=self.request.user)

class PocketProfileView(LoginRequiredMixin, DetailView):
    """
    View to display a user's PocketProfile, including whether the profile is
    the current user's own profile, whether the user and the profile are friends,
    and any pending friend requests between them.
    """
    model = PocketProfile  # The model representing a user's profile
    template_name = 'project/pocket_profile.html'  # Template to render the profile page
    context_object_name = 'profile_viewed'  # The context variable used to refer to the profile in the template

    def get_context_data(self, **kwargs):
        """
        Retrieve additional context data for the profile view, including information
        about whether the profile is the current user's own, if they are friends,
        and any pending friend requests.
        """
        context = super().get_context_data(**kwargs)  # Get the default context
        profile = self.get_object()  # The PocketProfile object being viewed
        viewer = get_object_or_404(PocketProfile, user=self.request.user)  # The PocketProfile of the currently logged-in user

        # Add context data indicating whether the profile is the current user's, 
        # whether they are friends, and if there are any pending friend requests
        context['is_me'] = profile == viewer  # True if the profile belongs to the logged-in user
        context['is_friend'] = profile in viewer.get_friends()  # True if the logged-in user and profile are friends
        context['sent_request'] = PocketFriendRequest.objects.filter(from_profile=viewer, to_profile=profile).first()  # Sent friend request
        context['received_request'] = PocketFriendRequest.objects.filter(from_profile=profile, to_profile=viewer).first()  # Received friend request

        return context

class SendFriendRequestView(LoginRequiredMixin, View):
    """
    View to handle sending a friend request from the currently logged-in user
    to another user identified by their profile ID.
    """

    def get_object(self):
        """Retrieve the PocketProfile associated with the current logged-in user"""
        return PocketProfile.objects.get(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to send a friend request.
        Ensures that users cannot send friend requests to themselves,
        and avoids duplicate friend requests by using get_or_create.
        """
        from_profile = self.get_object()  # The user sending the friend request
        to_profile = get_object_or_404(PocketProfile, id=self.kwargs['profile_id'])  # The recipient profile

        # Only send a friend request if it's not to self
        if from_profile != to_profile:
            PocketFriendRequest.objects.get_or_create(from_profile=from_profile, to_profile=to_profile)

        # Redirect to the recipient's profile after sending the request
        return redirect('pocket_profile', pk=to_profile.id)

class CancelFriendRequestView(LoginRequiredMixin, View):
    """
    View to handle the cancellation of a previously sent friend request
    by the currently logged-in user to another user's profile.
    """

    def get_object(self):
        """Retrieve the PocketProfile associated with the current logged-in user"""
        return PocketProfile.objects.get(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to cancel a sent friend request.
        Deletes the friend request from the current user to the specified profile ID.
        """
        from_profile = self.get_object()  # The user canceling the request

        # Delete the friend request directed at the specified profile
        PocketFriendRequest.objects.filter(
            from_profile=from_profile,
            to_profile_id=self.kwargs['profile_id']
        ).delete()

        # Redirect back to the profile page of the recipient
        return redirect('pocket_profile', pk=self.kwargs['profile_id'])

class AcceptFriendRequestView(LoginRequiredMixin, View):
    """
    View to handle acceptance of a friend request sent to the current user.
    On acceptance, a mutual friendship is created and the request is deleted.
    """

    def get_object(self):
        """Retrieve the PocketProfile associated with the current logged-in user"""
        return PocketProfile.objects.get(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to accept a friend request.
        Creates a friendship between the sender and receiver, and deletes the request.
        """
        to_profile = self.get_object()  # The recipient of the friend request
        from_profile = get_object_or_404(PocketProfile, id=self.kwargs['profile_id'])  # The sender

        # Retrieve and verify the friend request exists
        friend_request = get_object_or_404(
            PocketFriendRequest,
            from_profile=from_profile,
            to_profile=to_profile
        )

        # Ensure a consistent ordering of profile1/profile2 in the friendship
        profile1, profile2 = sorted([to_profile, from_profile], key=lambda p: p.id)
        
        # Create the friendship if it doesn't already exist
        PocketFriend.objects.get_or_create(profile1=profile1, profile2=profile2)

        # Remove the friend request as it has been accepted
        friend_request.delete()

        # Redirect to the friend requests page
        return redirect('friend_requests')

class DeclineFriendRequestView(LoginRequiredMixin, View):
    """
    View to handle declining of a received friend request.
    Deletes the friend request without creating a friendship.
    """

    def get_object(self):
        """Retrieve the PocketProfile associated with the current logged-in user"""
        return PocketProfile.objects.get(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to decline a friend request.
        Deletes the request from the sender to the current user.
        """
        to_profile = self.get_object()  # The current logged-in user (receiver of the request)

        # Remove the friend request sent to the current user
        PocketFriendRequest.objects.filter(
            from_profile_id=self.kwargs['profile_id'],
            to_profile=to_profile
        ).delete()

        # Redirect to the friend requests page
        return redirect('friend_requests')

class RemoveFriendView(LoginRequiredMixin, View):
    """
    View to handle the removal of an existing friend connection
    between the logged-in user and another profile.
    """

    def get_object(self):
        """Retrieve the PocketProfile associated with the current logged-in user"""
        return PocketProfile.objects.get(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to remove a friend connection.
        Deletes the corresponding PocketFriend entry between both users.
        """
        my_profile = self.get_object()  # The profile of the logged-in user
        other_profile = get_object_or_404(PocketProfile, id=self.kwargs['profile_id'])  # Friend to remove

        # Sort the two profiles by ID to match storage format in PocketFriend
        profile1, profile2 = sorted([my_profile, other_profile], key=lambda p: p.id)

        # Delete the friendship entry from the database
        PocketFriend.objects.filter(profile1=profile1, profile2=profile2).delete()

        # Redirect to the friend's profile page
        return redirect('pocket_profile', pk=other_profile.id)

class TradeOptionsView(LoginRequiredMixin, ListView):
    """
    View for displaying tradable cards that the user owns.
    Filters out cards with only one copy and allows optional search by name.
    """

    model = OwnedBy
    template_name = 'project/trade_options.html'
    context_object_name = 'cards'

    def get_login_url(self):
        """Return the URL required for login"""
        return reverse('login')

    def get_profile(self):
        """Retrieve the PocketProfile associated with the current logged-in user"""
        return PocketProfile.objects.get(user=self.request.user)

    def get_queryset(self):
        """Return a filtered queryset of tradable cards based on the user's profile and optional search input"""
        # Start with all cards owned by the user
        queryset = OwnedBy.objects.filter(profile=self.get_profile())

        # Only include cards with more than one copy (tradable)
        queryset = queryset.filter(count__gt=1)

        # Apply filtering from GET form input
        form = TradeOptionsForm(self.request.GET)
        if form.is_valid():
            search_name = form.cleaned_data.get('search_name', '').strip()
            if search_name:
                queryset = queryset.filter(card__name__icontains=search_name)

        # Order the results by card ID
        return queryset.order_by('card__cid')

    def get_context_data(self, **kwargs):
        """Add the form, result count, and context-specific trade info to the template context"""
        context = super().get_context_data(**kwargs)

        # Add the search form and count of filtered results
        context["form"] = TradeOptionsForm(self.request.GET)
        context["result_count"] = self.get_queryset().count()

        # Include trade-related identifiers depending on the request context
        if len(self.kwargs) > 1:
            context["type"] = self.kwargs.get('type')
            context["sender_pk"] = self.kwargs.get('sender_pk')
            context["receiver_pk"] = self.kwargs.get('receiver_pk')
        else:
            context["trade_pk"] = self.kwargs.get('trade_pk')

        return context

class CreateTradeView(LoginRequiredMixin, View):
    """Handle creation of a new trade request between two users"""

    def get_login_url(self):
        """Return the URL required for login"""
        return reverse('login')

    def get_profile(self):
        """Retrieve the PocketProfile associated with the current logged-in user"""
        return PocketProfile.objects.get(user=self.request.user)

    def dispatch(self, request, sender_pk, receiver_pk, card_pk, *args, **kwargs):
        """
        Process the trade creation request:
        - Ensure user is authenticated
        - Validate the sender, receiver, and selected card
        - Only allow trade if the card has more than one copy
        - Redirect to the appropriate trade view on success or back to options on failure
        """

        # Fetch trade participants and card
        profile1 = get_object_or_404(PocketProfile, pk=sender_pk)
        profile2 = get_object_or_404(PocketProfile, pk=receiver_pk)
        card = OwnedBy.objects.get(pk=card_pk)

        # If card is invalid or not tradable, redirect back to trade options
        if not card or card.count <= 1:
            return redirect('trade_options', type=0, sender_pk=profile1.pk, receiver_pk=profile2.pk)

        # Create the trade request
        TradeRequest.objects.create(
            profile1=profile1,
            profile2=profile2,
            card1=card,
        )

        # Redirect to the trade view for the logged-in user
        return redirect('trade', pk=self.get_profile().pk)

class AcceptTradeView(LoginRequiredMixin, View):
    """Handle the acceptance of a trade by the receiver"""

    def get_login_url(self):
        """Return the URL required for login"""
        return reverse('login')

    def get_profile(self):
        """Retrieve the PocketProfile associated with the current logged-in user"""
        return PocketProfile.objects.get(user=self.request.user)

    def dispatch(self, request, trade_pk, card_pk, *args, **kwargs):
        """
        Accept a trade request by:
        - Validating user authentication
        - Retrieving the trade and selected card
        - Ensuring the card exists and has more than one copy
        - Assigning the selected card as card2 in the trade and marking it accepted
        """

        # Redirect unauthenticated users to login
        if not request.user.is_authenticated:
            return reverse('login')

        # Fetch the trade request
        trade = TradeRequest.objects.get(pk=trade_pk)

        # Fetch the card proposed in exchange
        card = OwnedBy.objects.get(pk=card_pk)
        if not card or card.count <= 1:
            # Redirect back to trade options if card is invalid or not tradable
            return redirect('trade_options', sender_pk=trade.profile1.pk, receiver_pk=trade.profile2.pk)

        # Update the trade request with the selected card and mark as accepted
        trade.card2 = card
        trade.rcv_acc = True
        trade.save()

        # Redirect to the trade list view for the current user
        return redirect('trade', pk=self.get_profile().pk)

class FinalizeTradeView(LoginRequiredMixin, View):
    """Handle the finalization of a trade once both parties have accepted"""

    def get_login_url(self):
        """Return the URL required for login"""
        return reverse('login')

    def get_profile(self):
        """Retrieve the PocketProfile associated with the current logged-in user"""
        return PocketProfile.objects.get(user=self.request.user)

    def dispatch(self, request, trade_pk, *args, **kwargs):
        """
        Finalize the trade process by:
        - Marking the trade as accepted by the sender
        - Checking if both sender and receiver have accepted
        - If both accepted and both cards are tradable (count > 1), exchange the cards
        - Otherwise, cancel the trade due to insufficient card count
        """

        # Redirect unauthenticated users to login
        if not request.user.is_authenticated:
            return reverse('login')

        # Fetch the trade request
        trade = TradeRequest.objects.get(pk=trade_pk)
        print(trade)  # Debug print

        # Mark sender as having accepted the trade
        trade.send_acc = True
        trade.save()

        # Proceed if both parties have accepted
        if trade.send_acc and trade.rcv_acc:
            # Ensure both cards are available for trade
            if trade.card1.count > 1 and trade.card2.count > 1:
                # Deduct one card from each party
                trade.card1.count -= 1
                trade.card1.save()

                trade.card2.count -= 1
                trade.card2.save()

                # Give card1 to receiver
                card_from_sender, created = OwnedBy.objects.get_or_create(
                    profile=trade.profile2,
                    card=trade.card1.card
                )
                if not created:
                    card_from_sender.count += 1
                print("Created: ", trade.profile2, trade.card1.card)
                card_from_sender.save()

                # Give card2 to sender
                card_from_receiver, created = OwnedBy.objects.get_or_create(
                    profile=trade.profile1,
                    card=trade.card2.card
                )
                if not created:
                    card_from_receiver.count += 1
                print("Created: ", trade.profile1, trade.card2.card)
                card_from_receiver.save()
            else:
                # Cancel trade if any party lacks sufficient card count
                trade.canceled = True
                trade.save()

        # Redirect to the user's trade list
        return redirect('trade', pk=self.get_profile().pk)
