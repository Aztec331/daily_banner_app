from django.contrib import admin
from .models import BusinessProfile


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'category', 'phone', 'is_verified', 'created_at')
    search_fields = ('name', 'category', 'phone', 'email')
    list_filter = ('is_verified', 'category', 'created_at')
    ordering = ('-created_at',)
