from django.urls import path
from .views import MediaListView, MediaUploadView, MediaDeleteView

urlpatterns = [
    path('media/', MediaListView.as_view(), name='media-list'),
    path('media/upload/', MediaUploadView.as_view(), name='media-upload'),
    path('media/<int:id>/', MediaDeleteView.as_view(), name='media-delete'),
]
