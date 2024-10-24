# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),  # Login page
    path(
        "get_token/", views.get_token_view, name="get_token"
    ),  # Callback URL for handling token
    path(
        "get_users/", views.get_users_view, name="get_users"
    ),  # Fetch users from Microsoft Graph
]
