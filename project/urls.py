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

    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]