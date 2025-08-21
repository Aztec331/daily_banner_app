from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class GreetingCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class GreetingTemplate(models.Model):
    category = models.ForeignKey(GreetingCategory, on_delete=models.CASCADE, related_name="templates")
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="greeting_templates/")
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_templates")
    created_at = models.DateTimeField(auto_now_add=True)
    default_text = models.TextField(blank=True, null=True)
    default_background = models.URLField(blank=True, null=True)
    default_stickers  = models.JSONField(default=list,blank=True, null=True)
    default_emojis = models.JSONField(default=list,blank=True, null=True)
    layout = models.CharField(max_length=50, choices=[('vertical','Vertical'),('horizontal','Horizontal')], default='vertical')
    language = models.CharField(max_length=50, default='en')
    is_premium = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    customizations = models.JSONField(default=dict, blank=True, null=True)
    tags = models.JSONField(default=list, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    
def __str__(self):
    return self.title


class Greeting(models.Model):
    template = models.ForeignKey(GreetingTemplate, on_delete=models.CASCADE, related_name="greetings")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_greetings")
    recipient_email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    customizations = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"Greeting from {self.sender.username} to {self.recipient_email}"


class GreetingTemplateLike(models.Model):
    template = models.ForeignKey(GreetingTemplate, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="template_likes")
    created_at = models.DateTimeField(auto_now_add=True) #set once when created
    liked_at = models.DateTimeField(auto_now=True) #updated every time the like is toggled
    
    

    class Meta:
        unique_together = ("template", "user")  # prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} liked {self.template.title}"


class GreetingTemplateDownload(models.Model):
    template = models.ForeignKey(GreetingTemplate, on_delete=models.CASCADE, related_name="downloads")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="template_downloads")
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} downloaded {self.template.title}"
