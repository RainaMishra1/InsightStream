"""
AIContent model for AI-generated video metadata.
"""
from django.db import models
from django.conf import settings


class AIContent(models.Model):
    """
    Model to store AI-generated content (titles, descriptions, tags).
    Matches the Next.js AiContentTable schema.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_contents',
        help_text='User who generated this content'
    )
    user_input = models.CharField(
        max_length=500,
        help_text='User input topic for content generation'
    )
    content = models.JSONField(
        help_text='Generated content (titles, description, tags) in JSON format'
    )
    thumbnail_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text='Optional thumbnail URL'
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when content was generated'
    )
    
    class Meta:
        db_table = 'ai_content'
        verbose_name = 'AI Content'
        verbose_name_plural = 'AI Contents'
        ordering = ['-created_on']
        indexes = [
            models.Index(fields=['-created_on']),
            models.Index(fields=['user', '-created_on']),
        ]
    
    def __str__(self):
        return f"AI Content by {self.user.email} - {self.created_on.strftime('%Y-%m-%d %H:%M')}"
    
    def get_titles(self):
        """Extract titles from content JSON."""
        return self.content.get('titles', []) if self.content else []
    
    def get_description(self):
        """Extract description from content JSON."""
        return self.content.get('description', '') if self.content else ''
    
    def get_tags(self):
        """Extract tags from content JSON."""
        return self.content.get('tags', []) if self.content else []
