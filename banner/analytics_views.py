from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.utils.timezone import now
from datetime import timedelta
from banner.models import Banner
from accounts.models import CompanyDetails
from subscription.models import UserSubscription

class AdminAnalyticsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        today = now().date()
        week_start = today - timedelta(days=7)

        total_banners = Banner.objects.count()
        total_users = CompanyDetails.objects.count()
        active_users = CompanyDetails.objects.filter(is_active=True).count()
        total_subscription = UserSubscription.objects.count()

        banners_used_today = Banner.objects.filter(created_at__date=today).count()
        banners_user_week = Banner.objects.filter(created_at__date__gte=week_start).count()

        return Response({
            "total_banners": total_banners,
            "total_users": total_users,
            "active_users": active_users,
            "subscriptions": total_subscription,
            "banners_used_today": banners_used_today,
            "banners_user_week": banners_user_week
        })
