from rest_framework import serializers
from .models import BusinessProfile

class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = '__all__'
        # If you want user to be set automatically:
        extra_kwargs = {
            'user': {'read_only': True}
        }
