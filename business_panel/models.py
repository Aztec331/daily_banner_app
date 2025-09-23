# business_panel/models.py
from django.db import models
from django.conf import settings

class Business(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True, default="No address")
    email = models.EmailField(null=True, blank=True, default="noemail@example.com")
    logo = models.ImageField(null=True, blank=True, default="https://example.com/logo.png")
    phone = models.CharField(max_length=20, null=True, blank=True, default="0000000000")
    tagline = models.CharField(max_length=255, null=True, blank=True, default="")
    banner = models.ImageField(upload_to="business/banners/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class BusinessUpload(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="business_panel_uploads"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)

    logo = models.ImageField(upload_to="business_profiles/logos/", blank=True, null=True)
    banner = models.ImageField(upload_to="business_profiles/banners/", blank=True, null=True)

    def __str__(self):
        return self.name