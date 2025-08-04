from django.urls import path
from .views import MediaListView, MediaUploadView, MediaDeleteView

urlpatterns = [
    path('media/', MediaListView.as_view()),
    path('media/upload/', MediaUploadView.as_view()),
    path('media/<int:pk>/', MediaDeleteView.as_view()),
]
