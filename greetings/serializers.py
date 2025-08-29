from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from .models import (
    GreetingCategory,
    GreetingTemplate,
    GreetingTemplateLike,
    GreetingTemplateDownload,
    Greeting
)


class GreetingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GreetingCategory
        fields = ['id', 'name', 'description']


class GreetingTemplateSerializer(serializers.ModelSerializer):
    category = GreetingCategorySerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    downloads_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_downloaded = serializers.SerializerMethodField()

    class Meta:
        model = GreetingTemplate
        fields = [
            'id', 'title', 'image', 'language', 'is_premium',
            'category', 'likes_count', 'downloads_count', 'is_liked',
            'created_at', 'updated_at','is_downloaded'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_downloads_count(self, obj):
        return obj.downloads.count()

    def get_is_liked(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False
    
    def get_is_downloaded(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return obj.downloads.filter(user=user).exists()
        return False


class GreetingTemplateLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GreetingTemplateLike
        fields = ['id', 'user', 'template', 'created_at','likes_count']


class GreetingTemplateDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = GreetingTemplateDownload
        fields = ['id', 'user', 'template', 'created_at']


class GreetingSerializer(serializers.ModelSerializer):
    template = GreetingTemplateSerializer(read_only=True)
    template_id = serializers.PrimaryKeyRelatedField(
        queryset=GreetingTemplate.objects.all(),
        source='template',
        write_only=True
    )

    class Meta:
        model = Greeting
        fields = [
            'id', 'template', 'template_id',
            'customizations', 'created_at'
        ]
