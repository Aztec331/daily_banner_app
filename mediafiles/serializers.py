from rest_framework import serializers
from .models import MediaAsset

class MediaAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAsset
        fields = ['id','user','file','media_type','uploaded_at']
        read_only_fields= ['id','user','uploaded_at']