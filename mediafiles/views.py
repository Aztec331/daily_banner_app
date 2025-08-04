from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import MediaAsset
from .serializers import MediaAssetSerializer

class MediaListView(generics.ListAPIView):
    queryset= MediaAsset.objects.all()
    serializer_class = MediaAssetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MediaAsset.objects.filter(user=self.request.user)
    
class MediaUploadView(generics.CreateAPIView):
    queryset= MediaAsset.objects.all()
    serializer_class = MediaAssetSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] #MultiPartparser- images and videos #Formparser- text and names etc

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MediaDeleteView(generics.DestroyAPIView):
    queryset = MediaAsset.objects.all()
    serializer_class = MediaAssetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MediaAsset.objects.filter(user=self.request.user)
    