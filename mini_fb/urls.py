from django.urls import path
from .views import ShowAllView, ShowProfilePageView

urlpatterns = [
    path('', ShowAllView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
]