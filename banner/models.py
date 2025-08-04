from django.db import models
from django.db import models
from django.conf import settings


class Template(models.Model):
    CATEGORY_CHOICES = [
        ('daily', 'Daily'),
        ('festival', 'Festival'),
        ('special', 'Special'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    template_image = models.ImageField(max_length=255)  # or use ImageField if handling file uploads
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.category})"


class Banner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True)
    banner_image = models.ImageField(max_length=255)  # or use ImageField
    text_content = models.TextField(blank=True, null=True)
    custom_name = models.CharField(max_length=100, blank=True, null=True)
    custom_logo = models.CharField(max_length=255, blank=True, null=True)  # or ImageField
    custom_photo = models.CharField(max_length=255, blank=True, null=True)  # or ImageField
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Banner #{self.id} by {self.user.email}"
