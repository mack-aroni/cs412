from django.urls import path
from .views import *

urlpatterns = [
    path('', ResultView.as_view(), name='home'),
]