from django.contrib import admin

# Register your models here.
from .models import SubscriptionPlan, UserSubscription, SubscriptionHistory, SubscriptionStatus, SubPlan

admin.site.register(SubscriptionPlan)
admin.site.register(SubPlan)
admin.site.register(UserSubscription)
admin.site.register(SubscriptionHistory)
admin.site.register(SubscriptionStatus)