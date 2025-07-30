from django.db import models
from accounts.models import CustomUser
#from subscriptions.models import Subscription
# Create your models here.
class AdminActionLog(models.model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)