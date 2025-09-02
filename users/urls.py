# authapp/urls.py
from django.urls import path
from .views import hemis_callback

urlpatterns = [
    path("hemis/callback/", hemis_callback, name="hemis_callback"),
]
