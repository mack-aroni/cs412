from django.urls import path
from .views import ShowAllView, ShowProfilePageView #, RandomArticleView

urlpatterns = [
    path('', ShowAllView.as_view(), name="show_all_profiles"),
    # path('show_all', ShowAllView.as_view(), name="show_all"), # modified
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
]