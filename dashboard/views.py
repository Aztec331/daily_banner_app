from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone
from django.db.models import Count, Sum
from datetime import timedelta

# Import models
from greetings.models import Greeting, GreetingTemplate, GreetingTemplateLike, GreetingTemplateDownload
from banner.models import Banner
from subscription.models import UserSubscription as Subscription
from mediafiles.models import Media as MediaFile
from accounts.models import CompanyDetails

from .serializers import (
    DashboardSerializer,
    RecentActivitySerializer,
    BannersDataSerializer,
    TemplateUsageItemSerializer,
)

class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 1. Greetings Data
        greetings_data = {
            "total_greetings_sent": Greeting.objects.filter(sender=request.user).count(),
            "total_templates_used": Greeting.objects.filter(sender=request.user).values('template').distinct().count(),
            "total_likes": GreetingTemplateLike.objects.filter(user=request.user).count(),
            "total_downloads": GreetingTemplateDownload.objects.filter(user=request.user).count()
        }

        # 2. Banners Data
        banners_data = {
            "total_banners": Banner.objects.count(),
            "active_banners": Banner.objects.filter(created_at__gte=timezone.now() - timedelta(days=30)).count(),
            "recently_created": Banner.objects.filter(created_at__gte=timezone.now() - timedelta(days=7)).count()
        }

        # 3. Subscriptions Data
        subscriptions_data = {
            "active_subscriptions": Subscription.objects.filter(user=request.user, is_active=True).count(),
            "expired_subscriptions": Subscription.objects.filter(user=request.user, is_active=False).count()
        }

        # 4. Media Files Data
        # Sum sizes safely without relying on a DB column (handles legacy DBs without 'size')
        try:
            total_size_bytes = sum(getattr(m.file, 'size', 0) or 0 for m in MediaFile.objects.all())
        except Exception:
            total_size_bytes = 0

        mediafiles_data = {
            "total_files": MediaFile.objects.count(),
            "total_size": total_size_bytes
        }

        # 5. Users Data
        users_data = {
            "total_users": CompanyDetails.objects.count(),
            "active_users": CompanyDetails.objects.filter(is_active=True).count()
        }

        # 6. Recent Activities (last 10)
        greetings_activities = Greeting.objects.filter(sender=request.user).order_by('-created_at')[:10]
        downloads_activities = GreetingTemplateDownload.objects.filter(user=request.user).order_by('-downloaded_at')[:10]
        likes_activities = GreetingTemplateLike.objects.filter(user=request.user).order_by('-liked_at')[:10]

        activities = []
        for g in greetings_activities:
            activities.append({
                "user": g.sender.username,
                "action": "sent",
                "template_or_banner": g.template.title,
                "timestamp": g.created_at
            })
        for d in downloads_activities:
            activities.append({
                "user": d.user.username,
                "action": "downloaded",
                "template_or_banner": d.template.title,
                "timestamp": d.downloaded_at
            })
        for l in likes_activities:
            activities.append({
                "user": l.user.username,
                "action": "liked",
                "template_or_banner": l.template.title,
                "timestamp": l.liked_at
            })

        # Sort by timestamp descending and limit to 10
        activities = sorted(activities, key=lambda x: x["timestamp"], reverse=True)[:10]

        dashboard_data = {
            "greetings": greetings_data,
            "banners": banners_data,
            "subscriptions": subscriptions_data,
            "mediafiles": mediafiles_data,
            "users": users_data,
            "recent_activities": activities
        }

        serializer = DashboardSerializer(dashboard_data)
        return Response(serializer.data)


class BannerStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            "total_banners": Banner.objects.count(),
            "active_banners": Banner.objects.filter(created_at__gte=timezone.now() - timedelta(days=30)).count(),
            "recently_created": Banner.objects.filter(created_at__gte=timezone.now() - timedelta(days=7)).count(),
        }
        return Response(BannersDataSerializer(data).data)


class TemplateUsageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        usage = (
            Greeting.objects
            .filter(sender=request.user)
            .values("template__id", "template__title")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        serialized = [
            TemplateUsageItemSerializer({
                "template_id": item["template__id"],
                "template_title": item["template__title"],
                "usage_count": item["count"],
            }).data
            for item in usage
        ]
        return Response(serialized)


class RecentActivitiesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        greetings_activities = Greeting.objects.filter(sender=request.user).order_by('-created_at')[:10]
        downloads_activities = GreetingTemplateDownload.objects.filter(user=request.user).order_by('-downloaded_at')[:10]
        likes_activities = GreetingTemplateLike.objects.filter(user=request.user).order_by('-liked_at')[:10]

        activities = []
        for g in greetings_activities:
            activities.append({
                "user": g.sender.username,
                "action": "sent",
                "template_or_banner": g.template.title,
                "timestamp": g.created_at
            })
        for d in downloads_activities:
            activities.append({
                "user": d.user.username,
                "action": "downloaded",
                "template_or_banner": d.template.title,
                "timestamp": d.downloaded_at
            })
        for l in likes_activities:
            activities.append({
                "user": l.user.username,
                "action": "liked",
                "template_or_banner": l.template.title,
                "timestamp": l.liked_at
            })

        activities = sorted(activities, key=lambda x: x["timestamp"], reverse=True)[:10]
        return Response([RecentActivitySerializer(a).data for a in activities])
