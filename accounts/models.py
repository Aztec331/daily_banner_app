from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CompanyManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CompanyDetails(AbstractBaseUser, PermissionsMixin):
    BUSINESS_CATEGORY_CHOICES = [
        ('Event Planners', 'Event Planners'),
        ('Decorators', 'Decorators'),
        ('Sound Suppliers', 'Sound Suppliers'),
        ('Light Suppliers', 'Light Suppliers'),
        ('Video Services', 'Video Services'),
    ]

    company_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, db_index=True)  # required
    password = models.CharField(max_length=128)  # required
    is_active = models.BooleanField(default=True)  # required
    last_login = models.DateTimeField(null=True, blank=True)  # optional
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone_no = models.CharField(max_length=20)
    alternate_phone_no = models.CharField(max_length=20, blank=True, null=True)
    business_category = models.CharField(max_length=50, choices=BUSINESS_CATEGORY_CHOICES)
    company_website = models.URLField(blank=True, null=True)
    company_logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    objects = CompanyManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name', 'business_category', 'phone_no', 'company_address']

    class Meta:
        app_label = 'accounts'

    def __str__(self):
        return self.company_name
