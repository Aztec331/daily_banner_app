from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessProfileViewSet

router = DefaultRouter()
router.register(r'business-profiles', BusinessProfileViewSet, basename='businessprofile')

urlpatterns = [
    path('', include(router.urls)),  # no extra "api/business-profile/"
]
