# authapp/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("hemis/login/", views.hemis_login),
    path("callback/hemis", views.hemis_callback),
]
