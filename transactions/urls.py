from django.urls import path
from .views import TransactionViewSet

transaction_list = TransactionViewSet.as_view({'get': 'list'})
transaction_detail = TransactionViewSet.as_view({'get': 'retrieve'})
transaction_receipt = TransactionViewSet.as_view({'get': 'receipt'})

urlpatterns = [
    path('transactions/', transaction_list, name='transaction-list'),
    path('transactions/<int:pk>/', transaction_detail, name='transaction-detail'),
    path('transactions/<int:pk>/receipt/', transaction_receipt, name='transaction-receipt'),
]
