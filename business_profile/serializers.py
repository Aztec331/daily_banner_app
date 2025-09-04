from rest_framework import serializers
from .models import BusinessProfile

class BusinessProfileSerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(source='name')
    contactInfo = serializers.SerializerMethodField()
    socialMedia = serializers.JSONField(source='social_media')

    class Meta:
        model = BusinessProfile
        fields = ['companyName', 'description', 'logo', 'contactInfo', 'socialMedia']

    def get_contactInfo(self, obj):
        return {
            'email': obj.email,
            'phone': obj.phone,
            'website': obj.website
        }

    def update(self, instance, validated_data):
        contact_info = self.initial_data.get('contactInfo', {})
        instance.email = contact_info.get('email', instance.email)
        instance.phone = contact_info.get('phone', instance.phone)
        instance.website = contact_info.get('website', instance.website)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.social_media = validated_data.get('social_media', instance.social_media)
        instance.save()
        return instance
