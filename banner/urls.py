from django.urls import path
from . import views
from banner.analytics_views import AdminAnalyticsView
from .views import FontListView, FontCategoryView
from .views import UserBannersView
from .views import BannerUpdateView
from .views import PublishBannerAPIView, ArchiveBannerAPIView
from .views import ExportBannerAPIView
from .views import TemplateLikeView
from .views import TemplateDownloadView
from .views import TemplateCategoriesView
from .views import TemplateAnalyticsView, LikedTemplatesView, DownloadedTemplatesView
from .views import TemplateRecommendationsView

urlpatterns = [
    # Templates
    path('templates/', views.TemplateListView.as_view(), name='template-list'),
    path('templates/<int:id>/', views.TemplateDetailView.as_view(), name='template-detail'),
    path('templates/languages/', views.TemplateLanguagesView.as_view(), name='template-languages'),
    path("templates/<int:id>/like/", TemplateLikeView.as_view(), name="template-like"),
    path("templates/<int:id>/download/", TemplateDownloadView.as_view(), name="template-download"),
    path("templates/categories/", TemplateCategoriesView.as_view(), name="template-categories"),
    path('templates/<int:id>/analytics/', TemplateAnalyticsView.as_view(), name='template-analytics'),
    path('templates/liked/', LikedTemplatesView.as_view(), name='liked-templates'),
    path("templates/downloaded/", DownloadedTemplatesView.as_view(), name="downloaded-templates"),
    path("templates/recommendations/", TemplateRecommendationsView.as_view(), name="template-recommendations"),

    # Banners
    path('banners/', views.BannerCreateView.as_view(), name='banner-create'),
    path('banners/<int:id>/', views.BannerDetailView.as_view(), name='banner-detail'),
    path('admin/analytics/', AdminAnalyticsView.as_view(), name='admin-analytics'),
    path('banners/<int:id>/', BannerUpdateView.as_view(), name='banner-update'),
    path('banners/my/', UserBannersView.as_view(), name='user-banners'), #example- http://127.0.0.1:8000/api/banners/my/?status=draft&page=1&limit=3
    path('banners/<int:id>/publish/', PublishBannerAPIView.as_view(), name='publish-banner'),
    path('banners/<int:id>/archive/', ArchiveBannerAPIView.as_view(), name='archive-banner'),
    path('banners/<int:id>/export/', ExportBannerAPIView.as_view(), name='export-banner'),

    #Fonts
    path('fonts/', FontListView.as_view(), name='font-list'),
    path('fonts/categories/', FontCategoryView.as_view(), name='font-categories'),  
]
