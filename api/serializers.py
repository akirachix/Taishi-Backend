

from rest_framework import serializers
from user.models import User
from user_profile.models import UserProfile
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
            "is_active",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"password": {"write_only": True}}
    def create(self, validated_data):
        if User.objects.filter(email=validated_data["email"]).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."}
            )
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=["first_name", ""],
            last_name=["last_name", ""],
            role=validated_data.get("role", "user"),
        )
        return user
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ["user", "profile_picture"]