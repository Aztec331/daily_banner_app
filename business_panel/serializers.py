from rest_framework import serializers
from .models import Business, BusinessUpload

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
            'id', 'user', 'name', 'tagline', 'logo', 'phone', 'email', 
            'address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_phone(self, value):
        import re
        pattern = r'^\+91\d{10}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Phone number must start with +91 and be followed by exactly 10 digits.")
        return value
    
    def create(self, validated_data):
        # Ensure email can be set only at creation
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Prevent email from being updated
        validated_data.pop('email', None)
        return super().update(instance, validated_data)

class BusinessUploadSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=["logo", "banner"], write_only=True)
    file = serializers.ImageField(write_only=True)

    class Meta:
        model = Business   # ✅ point to Business, not BusinessUpload
        fields = ["id", "file", "type", "logo", "banner"]

    def update(self, instance, validated_data):
        upload_type = validated_data.pop("type")
        file = validated_data.pop("file")

        if upload_type == "logo":
            instance.logo = file
        elif upload_type == "banner":
            instance.banner = file
        instance.save()
        return instance
