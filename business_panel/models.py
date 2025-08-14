# business_panel/models.py
from django.db import models
from django.conf import settings
<<<<<<< HEAD

class Business(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True, default="No address")
    email = models.EmailField(null=True, blank=True, default="noemail@example.com")
    logo = models.ImageField(null=True, blank=True, default="https://example.com/logo.png")
    phone = models.CharField(max_length=20, null=True, blank=True, default="0000000000")
    tagline = models.CharField(max_length=255, null=True, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

=======

class Business(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True, default="No address")
    email = models.EmailField(null=True, blank=True, default="noemail@example.com")
    logo = models.ImageField(null=True, blank=True, default="https://example.com/logo.png")
    phone = models.CharField(max_length=20, null=True, blank=True, default="0000000000")
    tagline = models.CharField(max_length=255, null=True, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
>>>>>>> e5c64f20f21b679e927217597826b664eba451a4
