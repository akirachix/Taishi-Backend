from django.urls import path
from .views import SignupView, LoginView, UserDetailView, UserListView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='user_signup'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/', UserListView.as_view(), name='user_list'),

]
