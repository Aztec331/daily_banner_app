from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import generics, permissions
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Template, Banner, Font
from .serializers import TemplateSerializer, BannerSerializer, FontSerializer, BannerCreateSerializer, BannerUpdateSerializer
from .pagination import BannerPagination
from rest_framework.views import APIView
import io
import requests
from PIL import Image, ImageDraw
from django.http import HttpResponse, Http404

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

class BannerCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BannerCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            banner = serializer.save()
            return Response({
                "message": "Banner created successfully",
                "bannerId": banner.id,
                "templateId": banner.template.id,
                "title": banner.custom_name,
                "text_content": banner.text_content,
                "custom_image": banner.custom_image,
                "language": banner.language
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Get all banners of a user with pagination
class UserBannersView(ListAPIView):
    serializer_class = BannerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BannerPagination

    def get_queryset(self):
        user = self.request.user
        status_param = self.request.query_params.get('status', 'all')

        queryset = Banner.objects.filter(user=user)

        if status_param != 'all':
            queryset = queryset.filter(status=status_param)

        return queryset.order_by('-created_at')

class BannerDetailView(generics.RetrieveDestroyAPIView):
    """
    Handles:
    - GET    /api/banners/{id}/     → Get banner details by id
    - DELETE /api/banners/{id}/     → Delete banner by id
    """
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        # Only allow banners of the logged-in user
        return Banner.objects.filter(user=self.request.user)

class BannerUpdateView(generics.UpdateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # User can update only their own banners
        return Banner.objects.filter(user=self.request.user)

class PublishBannerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            banner = Banner.objects.get(id=id, user=request.user)
        except Banner.DoesNotExist:
            return Response({"detail": "Banner not found."}, status=status.HTTP_404_NOT_FOUND)

        if banner.status == 'published':
            return Response({"detail": "Banner is already published."}, status=status.HTTP_400_BAD_REQUEST)

        banner.status = 'published'
        banner.save()

        return Response({
            "id": banner.id,
            "custom_name": banner.custom_name,
            "status": banner.status,
            "message": "Banner has been published successfully."
        }, status=status.HTTP_200_OK)

class ArchiveBannerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            banner = Banner.objects.get(id=id, user=request.user)
        except Banner.DoesNotExist:
            return Response({"detail": "Banner not found."}, status=status.HTTP_404_NOT_FOUND)

        if banner.status == 'archived':
            return Response({"detail": "Banner is already archived."}, status=status.HTTP_400_BAD_REQUEST)

        banner.status = 'archived'
        banner.save()

        return Response({
            "id": banner.id,
            "custom_name": banner.custom_name,
            "status": banner.status,
            "message": "Banner has been archived successfully."
        }, status=status.HTTP_200_OK)


class ExportBannerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        quality = int(request.query_params.get("quality", 90))

        try:
            banner = Banner.objects.get(id=id)
        except Banner.DoesNotExist:
            return Response({"detail": "Banner not found."}, status=status.HTTP_404_NOT_FOUND)

        # Default white canvas
        img = Image.new("RGB", (800, 400), color=(255, 255, 255))

        # If banner has an image URL, fetch it
        if banner.custom_image:
            try:
                r = requests.get(banner.custom_image, stream=True, timeout=5)
                if r.status_code == 200:
                    img = Image.open(io.BytesIO(r.content)).convert("RGB")
            except Exception:
                pass  # fallback to white canvas if URL fails

        # Draw banner text
        draw = ImageDraw.Draw(img)
        text = banner.text_content or banner.custom_name
        draw.text((50, 50), text, fill=(0, 0, 0))

        # Save as PNG
        buffer = io.BytesIO()
        img.save(buffer, format="PNG", quality=quality)
        buffer.seek(0)

        response = HttpResponse(buffer, content_type="image/png")
        response["Content-Disposition"] = f'attachment; filename="banner_{banner.id}.png"'
        return response


 




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



