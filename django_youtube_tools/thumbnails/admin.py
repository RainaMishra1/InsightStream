"""
Admin configuration for thumbnails app.
"""
from django.contrib import admin
from .models import Thumbnail


@admin.register(Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    """Admin interface for Thumbnail model."""
    
    list_display = ['id', 'user', 'user_input_preview', 'thumbnail_url_preview', 'created_on']
    list_filter = ['created_on']
    search_fields = ['user__email', 'user_input']
    readonly_fields = ['created_on']
    ordering = ['-created_on']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Thumbnail Details', {
            'fields': ('user_input', 'thumbnail_url', 'ref_image')
        }),
        ('Metadata', {
            'fields': ('created_on',)
        }),
    )
    
    def user_input_preview(self, obj):
        """Show truncated user input."""
        return obj.user_input[:50] + '...' if len(obj.user_input) > 50 else obj.user_input
    user_input_preview.short_description = 'Input'
    
    def thumbnail_url_preview(self, obj):
        """Show truncated thumbnail URL."""
        return obj.thumbnail_url[:50] + '...' if len(obj.thumbnail_url) > 50 else obj.thumbnail_url
    thumbnail_url_preview.short_description = 'Thumbnail URL'
