from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from subscription.models import UserSubscription
from subscription.serializers import UserSubscriptionSerializer
from .models import BannerTemplate, UploadedMedia
from .serializers import BannerTemplateSerializer, UploadedMediaSerializer, AdminLoginSerializer



class AdminLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Ensure only admin/staff can login here
            if not user.is_staff and not user.is_superuser:
                return Response({"detail": "Not authorized as admin."}, status=status.HTTP_403_FORBIDDEN)

            token, _ = Token.objects.get_or_create(user=user)
            user_data = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "token": token.key,
            }

            return Response(user_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Admin user list with optional status filter
class AdminUserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = CustomUser.objects.all()
        status_filter = request.query_params.get('status')
        if status_filter == 'active':
            users = users.filter(is_active=True)
        elif status_filter == 'expired':
            users = users.filter(subscription__status='expired')
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

# Admin user detail view
class AdminUserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        user.is_active = request.data.get('is_active', user.is_active)
        user.save()
        return Response({'detail': 'User status updated'})

# List all subscriptions
class AdminSubscriptionListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        subscriptions = UserSubscription.objects.select_related('user').all()
        serializer = UserSubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

# Create a new banner template
class TemplateCreateView(generics.CreateAPIView):
    queryset = BannerTemplate.objects.all()
    serializer_class = BannerTemplateSerializer
    permission_classes = [IsAdminUser]

# Update or delete existing banner template
class TemplateUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BannerTemplate.objects.all()
    serializer_class = BannerTemplateSerializer
    permission_classes = [IsAdminUser]

# List all uploaded media
class AdminMediaListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        media = UploadedMedia.objects.all()
        serializer = UploadedMediaSerializer(media, many=True)
        return Response(serializer.data)


class SubscribedUsersListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        user_ids = UserSubscription.objects.filter(is_active=True).values_list('user_id', flat=True).distinct()
        users = CustomUser.objects.filter(id__in=user_ids)

        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)