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
    template_image = models.ImageField(upload_to='templates/')  # or use ImageField if handling file uploads
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.category})"

#------------------------------------------------------------------------------------------------------------------------
#Banner models
class Banner(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey(
        Template, on_delete=models.SET_NULL, null=True, blank=True, related_name='banners'
    )

    custom_name = models.CharField(max_length=100)  # Banner Title
    description = models.TextField(blank=True, null=True)  # Banner Description
    text_content = models.TextField(blank=True, null=True)  # customizations.text
    custom_image = models.URLField(blank=True, null=True)  # customizations.image
    language = models.CharField(
        max_length=5,
        choices=[('en', 'English'), ('hi', 'Hindi'), ('mr', 'Marathi')],
        default='en'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Banner #{self.id} - {self.custom_name} by {self.user.email}"

#-------------------------------------------------------------------
#Font models
class Font(models.Model):
    CATEGORY_CHOICES = [
        ('serif', 'Serif'),
        ('sans-serif', 'Sans-Serif'),
        ('display', 'Display'),
        ('script', 'Script'),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('mr', 'Marathi'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES)
    url = models.URLField()  # link to font file if needed

    def __str__(self):
        return self.name
