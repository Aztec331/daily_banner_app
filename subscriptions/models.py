from django.db import models
from accounts.models import CustomUser

# Create your models here.
SUBSCRIPTION_CHOICES = [
    ('free', 'Free'),
    ('premium', 'Premium'),
    ('pro', 'Pro'),
]

SUBSCRIPTION_STATUS = [
    ('active', 'Active'),
    ('expired', 'Expired'),
    ('cancelled', 'Cancelled'),
    ('pending', 'Pending'),
]

class Subscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=10, choices=SUBSCRIPTION_CHOICES, default='free')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=SUBSCRIPTION_STATUS, default='pending')
    payment_reference = models.CharField(max_length=255, null=True, blank=True)


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    features = models.TextField(blank=True)

class UserSubscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=SUBSCRIPTION_STATUS, default='pending')
    payment_reference = models.CharField(max_length=255, null=True, blank=True)
