from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from user.forms import UserSignupForm, UserLoginForm  
from .serializers import UserSerializer, ProfileSerializer
from user.models import User
from user_profile.models import UserProfile

class SignupView(APIView):
    """
    API view for user registration
    """
    def get(self, request):
        form = UserSignupForm()
        return render(request, 'user/signup.html', {'form': form})

    def post(self, request):
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
        return render(request, 'user/signup.html', {'form': form})

class LoginView(APIView):
    """
    API view for user login
    """
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('some_dashboard_url') 
            else:
                return render(request, 'user/login.html', {'form': form, 'error': 'Invalid credentials'})
        return render(request, 'user/login.html', {'form': form})


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve or update user profile
    """
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'pk' 


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve or update a specific user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk' 


class UserListView(generics.ListAPIView):
    """
    API view to retrieve the list of users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileListView(generics.ListAPIView):
    """
    API view to retrieve the list of all profiles
    """
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer