from django.urls import path
from .views import (
    SubscriptionPlanListView,
    SubscribeView,
    SubscriptionStatusView,
    SubscriptionHistoryView,
    CancelSubscriptionView
)

urlpatterns = [
    path('plans/', SubscriptionPlanListView.as_view(), name='subscription-plans'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('status/', SubscriptionStatusView.as_view(), name='subscription-status'),
    path('history/', SubscriptionHistoryView.as_view(), name='subscription-history'),
    path('cancel/', CancelSubscriptionView.as_view(), name='cancel-subscription'),
]
