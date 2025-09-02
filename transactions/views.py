from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # GET /api/transactions/{id}/receipt/
    @action(detail=True, methods=["get"], url_path="receipt")
    def receipt(self, request, pk=None):
        transaction = self.get_object()
        receipt_data = {
            "transaction_id": transaction.id,
            "payment_id": transaction.payment_id,
            "order_id": transaction.order_id,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "status": transaction.status,
            "plan": transaction.plan,
            "plan_name": transaction.plan_name,
            "description": transaction.description,
            "method": transaction.method,
            "metadata": transaction.metadata,
            "user": transaction.user.username,
            "receipt_message": "Payment received successfully ✅"
        }
        return Response(receipt_data, status=status.HTTP_200_OK)
