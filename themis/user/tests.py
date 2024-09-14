from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class UserModelTests(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user_with_valid_email(self):
        user = self.User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            role="judge",
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password123"))
        self.assertTrue(user.is_active)
        self.assertEqual(user.role, "judge")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError) as context:
            self.User.objects.create_user(
                email="",
                password="password123",
                first_name="Test",
                last_name="User",
                role="judge",
            )
        self.assertEqual(str(context.exception), _("The Email field must be set"))

    def test_create_superuser(self):
        superuser = self.User.objects.create_superuser(
            email="superuser@example.com",
            password="password123",
            first_name="Super",
            last_name="User",
            role="admin",
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertEqual(superuser.role, "admin")

    def test_create_superuser_with_invalid_permissions(self):
        with self.assertRaises(ValueError) as context:
            self.User.objects.create_superuser(
                email="superuser@example.com",
                password="password123",
                first_name="Super",
                last_name="User",
                role="admin",
                is_staff=False,
            )
        self.assertEqual(
            str(context.exception), _("Superuser must have is_staff=True.")
        )

        with self.assertRaises(ValueError) as context:
            self.User.objects.create_superuser(
                email="superuser@example.com",
                password="password123",
                first_name="Super",
                last_name="User",
                role="admin",
                is_superuser=False,
            )
        self.assertEqual(
            str(context.exception), _("Superuser must have is_superuser=True.")
        )
