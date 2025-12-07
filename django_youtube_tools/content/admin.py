"""
Admin configuration for content app.
"""
from django.contrib import admin
from .models import AIContent


@admin.register(AIContent)
class AIContentAdmin(admin.ModelAdmin):
    """Admin interface for AIContent model."""
    
    list_display = ['id', 'user', 'user_input_preview', 'titles_count', 'tags_count', 'created_on']
    list_filter = ['created_on']
    search_fields = ['user__email', 'user_input']
    readonly_fields = ['created_on', 'content_preview']
    ordering = ['-created_on']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Content Details', {
            'fields': ('user_input', 'content', 'thumbnail_url')
        }),
        ('Preview', {
            'fields': ('content_preview',)
        }),
        ('Metadata', {
            'fields': ('created_on',)
        }),
    )
    
    def user_input_preview(self, obj):
        """Show truncated user input."""
        return obj.user_input[:50] + '...' if len(obj.user_input) > 50 else obj.user_input
    user_input_preview.short_description = 'Input'
    
    def titles_count(self, obj):
        """Show number of titles."""
        titles = obj.get_titles()
        return len(titles)
    titles_count.short_description = 'Titles'
    
    def tags_count(self, obj):
        """Show number of tags."""
        tags = obj.get_tags()
        return len(tags)
    tags_count.short_description = 'Tags'
    
    def content_preview(self, obj):
        """Show formatted content preview."""
        if not obj.content:
            return 'No content'
        
        preview = []
        titles = obj.get_titles()
        if titles:
            preview.append(f"Titles: {len(titles)}")
        
        description = obj.get_description()
        if description:
            preview.append(f"Description: {description[:100]}...")
        
        tags = obj.get_tags()
        if tags:
            preview.append(f"Tags: {', '.join(tags[:5])}")
        
        return '\n'.join(preview)
    content_preview.short_description = 'Content Preview'
