from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import LoginSerializer
from user.forms import UserSignupForm, UserLoginForm  
from .serializers import UserSerializer, ProfileSerializer
from user.models import User
from user_profile.models import UserProfile
from rest_framework.permissions import AllowAny

class SignupView(APIView):
    """
    API view for user registration
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully!', 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
class CreateAdminUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        password = request.data.get('password')
        email = request.data.get('email', '')
        first_name = request.data.get('firstname')
        last_name = request.data.get('lastname')
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(first_name=first_name, last_name=last_name, email=email, password=password)
            return Response({"detail": "Superuser created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Superuser already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    """
    API view for user login
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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