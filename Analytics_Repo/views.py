from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.utils.timezone import now, timedelta

from accounts.models import CustomUser
from subscription.models import UserSubscription
# Create your views here.

class AdminAnalyticsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        today = now().date()
        week_start = today - timedelta(days=7)

        total_users = CustomUser.objects.count()
        active_users = CustomUser.objects.filter(is_active=True).count()
        total_subscription = UserSubscription.objects.count()

        return Response({
            "total Users": total_users,
            "active Users": active_users,
            "subscriptions": total_subscription,
        })