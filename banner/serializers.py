from rest_framework import serializers
from .models import Template, Banner, Font


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'

#Template download info serializer 
class TemplateDownloadSerializer(serializers.ModelSerializer):
    downloads_count = serializers.SerializerMethodField()
    downloaded = serializers.SerializerMethodField()

    class Meta:
        model = Template
        fields = ['id', 'title', 'downloads_count', 'downloaded']

    def get_downloads_count(self, obj):
        return obj.downloads.count()

    def get_downloaded(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return obj.downloads.filter(user=user).exists()
        return False

#Banner serializer to get all banners according to model name/fields
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

#Banner serializer to create a banner according to our custom name/fields
class BannerCreateSerializer(serializers.ModelSerializer):
    templateId = serializers.PrimaryKeyRelatedField(
        queryset=Template.objects.all(), source='template', write_only=True
    )
    title = serializers.CharField(source='custom_name')
    customizations = serializers.DictField(child=serializers.CharField(), required=False)
    
    class Meta:
        model = Banner
        fields = ['templateId', 'title', 'description', 'customizations', 'language']

    def create(self, validated_data):
        user = self.context['request'].user
        customizations = validated_data.pop('customizations', {})

        banner = Banner.objects.create(
            user=user,
            template=validated_data['template'],
            custom_name=validated_data['custom_name'],
            description=validated_data.get('description', ''),
            text_content=customizations.get('text', ''),
            custom_image=customizations.get('image', ''),
            language=validated_data.get('language', 'en')
        )
        return banner

 

class FontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Font
        fields = ['id', 'name', 'category', 'language', 'url']