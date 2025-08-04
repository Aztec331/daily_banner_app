from django.db import models
from django.conf import settings

class MediaAsset(models.Model):
    MEDIA_TYPE_CHOICES= [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media_assets/')
    media_type= models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    uploaded_at= models.DateTimeField(auto_now_add=True)

    def __str___(self):
        return f"{self.media_type} uploaded by {self.user.email}"