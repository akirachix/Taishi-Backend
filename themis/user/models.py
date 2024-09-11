from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Define choices for the role field
ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('judge', 'Judge'),
]

class User(AbstractUser):
    is_active = models.BooleanField(_('active'), default=True)
    role = models.CharField(_('role'), max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"