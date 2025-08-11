from django.contrib import admin
from rest_framework.authtoken.models import Token
from .models import CustomUser

# Unregister Token if already registered (safe cleanup)
try:
    admin.site.unregister(Token)
except admin.sites.NotRegistered:
    pass

# Register your CustomUser model
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active', 'is_staff')  # Customize as per your model
    search_fields = ('email',)
    list_filter = ('is_active', 'is_staff')


# Register Token with a custom admin
@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ("key", "user", "created")
    search_fields = ("user__email", "key")
    actions = ["delete_selected"]
