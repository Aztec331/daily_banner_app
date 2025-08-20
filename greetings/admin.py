from django.contrib import admin
from .models import GreetingCategory, GreetingTemplate, Greeting, GreetingTemplateLike, GreetingTemplateDownload

@admin.register(GreetingCategory)
class GreetingCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')   # shows columns in admin list
    search_fields = ('name',)                      # allows search by category name

@admin.register(GreetingTemplate)
class GreetingTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_by', 'created_at')
    list_filter = ('category',)
    search_fields = ('title',)

@admin.register(Greeting)
class GreetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'template', 'created_at')

@admin.register(GreetingTemplateLike)
class GreetingTemplateLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'template')

@admin.register(GreetingTemplateDownload)
class GreetingTemplateDownloadAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'template', 'downloaded_at')
