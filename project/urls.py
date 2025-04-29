# File: urls.py
# Author: Ethan Macheder (emach@bu.edu) April 15, 2025
# Description: 

from django.urls import path

from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', LoginOrProfileView.as_view(), name="landing"),
    path('profile/', TempHome.as_view(), name='profile'),
    path('catalog/', CardCatalogView.as_view(), name='catalog'),
    path('packs/', PackSelectView.as_view(), name='packs'),

    path('trade/<int:pk>', TradeHubView.as_view(), name='trade'),
    path('trade/manage/<int:type>/<int:sender_pk>/<int:receiver_pk>', TradeOptionsView.as_view(), name='trade_options'),
    path('trade/create/<int:sender_pk>/<int:receiver_pk>/<int:card_pk>', CreateTradeView.as_view(), name='create_trade'),
    path('trade/add/<int:trade_pk>', TradeOptionsView.as_view(), name='trade_add'),
    path('trade/accept/<int:trade_pk>/<int:card_pk>', AcceptTradeView.as_view(), name='accept_trade'),    
    path('trade/finalize/<int:trade_pk>', FinalizeTradeView.as_view(), name='trade_finalize'),


    path('friend/suggestions/', ShowPocketFriendSuggestionsView.as_view(), name="friend_suggestions"),
    path('friend/add/<int:friend_pk>', AddPocketFriendView.as_view(), name='add_friend'),

    path('register/', CreatePocketProfile.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]