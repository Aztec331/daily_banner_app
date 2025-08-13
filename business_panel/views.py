# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Business
from .serializers import BusinessSerializer

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
from django.shortcuts import render

# Create your views here.
