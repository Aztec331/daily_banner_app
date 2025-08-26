from rest_framework import serializers

class GreetingsDataSerializer(serializers.Serializer):
    total_greetings_sent = serializers.IntegerField()
    total_templates_used = serializers.IntegerField()
    total_likes = serializers.IntegerField()
    total_downloads = serializers.IntegerField()

class BannersDataSerializer(serializers.Serializer):
    total_banners = serializers.IntegerField()
    active_banners = serializers.IntegerField()
    recently_created = serializers.IntegerField()

class TemplateUsageItemSerializer(serializers.Serializer):
    template_id = serializers.IntegerField()
    template_title = serializers.CharField()
    usage_count = serializers.IntegerField()

class SubscriptionsDataSerializer(serializers.Serializer):
    active_subscriptions = serializers.IntegerField()
    expired_subscriptions = serializers.IntegerField()

class MediaFilesDataSerializer(serializers.Serializer):
    total_files = serializers.IntegerField()
    total_size = serializers.IntegerField()

class UsersDataSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()

class DashboardSerializer(serializers.Serializer):
    greetings = GreetingsDataSerializer()
    banners = BannersDataSerializer()
    subscriptions = SubscriptionsDataSerializer()
    mediafiles = MediaFilesDataSerializer()
    users = UsersDataSerializer()

class RecentActivitySerializer(serializers.Serializer):
    user = serializers.CharField()
    action = serializers.CharField()
    template_or_banner = serializers.CharField()
    timestamp = serializers.DateTimeField()