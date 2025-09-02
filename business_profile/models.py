from django.db import models
from django.conf import settings
import uuid


class BusinessProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='business_profiles'
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.URLField(blank=True, null=True)
    banner = models.URLField(blank=True, null=True)

    # JSON fields for flexibility
    social_media = models.JSONField(default=dict, blank=True)   # e.g. {"instagram": "...", "facebook": "..."}
    services = models.JSONField(default=list, blank=True)       # e.g. ["Haircut", "Shaving", "Facial"]
    working_hours = models.JSONField(default=dict, blank=True)  # e.g. {"mon-fri": "9-6", "sat": "10-4"}

    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"
