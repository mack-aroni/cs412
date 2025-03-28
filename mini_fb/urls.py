# File: urls.py
# Author: Ethan Macheder (emach@bu.edu) Feb 21, 2025
# Description: This file defines the URL patterns for the mini_fb app.
# It maps the URLs of various views to corresponding Django view functions or classes.
# These include paths for displaying all profiles, managing profile creation,
# updating profiles, handling status messages, managing friend suggestions, 
# and adding friends.

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', ShowAllView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/create_status', CreateStatusMessageView.as_view(), name="create_status"),
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path('profile/friend_suggestions', ShowFriendSuggestionsView.as_view(), name="show_friend_suggestions"),    path('profile/news_feed', ShowNewsFeedView.as_view(), name="show_news_feed"),
    path('profile/add_friend/<int:friend_pk>', AddFriendView.as_view(), name="add_friend"),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update', UpdateStatusView.as_view(), name="update_status"),
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]