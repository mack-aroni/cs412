# File: urls.py
# Author: Ethan Macheder (emach@bu.edu) May 3, 2025
# Description: This file defines the URL patterns for the voter_analytics app.
# It maps URLs to the appropriate views for listing voters, viewing details,
# and displaying visual analytics.

from django.urls import path
from .views import *

urlpatterns = [
    # Display a paginated, filterable list of voters
    path('', VoterListView.as_view(), name='voters'),

    # Display detailed information for a single voter (by primary key)
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'),

    # Display charts and graphs summarizing voter data
    path('graphs/', GraphsView.as_view(), name='graphs'),
]
