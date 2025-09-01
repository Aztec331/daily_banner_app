from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Template, Banner, Font
from .serializers import TemplateSerializer, BannerSerializer, FontSerializer
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from django.conf import settings
import os

# ------------------ TEMPLATE VIEWS ------------------ #

class TemplateListView(generics.ListAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        category = self.request.query_params.get('category')
        base_queryset= Template.objects.all()
        if category:
            return base_queryset.filter(category=category)
        return base_queryset


class TemplateDetailView(generics.RetrieveAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.AllowAny]

class TemplateLanguagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # List of template languages
        languages = [
            {"code": "en", "name": "English"},
            {"code": "hi", "name": "Hindi"},
            {"code": "mr", "name": "Marathi"},
        ]
        return Response({"languages": languages})


# ------------------ BANNER VIEWS ------------------ #


class BannerUpdateView(generics.UpdateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Banner.objects.filter(user=self.request.user)


class MyBannersListView(generics.ListAPIView):
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Banner.objects.filter(user=self.request.user)


class BannerDetailView(generics.RetrieveAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAuthenticated]


class BannerDeleteView(generics.DestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Banner.objects.filter(user=self.request.user)

class BannerDownloadView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self, request, pk):
        try:
            banner = Banner.objects.get(pk=pk)
        except Banner.DoesNotExist:
            raise Http404("Banner not found")
        
        if not banner.banner_image:
            raise Http404("No file available for this banner")
        
        file_path = banner.banner_image.path
        file_name = os.path.basename(file_path)

        return FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=file_name
        )

#------------------Font Views-------------------------------#

class FontListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        category = request.query_params.get('category', 'all')
        language = request.query_params.get('language', 'all')

        fonts = Font.objects.all()
        if category != 'all':
            fonts = fonts.filter(category=category)
        if language != 'all':
            fonts = fonts.filter(language=language)

        serializer = FontSerializer(fonts, many=True)
        return Response(serializer.data)

class FontCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = [choice[0] for choice in Font.CATEGORY_CHOICES]
        return Response(categories)