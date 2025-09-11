from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Media
from .serializers import MediaSerializer, MediaUploadSerializer
from .pagination import MediaPagination
from django.db.models import Q
from rest_framework.views import APIView
from django.db.models import Count, Sum

#Get all media with pagination
class MediaListView(generics.ListAPIView):
    serializer_class = MediaSerializer
    pagination_class = MediaPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        media_type = self.request.query_params.get("type")

        queryset = Media.objects.filter(user=user)

        if media_type in ["image", "video"]:
            queryset = queryset.filter(file_type=media_type)

        return queryset.order_by("-uploaded_at")

#Upload media
class MediaUploadView(generics.CreateAPIView):
    serializer_class = MediaUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

#Retrieve and delete media by id
class MediaRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You cannot access or delete this media.")
        return obj

#get all media by type image/video
class MediaByTypeView(generics.ListAPIView):
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        media_type = self.kwargs.get("type")
        if media_type not in ["image", "video"]:
            raise ValidationError({"error": "Invalid type. Allowed values: 'image', 'video'."})

        return Media.objects.filter(user=self.request.user, file_type=media_type)

#get user's media filtered through searched tags
class MediaSearchView(generics.ListAPIView):
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MediaPagination

    def get_queryset(self):
        user = self.request.user
        tags_param = self.request.query_params.get('tags', None)

        # Start with all media for this user
        queryset = Media.objects.filter(user=user)

        if tags_param:
            # Split query tags, strip spaces
            search_tags = [tag.strip() for tag in tags_param.split(',') if tag.strip()]

            # Build OR query for case-insensitive search
            q_objects = Q()
            for tag in search_tags:
                q_objects |= Q(tags__icontains=tag)  # icontains is case-insensitive

            queryset = queryset.filter(q_objects)

        return queryset.order_by('-uploaded_at')

#get media statistics of logged in user
class MediaStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Base queryset → only this user's media
        queryset = Media.objects.filter(user=user)

        # Total count
        total_files = queryset.count()

        # Count by file_type
        file_type_counts = queryset.values('file_type').annotate(count=Count('id'))

        # Count by category
        category_counts = queryset.values('category').annotate(count=Count('id'))

        # Total size
        total_size = queryset.aggregate(total=Sum('size'))['total'] or 0

        return Response({
            "total_files": total_files,
            "by_file_type": {item['file_type']: item['count'] for item in file_type_counts},
            "by_category": {item['category']: item['count'] for item in category_counts},
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        })
    