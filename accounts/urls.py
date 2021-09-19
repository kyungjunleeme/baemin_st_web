from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# https://stackoverflow.com/questions/47065438/attributeerror-module-django-contrib-auth-views-has-no-attribute
urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
]
