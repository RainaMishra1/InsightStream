"""
Serializers for content API.
"""
from rest_framework import serializers
from .models import AIContent


class AIContentSerializer(serializers.ModelSerializer):
    """Serializer for AIContent model."""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    titles = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    
    class Meta:
        model = AIContent
        fields = [
            'id',
            'user_email',
            'user_input',
            'content',
            'titles',
            'description',
            'tags',
            'created_on'
        ]
        read_only_fields = ['id', 'user_email', 'created_on']
    
    def get_titles(self, obj):
        """Extract titles from content JSON."""
        return obj.get_titles()
    
    def get_description(self, obj):
        """Extract description from content JSON."""
        return obj.get_description()
    
    def get_tags(self, obj):
        """Extract tags from content JSON."""
        return obj.get_tags()


class ContentGenerateRequestSerializer(serializers.Serializer):
    """Serializer for content generation request."""
    
    userInput = serializers.CharField(
        max_length=500,
        required=True,
        help_text='Video topic for content generation'
    )
    
    def validate_userInput(self, value):
        """Validate user input is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError('User input cannot be empty')
        return value.strip()
