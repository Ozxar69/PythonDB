from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
from .views import login_view, profile_view

app_name = "users"

urlpatterns = [
    path(
        "logout/",
        LogoutView.as_view(template_name="users/logged_out.html"),
        name="logout",
    ),
    path("login/", login_view, name="login"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("reset/", views.ResetPassword.as_view(), name="password_reset"),
    path("profile/<int:user_id>/", profile_view, name="profile"),
]
