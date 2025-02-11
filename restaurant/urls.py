from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [ 
    path(r'', views.main, name="main"),
    path(r'order', views.order, name="order"),
    # path(r'confirmation', views.confirmation, name="confirmation"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
