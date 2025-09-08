# serializers.py
from rest_framework import serializers
from .models import Media

class MediaSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False
    )

    class Meta:
        model = Media
        fields = '__all__'
        read_only_fields = [
            'user', 'uploaded_at', 'size', 'file_name', 'file_type', 'file'
        ]
