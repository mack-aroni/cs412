from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [ 
    path(r'', views.show_form, name="show_form"),
    path(r'submit', views.submit, name="submit"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
