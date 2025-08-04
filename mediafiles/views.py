from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Media
from .serializers import MediaSerializer

class MediaListView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [AllowAny]

class MediaUploadView(generics.CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [AllowAny]

class MediaDeleteView(generics.DestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
