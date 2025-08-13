from django.urls import path
from . import views
from banner.analytics_views import AdminAnalyticsView
from .views import BannerDownloadView  # Make sure to import BannerDownloadView

urlpatterns = [
    # Templates
    path('templates/', views.TemplateListView.as_view(), name='template-list'),
    path('template/<int:pk>/', views.TemplateDetailView.as_view(), name='template-detail'),

    # Banners
    path('banner/create/', views.BannerCreateView.as_view(), name='banner-create'),
    path('banner/<int:pk>/update/', views.BannerUpdateView.as_view(), name='banner-update'),
    path('banner/mine/', views.MyBannersListView.as_view(), name='banner-mine'),
    path('banner/<int:pk>/', views.BannerDetailView.as_view(), name='banner-detail'),
    path('banner/<int:pk>/delete/', views.BannerDeleteView.as_view(), name='banner-delete'),
    path('admin/analytics/', AdminAnalyticsView.as_view(), name='admin-analytics'),
    path('banner/<int:pk>/download/', BannerDownloadView.as_view(), name='banner-download'),
]
