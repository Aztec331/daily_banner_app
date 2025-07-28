from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields =['id', 'email', 'username', 'password', 'user_type'] 
        # extra_kwargs = {'password': {'write_only': True}}
        password = serializers.CharField()
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'name', 'profile_image', 'user_logo', 'user_photo', 'user_type']
        read_only_fields = ['id', 'email', 'username', 'user_type']  # 🔐 Locked fields
