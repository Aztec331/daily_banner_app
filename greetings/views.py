from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions, filters
from django.shortcuts import get_object_or_404
from .models import (
    GreetingCategory,
    GreetingTemplate,
    Greeting,
    GreetingTemplateLike,
    GreetingTemplateDownload
)
from django.db.models import F
from .serializers import (
    GreetingCategorySerializer,
    GreetingTemplateSerializer,
    GreetingSerializer,
    GreetingTemplateLikeSerializer,
    GreetingTemplateDownloadSerializer
)


# 7.1 Get Greeting Categories
class GreetingCategoryListView(generics.ListAPIView):
    queryset = GreetingCategory.objects.all()
    serializer_class = GreetingCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


# 7.2 + 7.3 Get Greeting Templates (with filters)
class GreetingTemplateListView(generics.ListAPIView):
    serializer_class = GreetingTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = GreetingTemplate.objects.all()

        category = self.request.query_params.get('category')
        language = self.request.query_params.get('language')
        is_premium = self.request.query_params.get('isPremium')
        search = self.request.query_params.get('search')

        if category:
            queryset = queryset.filter(category__id=category)
        if language:
            queryset = queryset.filter(language__iexact=language)
        if is_premium in ['true', 'false']:
            queryset = queryset.filter(is_premium=(is_premium == 'true'))
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset


# 7.4 Search Greeting Templates (separate endpoint)
class GreetingTemplateSearchView(generics.ListAPIView):
    serializer_class = GreetingTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        q = self.request.query_params.get('q', '')
        return GreetingTemplate.objects.filter(title__icontains=q)


# 7.5 Like Greeting Template
class GreetingTemplateLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        template = get_object_or_404(GreetingTemplate, pk=pk)
        user = request.user

        like, created = GreetingTemplateLike.objects.get_or_create(user=user, template=template)

        if not created:
            # Already liked -> Unlike
            template.likes_count = F("likes_count") - 1  # decrement counter
            template.save(update_fields=["likes_count"])
            template.refresh_from_db()
            return Response({
                "message": "Unliked successfully",
                "likes_count": template.likes_count
            }, status=status.HTTP_200_OK)

        template.likes_count = F("likes_count") + 1
        template.likes_count = F("likes_count") + 1
        template.save(update_fields=["likes_count"])
        template.refresh_from_db()
        return Response({
            "message": "Liked successfully",
            "likes_count": template.likes_count
        }, status=status.HTTP_201_CREATED)


# 7.6 Download Greeting Template
class GreetingTemplateDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        template = get_object_or_404(GreetingTemplate, pk=pk)
        user = request.user

        download, created = GreetingTemplateDownload.objects.get_or_create(user=user, template=template)

        serializer = GreetingTemplateDownloadSerializer(download)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 7.7 Create Greeting
class GreetingCreateView(generics.CreateAPIView):
    serializer_class = GreetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
