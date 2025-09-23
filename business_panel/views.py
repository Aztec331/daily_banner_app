# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Business, BusinessUpload
from .serializers import BusinessSerializer, BusinessUploadSerializer
from django.shortcuts import render

# GET /user/businesses
class UserBusinessListView(generics.ListAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Business.objects.filter(user=self.request.user)

# POST /business
class BusinessCreateView(generics.CreateAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the logged-in user
        serializer.save(user=self.request.user)

# PUT /business/:id
class BusinessUpdateView(generics.UpdateAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow updating businesses owned by the logged-in user
        return Business.objects.filter(user=self.request.user)

# DELETE /business/:id
class BusinessDeleteView(generics.DestroyAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow deleting businesses owned by the logged-in user
        return Business.objects.filter(user=self.request.user)



class BusinessUploadView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            business = Business.objects.get(pk=pk, user=request.user)
        except Business.DoesNotExist:
            return Response({"detail": "Business not found."}, status=404)

        serializer = BusinessUploadSerializer(business, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": {
                    "url": serializer.data["logo"] or serializer.data["banner"],
                    "type": request.data.get("type"),
                },
                "message": "Image uploaded successfully"
            }, status=200)
        return Response(serializer.errors, status=400)