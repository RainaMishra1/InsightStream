"""
Celery tasks for thumbnail generation and processing.
"""
from celery import shared_task
from services.celery_tasks import AITaskWithRetry, ImageProcessingTask
from celery.utils.log import get_task_logger
from services.ai_service import get_ai_service
from services.imagekit_service import get_imagekit_service
from thumbnails.models import Thumbnail
from accounts.models import User
import time

logger = get_task_logger(__name__)


@shared_task(base=AITaskWithRetry, bind=True)
def generate_thumbnail_task(self, user_input, ref_image=None, user_email=None):
    """
    Generate AI thumbnail using Replicate or Pollinations.
    
    Args:
        user_input: User's text description for thumbnail
        ref_image: Optional reference image URL or base64 data
        user_email: User's email address
    
    Returns:
        dict: Generated thumbnail details with URL and success status
    """
    logger.info(f'Starting thumbnail generation for {user_email}')
    
    try:
        # Get services
        ai_service = get_ai_service()
        imagekit_service = get_imagekit_service()
        
        # Step 1: Generate thumbnail with AI
        image_blob = None
        
        if ref_image:
            # Try with reference image
            try:
                logger.info('Generating thumbnail with reference image')
                image_blob = ai_service.generate_thumbnail_with_replicate(
                    prompt=user_input,
                    ref_image=ref_image
                )
            except Exception as e:
                logger.warning(f'Reference image generation failed: {e}, trying without reference')
                # Fallback to text-only
                image_blob = None
        
        # If no reference image or reference failed, try text-only
        if image_blob is None:
            try:
                logger.info('Generating thumbnail with Replicate (text-only)')
                image_blob = ai_service.generate_thumbnail_with_replicate(
                    prompt=user_input,
                    ref_image=None
                )
            except Exception as e:
                logger.warning(f'Replicate generation failed: {e}, trying Pollinations fallback')
                # Fallback to Pollinations
                image_blob = ai_service.generate_thumbnail_with_pollinations(
                    prompt=user_input
                )
        
        if not image_blob:
            raise Exception('Failed to generate thumbnail with all AI services')
        
        # Step 2: Upload to ImageKit
        logger.info('Uploading thumbnail to ImageKit')
        filename = f'thumbnail_{int(time.time())}.png'
        thumbnail_url = imagekit_service.upload_image(
            file_buffer=image_blob,
            filename=filename,
            folder='/thumbnails'
        )
        
        # Step 3: Save to database with atomic transaction
        from django.db import transaction
        
        logger.info('Saving thumbnail to database')
        with transaction.atomic():
            user = User.objects.get(email=user_email)
            thumbnail = Thumbnail.objects.create(
                user=user,
                user_input=user_input,
                thumbnail_url=thumbnail_url,
                ref_image=ref_image if ref_image else None
            )
        
        logger.info(f'Thumbnail generation completed successfully: {thumbnail.id}')
        
        return {
            'success': True,
            'thumbnail_id': thumbnail.id,
            'thumbnail_url': thumbnail_url,
            'user_input': user_input,
            'message': 'Thumbnail generated successfully'
        }
        
    except Exception as e:
        logger.error(f'Thumbnail generation failed: {e}', exc_info=True)
        raise
