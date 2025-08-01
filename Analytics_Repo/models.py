from django.db import models
from django.db.models import JSONField

# Create your models here.
class AdminReport(models.Model):
    report_name = models.CharField(max_length=100)
    generated_at = models.DateTimeField(auto_now_add=True)
    data = JSONField()

    def __str__(self):
        return f"{self.report_name}- {self.generated_at.date()}"
    