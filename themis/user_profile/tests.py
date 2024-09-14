from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from .models import UserProfile


class UserProfileTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email="test@example.com",
            password="securepassword",
            first_name="John",
            last_name="Doe",
            role="judge",
        )

    def test_create_user_profile(self):
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.user, self.user)
        self.assertTrue(
            profile.profile_picture is None or profile.profile_picture.name == ""
        )

        # Testing picture upload

    def test_profile_picture_upload(self):
        file_path = "/home/student/Downloads/latifa.png"
        with open(file_path, "rb") as f:
            image_content = f.read()
        image = SimpleUploadedFile(
            name="latifa.png", content=image_content, content_type="image/png"
        )
        profile = UserProfile.objects.get(user=self.user)
        profile.profile_picture = image
        profile.save()
        profile.refresh_from_db()

        # Printing profile picture details
        print(f"Profile picture name: {profile.profile_picture.name}")
        print(
            f"Profile picture exists: {profile.profile_picture.storage.exists(profile.profile_picture.name)}"
        )
