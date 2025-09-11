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
        read_only_fields = ['user', 'uploaded_at', 'size', 'file_name', 'file_type']

    def validate(self, data):
        # Optional: validate type if query param is passed
        file_type_param = self.context['request'].query_params.get('type', None)
        if file_type_param in ['image', 'video'] and 'file_type' in data and data['file_type'] != file_type_param:
            raise serializers.ValidationError(
                f"You selected type='{file_type_param}' but the file type is '{data['file_type']}'."
            )
        return data

class MediaUploadSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False
    )

    class Meta:
        model = Media
        fields = ['file', 'file_name', 'file_type', 'title', 'description', 'category', 'tags', 'size']
        read_only_fields = ['size', 'file_name', 'file_type']

    def create(self, validated_data):
        file = validated_data['file']
        validated_data['file_name'] = file.name
        validated_data['file_type'] = 'image' if file.content_type.startswith('image') else 'video'
        validated_data['size'] = file.size
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
