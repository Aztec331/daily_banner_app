from django.urls import path
from . import views
from banner.analytics_views import AdminAnalyticsView
from .views import BannerDownloadView, FontListView, FontCategoryView  # Make sure to import BannerDownloadView
from .views import UserBannersView
from .views import BannerUpdateView

urlpatterns = [
    # Templates
    path('templates/', views.TemplateListView.as_view(), name='template-list'),
    path('templates/<int:pk>/', views.TemplateDetailView.as_view(), name='template-detail'),
    path('templates/languages/', views.TemplateLanguagesView.as_view(), name='template-languages'),

    # Banners
    path('banners/', views.BannerCreateView.as_view(), name='banner-create'),
    path('banner/<int:pk>/', views.BannerDetailView.as_view(), name='banner-detail'),
    path('banner/<int:pk>/delete/', views.BannerDeleteView.as_view(), name='banner-delete'),
    path('admin/analytics/', AdminAnalyticsView.as_view(), name='admin-analytics'),
    path('banner/<int:pk>/download/', BannerDownloadView.as_view(), name='banner-download'),
    path('banners/<int:pk>/', BannerUpdateView.as_view(), name='banner-update'),
    path('banners/my/', UserBannersView.as_view(), name='user-banners'), #example- http://127.0.0.1:8000/api/banners/my/?status=draft&page=1&limit=3

    #Fonts
    path('fonts/', FontListView.as_view(), name='font-list'),
    path('fonts/categories/', FontCategoryView.as_view(), name='font-categories'),
]
