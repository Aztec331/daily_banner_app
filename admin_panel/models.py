from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
user = get_user_model()
class BannerTemplate(models.Model):
    CATEGORY_CHOICES= [
        ('Daily','Daily Thought'),
        ('festival','Festival'),
        ('custom','Custom'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    file = models.FileField(upload_to='templates/')
    created_at = models.DateTimeField(auto_now_add =True)

    def __str__(self):
        return self.title
    
class AdminActivityLog(models.Model):
    admin_user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)