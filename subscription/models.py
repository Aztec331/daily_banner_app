from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

user = get_user_model()

# Create your models here.
class SubscriptionPlan(models.Model):
    PLAN_CATEGORIES = [
        ('daily','daily'),
        ('festival','festival'),
        ('premium','premium'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    category = models.CharField(max_length=20,choices=PLAN_CATEGORIES,default='daily')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.duration_days} days)"
    
class UserSubscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    payment_history = models.JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.end_date and self.plan:
            self.end_date = timezone.now() + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name if self.plan else 'No Plan'}"
    
class SubscriptionHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=50)  # e.g. 'active', 'cancelled'
    action = models.CharField(max_length=20, choices=[('subscribed', 'Subscribed'), ('cancelled', 'Cancelled')])
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.status}"
    
class SubscriptionStatus(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    current_status = models.CharField(max_length=50)  # e.g., 'active', 'expired', 'cancelled'
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.current_status}"