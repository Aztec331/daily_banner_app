from django.db import models
from accounts.models import Company
#from subscriptions.models import Subscription
# Create your models here.

class BannerTemplate(models.Model):
    CATEGORY_CHOICES = [
        ('daily_thought','Daily Thought'),
        ('festival','Festival'),
        ('special','Special Occasion'),
    ]
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='banner_templates/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class UploadedMedia(models.Model):
    uploaded_by = models.ForeignKey('accounts.Company',on_delete=models.CASCADE)
    media_file = models.FileField(upload_to='media_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uploaded_by.username}-{self.media_file.name}"
    
    
class AdminActionLog(models.Model):
    admin = models.ForeignKey(Company, on_delete=models.CASCADE)
    action = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.admin.username}- {self.action[:30]}"