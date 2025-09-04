from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import BusinessProfile
from .serializers import BusinessProfileSerializer

class BusinessProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = BusinessProfile.objects.get_or_create(user=request.user)
        serializer = BusinessProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile, _ = BusinessProfile.objects.get_or_create(user=request.user)
        serializer = BusinessProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
