from django.contrib import admin
from .models import GreetingCategory, GreetingTemplate, Greeting, GreetingTemplateLike, GreetingTemplateDownload

# -----------------------------
# Greeting Category Admin
# -----------------------------
@admin.register(GreetingCategory)
class GreetingCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    # Optional: you can add ordering
    ordering = ('name',)


# -----------------------------
# GreetingTemplate Admin
# -----------------------------
class GreetingTemplateLikeInline(admin.TabularInline):
    model = GreetingTemplateLike
    extra = 0
    readonly_fields = ('user', 'liked_at')


class GreetingTemplateDownloadInline(admin.TabularInline):
    model = GreetingTemplateDownload
    extra = 0
    readonly_fields = ('user', 'downloaded_at')


@admin.register(GreetingTemplate)
class GreetingTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_by', 'created_at')
    list_filter = ('category', 'created_by')
    search_fields = ('title', 'created_by__email', 'created_by__username')
    readonly_fields = ('created_at',)
    inlines = [GreetingTemplateLikeInline, GreetingTemplateDownloadInline]


# -----------------------------
# Greeting Admin
# -----------------------------
@admin.register(Greeting)
class GreetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'template', 'created_at')
    list_filter = ('sender', 'template')
    search_fields = ('sender__email', 'template__title')
    readonly_fields = ('created_at',)


# -----------------------------
# GreetingTemplateLike Admin
# -----------------------------
@admin.register(GreetingTemplateLike)
class GreetingTemplateLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'template', 'liked_at')
    list_filter = ('user', 'template')
    search_fields = ('user__email', 'template__title')
    readonly_fields = ('liked_at',)


# -----------------------------
# GreetingTemplateDownload Admin
# -----------------------------
@admin.register(GreetingTemplateDownload)
class GreetingTemplateDownloadAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'template', 'downloaded_at')
    list_filter = ('user', 'template')
    search_fields = ('user__email', 'template__title')
    readonly_fields = ('downloaded_at',)
