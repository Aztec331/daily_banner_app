from django.db import models
from django.contrib.auth.models import AbstractUser

USER_TYPE_CHOICES = [
    ('user', 'User'),
    ('admin', 'Admin'),
]
class CompanyDetails(models.Model):
    name = models.CharField(max_length= 100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone= models.CharField(max_length=15, null = True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    company_details = models.OneToOneField(CompanyDetails,on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')  # 👈 New field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone','username']

    def __str__(self):
        return f"{self.email} ({self.user_type})"
 

