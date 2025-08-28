from django.db import models
from django.conf import settings  # to use your custom auth user


class Transaction(models.Model):
    id = models.CharField(max_length=100, primary_key=True)   # or use UUIDField
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    status = models.CharField(max_length=50)   # e.g., SUCCESS, FAILED, PENDING
    plan = models.CharField(max_length=100, blank=True, null=True)
    plan_name = models.CharField(max_length=150, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    method = models.CharField(max_length=50, blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.user} - {self.status} ({self.amount} {self.currency})"
