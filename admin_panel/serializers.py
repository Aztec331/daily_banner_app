from rest_framework import serializers
from .models import BannerTemplate,UploadedMedia
from subscription.models import UserSubscription
from accounts.serializers import CustomUserSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        request = self.context.get("request")
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            # always use your CustomUser here
            user_obj = User.objects.get(email=email)
            user = authenticate(request=request, username=user_obj.email, password=password)
        except User.DoesNotExist:
            user = None

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        attrs["user"] = user
        return attrs 

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

    