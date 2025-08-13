from django.urls import path
from .views import (
    PlanListView,
    SubscribeView,
    SubscriptionStatusView,
    SubscriptionHistoryView,
    CancelSubscriptionView,
    SubscriptionRenewCreateView,
    PaymentSuccessView
)

urlpatterns = [
    path('plans/', PlanListView.as_view(), name='plans-List'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('payment/success/',PaymentSuccessView.as_view(),name = 'payment-success'),
    path('status/', SubscriptionStatusView.as_view(), name='subscription-status'),
    path('history/', SubscriptionHistoryView.as_view(), name='subscription-history'),
    path('cancel/', CancelSubscriptionView.as_view(), name='cancel-subscription'),
    path('Renew/',SubscriptionRenewCreateView.as_view(),name="Subscription-renew"),
]
