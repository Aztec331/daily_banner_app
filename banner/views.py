from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Template, Banner
from .serializers import TemplateSerializer, BannerSerializer


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


# ------------------ BANNER VIEWS ------------------ #

class BannerCreateView(generics.CreateAPIView):
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
