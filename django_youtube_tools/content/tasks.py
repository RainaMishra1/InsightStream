"""
Celery tasks for AI content generation.
"""
from celery import shared_task
from services.celery_tasks import AITaskWithRetry
from celery.utils.log import get_task_logger
from services.ai_service import get_ai_service
from content.models import AIContent
from accounts.models import User

logger = get_task_logger(__name__)


@shared_task(base=AITaskWithRetry, bind=True)
def generate_content_task(self, user_input, user_email):
    """
    Generate AI content (titles, description, tags) for YouTube videos.
    
    Args:
        user_input: User's video topic
        user_email: User's email address
    
    Returns:
        dict: Generated content with titles, description, and tags
    """
    logger.info(f'Starting content generation for {user_email}')
    
    try:
        # Get AI service
        ai_service = get_ai_service()
        
        # Generate content metadata
        logger.info(f'Generating content metadata for topic: {user_input}')
        content_data = ai_service.generate_content_metadata(user_input)
        
        # Validate content structure
        if not content_data or not isinstance(content_data, dict):
            raise Exception('Invalid content data returned from AI')
        
        # Ensure required fields exist
        if 'titles' not in content_data:
            content_data['titles'] = [
                {"title": f"{user_input} - Complete Guide", "seo_score": 85},
                {"title": f"How to {user_input}", "seo_score": 80},
                {"title": f"{user_input} Tutorial", "seo_score": 75}
            ]
        
        if 'description' not in content_data:
            content_data['description'] = f"Learn everything about {user_input} in this comprehensive guide."
        
        if 'tags' not in content_data:
            content_data['tags'] = ["tutorial", "guide", "howto", user_input.lower()]
        
        # Save to database with atomic transaction
        from django.db import transaction
        
        logger.info('Saving content to database')
        with transaction.atomic():
            user = User.objects.get(email=user_email)
            ai_content = AIContent.objects.create(
                user=user,
                user_input=user_input,
                content=content_data
            )
        
        logger.info(f'Content generation completed successfully: {ai_content.id}')
        
        return {
            'success': True,
            'content_id': ai_content.id,
            'content': content_data,
            'user_input': user_input,
            'message': 'Content generated successfully'
        }
        
    except Exception as e:
        logger.error(f'Content generation failed: {e}', exc_info=True)
        raise
