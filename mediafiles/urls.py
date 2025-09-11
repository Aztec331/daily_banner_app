from django.urls import path
from .views import (
    MediaListView,
    MediaUploadView,
    MediaRetrieveDeleteView,
    MediaByTypeView,
    MediaSearchView,
    MediaStatsView
)

urlpatterns = [
    path("media/", MediaListView.as_view(), name="media-list"),  # GET list with pagination , example- http://127.0.0.1:8000/api/media?page=1&limit=10
    path("media/upload/", MediaUploadView.as_view(), name="media-upload"),  # POST upload
    path("media/<int:pk>/",MediaRetrieveDeleteView.as_view(),name="media-detail-update-delete"),  # GET, PUT, DELETE
    path("media/type/<str:type>/", MediaByTypeView.as_view(), name="media-by-type"),
    path('media/search/', MediaSearchView.as_view(), name='media-search'),
    path('media/stats/', MediaStatsView.as_view(), name='media-stats'),
]
