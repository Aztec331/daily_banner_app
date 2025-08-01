from django.urls import path
from .views import MediaListView, MediaUploadView, MediaDeleteView

urlpatterns = [
    path('api/media', MediaListView.as_view()),
    path('api/media/upload', MediaUploadView.as_view()),
    path('api/media/<int:pk>', MediaDeleteView.as_view()),
]
