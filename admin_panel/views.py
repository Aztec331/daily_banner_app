from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from accounts.models import CustomUser
from accounts.serializers import UserProfileSerializer
#from subscriptions.models import 
# Create your views here.
class AdminUserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    
    def get(self,request):
        users = CustomUser.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)