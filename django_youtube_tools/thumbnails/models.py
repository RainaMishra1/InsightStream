"""
Thumbnail model for AI-generated thumbnails.
"""
from django.db import models
from django.conf import settings


class Thumbnail(models.Model):
    """
    Model to store AI-generated thumbnails.
    Matches the Next.js AiThumbnailTable schema.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='thumbnails',
        help_text='User who generated this thumbnail'
    )
    user_input = models.CharField(
        max_length=500,
        help_text='User input text/description for thumbnail generation'
    )
    thumbnail_url = models.URLField(
        max_length=1000,
        help_text='ImageKit URL of the generated thumbnail'
    )
    ref_image = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text='Reference image URL if provided'
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when thumbnail was generated'
    )
    
    class Meta:
        db_table = 'thumbnails'
        verbose_name = 'Thumbnail'
        verbose_name_plural = 'Thumbnails'
        ordering = ['-created_on']
        indexes = [
            models.Index(fields=['-created_on']),
            models.Index(fields=['user', '-created_on']),
        ]
    
    def __str__(self):
        return f"Thumbnail by {self.user.email} - {self.created_on.strftime('%Y-%m-%d %H:%M')}"
