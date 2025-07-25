from django.db import models
from django.contrib.auth.models import AbstractUser

USER_TYPE_CHOICES = [
    ('user', 'User'),
    ('admin', 'Admin'),
]

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    user_logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    user_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')  # 👈 New field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.user_type})"
