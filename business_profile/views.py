from rest_framework import viewsets, permissions
from .models import BusinessProfile
from .serializers import BusinessProfileSerializer

class BusinessProfileViewSet(viewsets.ModelViewSet):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Only return profiles for the logged-in user"""
        return BusinessProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Auto-assign the logged-in user"""
        serializer.save(user=self.request.user)
