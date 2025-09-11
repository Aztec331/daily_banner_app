from django.contrib import admin
from django.utils.html import format_html
from .models import Banner, Template, Font
# ---------------- Banner Admin ----------------
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "custom_name", "status", "language", "image_preview", "created_at")
    list_filter = ("status", "language", "created_at")
    search_fields = ("custom_name", "description", "text_content")
    def image_preview(self, obj):
        if obj.custom_image:
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" width="150" height="auto" /></a>',
                obj.custom_image
            )
        return "No Image"
    image_preview.short_description = "Preview"
# ---------------- Template Admin ----------------
@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "description")
# ---------------- Font Admin ----------------
@admin.register(Font)
class FontAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "language", "url")
    list_filter = ("category", "language")
    search_fields = ("name",)