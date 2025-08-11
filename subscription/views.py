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
import razorpay
from django.conf import settings

class SubscriptionPlanListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = SubscriptionPlan.objects.all()
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return Response(serializer.data)

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID))

class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubscribeRequestSerializer(data=request.data)
        if serializer.is_valid():
            plan_id = serializer.validated_data['plan_id']
            try:
                plan = SubscriptionPlan.objects.get(id=plan_id)
                amount_paise = int(plan.price * 100)

                # Step 1: Create Razorpay order
                razorpay_order = razorpay_client.order.create({
                    "amount": amount_paise,
                    "currency": "INR",
                    "payment_capture": "1"
                })

                # Optional: Save order ID temporarily in your database
                # e.g., create a pending UserSubscription with order_id
                UserSubscription.objects.update_or_create(
                    user=request.user,
                    defaults={
                        'plan': plan,
                        'is_active': False,
                        'order_id': razorpay_order['id'],  # Add this field in model
                    }
                )

                return Response({
                    "order_id": razorpay_order['id'],
                    "amount": amount_paise,
                    "currency": "INR",
                    "plan_name": plan.name,
                    "key_id": settings.RAZORPAY_KEY_ID,
                    "callback_url": "/api/payment/success/"  # for frontend redirection
                }, status=status.HTTP_200_OK)

            except SubscriptionPlan.DoesNotExist:
                return Response({"error": "Plan not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentSuccessView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        order_id = request.data.get("order_id")
        payment_id = request.data.get("payment_id")
        #signature = request.data.get("signature")
        if not all([order_id, payment_id, signature]):
            return Response({"status": "error", "message": "Missing order_id or payment_id"}, status=400)
        # try:
        #     params_dict = {
        #         "razor"
        #     }
        try:
            subscription = UserSubscription.objects.get(user=request.user,razorpay_order_id=order_id)

            #Activate subscription
            start_date= timezone.now()
            end_date = start_date + timedelta(days = subscription.plan.duration_days)

            subscription.start_date = start_date
            subscription.end_date = end_date
            subscription.is_active = True
            subscription.razorpay_payment_id = payment_id
            subscription.save()

            SubscriptionHistory.objects.create(
                user = request.user,
                plan = subscription.plan,
                start_date = start_date,
                end_date = end_date,
                status = 'active',
                action = 'subscribed',
                timestamp = timezone.now()
            )
            payment_details = razorpay_client.payment.fetch(payment_id)
            payment_status = payment_details.get("status")  # could be 'captured', 'failed', 'pending', etc.

            if payment_status == "captured":
                return Response({"status": "success", "message": "Payment captured and subscription activated"})
            else:
                return Response({"status": "pending", "message": f"Payment status: {payment_status}"})

        except UserSubscription.DoesNotExist:
            return Response({"status": "error", "message": "Subscription not found for this order_id"}, status=404)

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)
        
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

class PlanListView(APIView):
    def get(self, request):
        plans = SubscriptionPlan.objects.prefetch_related('subplans').all()
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return Response(serializer.data)