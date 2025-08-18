from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.conf import settings

user = get_user_model()

# Create your models here.
class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('Premium','Premium'),
    ]
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, default='Free')

    def __str__(self):
        return self.name

class SubPlan(models.Model):
    DURATION_CHOICES =[
        ('Monthly', 'Monthly'),
        ('Quarterly','Quarterly'),
        ('Half-Yearly','Half-Yearly'),
        ('Yearly', 'Yearly'),
    ]
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='subplans')
    name = models.CharField(max_length=20, choices=DURATION_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_in_days = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.plan.name} - {self.name}"
    
class UserSubscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    payment_history = models.JSONField(blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=255, blank = True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank = True, null=True)
    
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
    
class SubscriptionRenew(models.Model):
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    renewed_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.CASCADE)  # ✅ correct
    renewed_at = models.DateTimeField(auto_now_add=True)
    renewed_at_time= models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"Renewed: {self.user_subscription} by {self.renewed_by}"