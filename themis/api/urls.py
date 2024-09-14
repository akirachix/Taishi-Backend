from django.urls import path
from .views import SignupView, LoginView, UserDetailView, UserListView, ProfileListView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="user_signup"),
    path("login/", LoginView.as_view(), name="user_login"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("profiles/", ProfileListView.as_view(), name="profile_list"),
]
