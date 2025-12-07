"""
Serializers for thumbnail API.
"""
from rest_framework import serializers
from .models import Thumbnail


class ThumbnailSerializer(serializers.ModelSerializer):
    """Serializer for Thumbnail model."""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Thumbnail
        fields = [
            'id',
            'user_email',
            'user_input',
            'thumbnail_url',
            'ref_image',
            'created_on'
        ]
        read_only_fields = ['id', 'user_email', 'created_on']


class ThumbnailGenerateRequestSerializer(serializers.Serializer):
    """Serializer for thumbnail generation request."""
    
    userInput = serializers.CharField(
        max_length=500,
        required=True,
        help_text='Text description for thumbnail generation'
    )
    refImage = serializers.FileField(
        required=False,
        allow_null=True,
        help_text='Optional reference image'
    )
    
    def validate_userInput(self, value):
        """Validate user input is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError('User input cannot be empty')
        return value.strip()


class ThumbnailGenerateResponseSerializer(serializers.Serializer):
    """Serializer for thumbnail generation response."""
    
    success = serializers.BooleanField()
    task_id = serializers.CharField()
    status = serializers.CharField()
    message = serializers.CharField(required=False)
