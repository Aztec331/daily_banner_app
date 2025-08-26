from django.db import models

class Media(models.Model):
    FILE_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    CATEGORY_CHOICES = [
        ('daily', 'Daily'),
        ('festival', 'Festival'),
        ('general', 'General'),
    ]

    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file = models.FileField(upload_to='uploads/')
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField()  # size in bytes

    def __str__(self):
        return self.file_name
