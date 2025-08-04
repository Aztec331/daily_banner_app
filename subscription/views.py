from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import SubscriptionPlan, UserSubscription, SubscriptionHistory, SubscriptionRenew
from .serializers import (
    SubscriptionPlanSerializer,
    UserSubscriptionSerializer,
    SubscribeRequestSerializer,
    SubscriptionHistorySerializer,
    SubscriptionRenewSerializer,
)
from django.utils import timezone
from datetime import timedelta

class SubscriptionPlanListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        plans = SubscriptionPlan.objects.all()
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return Response(serializer.data)

class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubscribeRequestSerializer(data=request.data)
        if serializer.is_valid():
            plan_id = serializer.validated_data['plan_id']
            try:
                plan = SubscriptionPlan.objects.get(id=plan_id)
                start_date = timezone.now()
                end_date = start_date + timedelta(days=plan.duration_days)
                subscription, created = UserSubscription.objects.update_or_create(
                    user=request.user,
                    defaults={
                        'plan': plan,
                        'start_date': start_date,
                        'end_date': end_date,
                        'is_active': True
                    }
                )
                
                SubscriptionHistory.objects.create(
                    user = request.user,
                    plan=plan,
                    start_date = start_date,
                    end_date = end_date,
                    status = 'active',
                    action = 'subscribed',
                    timestamp = timezone.now()
                )

                return Response({"message": "Subscription successful."}, status=status.HTTP_200_OK)
            except SubscriptionPlan.DoesNotExist:
                return Response({"error": "Plan not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

class SubscriptionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            subscription = UserSubscription.objects.get(user=request.user)
            serializer = UserSubscriptionSerializer(subscription)
            return Response({"status": "success", "subscription": serializer.data}, status=status.HTTP_200_OK)
        except UserSubscription.DoesNotExist:
            return Response({"status": "no_active_subscription"},status=status.HTTP_404_NOT_FOUND)
        
class SubscriptionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = SubscriptionHistory.objects.filter(user=request.user).order_by('-start_date')
        serializer = SubscriptionHistorySerializer(history, many=True)
        return Response({"history": serializer.data})
    #if not history.exists():
    #return Response({"message": "No subscription history found."}, status=status.HTTP_404_NOT_FOUND)

class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            subscription = UserSubscription.objects.get(user=request.user)
            subscription.status = 'cancelled'
            subscription.save()

            SubscriptionHistory.objects.create(
                user=request.user,
                plan=subscription.plan,
                start_date=subscription.start_date,
                end_date=subscription.end_date,
                status='cancelled',
                action='cancelled',
                timestamp=timezone.now()
            )
            
            return Response({"message": "Subscription cancelled."}, status=status.HTTP_200_OK)
        except UserSubscription.DoesNotExist:
            return Response({"error": "No active subscription found."}, status=status.HTTP_404_NOT_FOUND)
        

class SubscriptionRenewCreateView(generics.CreateAPIView):
    queryset = SubscriptionRenew.objects.all()
    serializer_class = SubscriptionRenewSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(renewed_by=self.request.user)