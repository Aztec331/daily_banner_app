from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard-overview"),  # GET /api/dashboard/
    path("banners/stats/", views.BannerStatsView.as_view(), name="dashboard-banners-stats"),  # GET /api/dashboard/banners/stats/
    path("template/usage/", views.TemplateUsageView.as_view(), name="dashboard-templates-usage"),  # GET /api/dashboard/template/usage/
    path("activities/", views.RecentActivitiesView.as_view(), name="dashboard-recent-activity"),  # GET /api/dashboard/activities/
]
