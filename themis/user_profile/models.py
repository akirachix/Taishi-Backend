from django.db import models

class Profile(models.Model):
    profile_ID = models.AutoField(primary_key=True)
    user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"