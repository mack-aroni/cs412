# File: urls.py
# Author: Ethan Macheder (emach@bu.edu) April 15, 2025
# Description: URL patterns for the trading card app.
# Maps paths to views for profile access, card trading, pack selection,
# friend system (requests, suggestions, removal), authentication, and catalog browsing.

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    # Landing or profile redirect
    path('', LoginOrProfileView.as_view(), name="landing"),

    # Profile and catalog views
    path('profile/', LoginOrProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', PocketProfileView.as_view(), name='pocket_profile'),
    path('catalog/', CardCatalogView.as_view(), name='catalog'),
    path('packs/', PackSelectView.as_view(), name='packs'),

    # Trade operations
    path('trade/<int:pk>', TradeHubView.as_view(), name='trade'),
    path('trade/manage/<int:type>/<int:sender_pk>/<int:receiver_pk>', TradeOptionsView.as_view(), name='trade_options'),
    path('trade/create/<int:sender_pk>/<int:receiver_pk>/<int:card_pk>', CreateTradeView.as_view(), name='create_trade'),
    path('trade/add/<int:trade_pk>', TradeOptionsView.as_view(), name='trade_add'),
    path('trade/accept/<int:trade_pk>/<int:card_pk>', AcceptTradeView.as_view(), name='accept_trade'),
    path('trade/finalize/<int:trade_pk>', FinalizeTradeView.as_view(), name='trade_finalize'),

    # Friend system: requests, actions, and suggestions
    path('friend/requests/', FriendRequestListView.as_view(), name='friend_requests'),
    path('friend/suggestions/', FriendSuggestionListView.as_view(), name="friend_suggestions"),
    path('send-request/<int:profile_id>/', SendFriendRequestView.as_view(), name='send_request'),
    path('cancel-request/<int:profile_id>/', CancelFriendRequestView.as_view(), name='cancel_request'),
    path('accept-request/<int:profile_id>/', AcceptFriendRequestView.as_view(), name='accept_request'),
    path('decline-request/<int:profile_id>/', DeclineFriendRequestView.as_view(), name='decline_request'),
    path('remove-friend/<int:profile_id>/', RemoveFriendView.as_view(), name='remove_friend'),

    # Auth and registration
    path('register/', CreatePocketProfile.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
