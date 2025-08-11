from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription, SubscriptionHistory, SubscriptionStatus, SubscriptionRenew, SubPlan

class SubPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPlan
        fields = ['id','name','price','duration_in_days']

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    subplans = SubPlanSerializer(many=True, read_only=True)

    class Meta:
        model = SubscriptionPlan
        fields = ['id','name','subplans']

class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)

    class Meta:
        model = UserSubscription
        fields = '__all__'

class SubscribeRequestSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()

class SubscriptionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionStatus
        fields = '__all__'
class SubscriptionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionHistory
        fields = '__all__'

class SubscriptionRenewSerializer(serializers.ModelSerializer):
    class Meta:
        model= SubscriptionRenew
        fields = ['user_subscription']