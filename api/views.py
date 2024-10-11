

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model  # Use get_user_model for custom user models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from user.permissions import HasAdminPermissions
from .serializers import LoginSerializer
from user.forms import UserSignupForm, UserLoginForm
from .serializers import UserSerializer
from user.models import User
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from user.forms import UserSignupForm, UserLoginForm
from .serializers import UserSerializer, ProfileSerializer, LoginSerializer
from user_profile.models import UserProfile
User = get_user_model()
class SignupView(APIView):
    """
    API view for user registration
    """
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User created successfully!",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CreateAdminUser(APIView):
    """
    API view to create a new admin user.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        password = request.data.get("password")
        email = request.data.get("email", "")
        first_name = request.data.get("firstname")
        last_name = request.data.get("lastname")
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            return Response(
                {"detail": "Superuser created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"detail": "Superuser already exists"}, status=status.HTTP_400_BAD_REQUEST
        )
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if not all([username, password, first_name, last_name]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(email=email).exists():
            try:
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                return Response({'message': 'Superuser created successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Superuser already exists"}, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    """
    API view for user login
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, email=email, password=password)
            if user:
                return Response(
                    {
                        "message": "Login successful!",
                        "user": {
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                        }
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve or update a specific user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"
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
    
class CreateAdminUser(APIView):
    """
    API view to create a new admin user.
    """
    
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve or update user profile
    """
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        if not all([username, password, first_name, last_name]):
            return Response(
                {"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_superuser=True,
                is_staff=True,
                role="admin",
            )
            return Response(
                {"message": "Admin user created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def get_object(self):
        return self.request.user.profile
    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class JudgeUser(APIView):
    """
    API view to create a new judge user.
    """
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        if not all([username, password, first_name, last_name]):
            return Response(
                {"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role="judge",
            )
            return Response(
                {"message": "Judge user created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
def generate_token(request):
    email = request.GET.get('email', 'default_email@example.com')
    user, created = User.objects.get_or_create(email=email)
    refresh = RefreshToken.for_user(user)
    return JsonResponse({
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    })