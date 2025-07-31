from rest_framework import serializers
from .models import BannerTemplate,UploadedMedia
from subscription.models import UserSubscription
from accounts.serializers import CustomUserSerializer

class BannerTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerTemplate
        fields = '__all__'

class UploadedMediaSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    class Meta:
        model = UploadedMedia
        fields = ['id', 'uploaded_by', 'uploaded_by_username', 'media_file', 'uploaded_at']
        read_only_fields = ['id','uploaded_at', 'uploaded_by_username']

class SubscriptionSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserSubscription
        fields = ['id','user','username','email','subscription_type','start_date','end_date','status']

    