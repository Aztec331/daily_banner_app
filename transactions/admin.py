from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'payment_id',
        'order_id',
        'amount',
        'currency',
        'status',
        'plan_name',
        'method',
    )
    list_filter = ('status', 'currency', 'plan_name', 'method')
    search_fields = ('payment_id', 'order_id', 'user__username', 'plan_name')
    ordering = ('id',)  # or any other field that exists
