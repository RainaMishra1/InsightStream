"""
API views for thumbnail generation and management.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Thumbnail
from .serializers import (
    ThumbnailSerializer,
    ThumbnailGenerateRequestSerializer,
    ThumbnailGenerateResponseSerializer
)
from .tasks import generate_thumbnail_task
import base64
import logging

logger = logging.getLogger(__name__)


class ThumbnailGenerateAPIView(APIView):
    """
    API endpoint for thumbnail generation.
    
    POST: Queue thumbnail generation task
    GET: Get user's thumbnail history
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Queue thumbnail generation task.
        
        Request body:
            - userInput (str): Text description for thumbnail
            - refImage (file, optional): Reference image
        
        Returns:
            - task_id: Celery task ID
            - status: Task status
        """
        # Validate request data
        serializer = ThumbnailGenerateRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_input = serializer.validated_data['userInput']
        ref_image_file = serializer.validated_data.get('refImage')
        
        # Process reference image if provided
        ref_image_data = None
        if ref_image_file:
            try:
                # Read file and convert to base64
                image_bytes = ref_image_file.read()
                ref_image_data = f"data:{ref_image_file.content_type};base64,{base64.b64encode(image_bytes).decode('utf-8')}"
                logger.info(f'Reference image provided: {ref_image_file.name}')
            except Exception as e:
                logger.error(f'Failed to process reference image: {e}')
                return Response(
                    {'success': False, 'error': 'Failed to process reference image'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Try Celery first, fallback to direct processing
        try:
            from django.conf import settings
            import redis
            
            # Check if Redis is available
            try:
                redis_client = redis.from_url(settings.CELERY_BROKER_URL, socket_connect_timeout=1)
                redis_client.ping()
                
                # Redis available, use Celery
                task = generate_thumbnail_task.delay(
                    user_input=user_input,
                    ref_image=ref_image_data,
                    user_email=request.user.email
                )
                logger.info(f'Thumbnail generation task queued: {task.id}')
                return Response({
                    'success': True,
                    'task_id': task.id,
                    'status': 'processing',
                    'message': 'Thumbnail generation started'
                }, status=status.HTTP_202_ACCEPTED)
                
            except:
                # Redis not available, return immediate response and process in background
                logger.warning('Redis not available, starting direct processing')
                
                # Import threading for background processing
                import threading
                
                # Create a simple task ID
                import uuid
                task_id = str(uuid.uuid4())
                
                # Process in background thread
                def process_thumbnail():
                    try:
                        generate_thumbnail_task(
                            user_input=user_input,
                            ref_image=ref_image_data,
                            user_email=request.user.email
                        )
                        logger.info(f'Background thumbnail generation completed: {task_id}')
                    except Exception as e:
                        logger.error(f'Background thumbnail generation failed: {e}')
                
                thread = threading.Thread(target=process_thumbnail)
                thread.daemon = True
                thread.start()
                
                return Response({
                    'success': True,
                    'task_id': task_id,
                    'status': 'processing',
                    'message': 'Thumbnail generation started (this may take 30-60 seconds)'
                }, status=status.HTTP_202_ACCEPTED)
            
        except Exception as e:
            logger.error(f'Failed to generate thumbnail: {e}')
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get(self, request):
        """
        Get user's thumbnail history.
        
        Returns:
            List of thumbnails ordered by creation date (newest first)
        """
        try:
            thumbnails = Thumbnail.objects.filter(user=request.user)
            serializer = ThumbnailSerializer(thumbnails, many=True)
            
            logger.info(f'Retrieved {len(serializer.data)} thumbnails for user {request.user.email}')
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f'Failed to retrieve thumbnails: {e}')
            return Response(
                {'success': False, 'error': 'Failed to retrieve thumbnails'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TaskStatusAPIView(APIView):
    """
    API endpoint to check Celery task status.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, task_id):
        """
        Get status of a Celery task.
        
        Args:
            task_id: Celery task ID
        
        Returns:
            - task_id: Task ID
            - status: Task status (PENDING, STARTED, SUCCESS, FAILURE)
            - result: Task result if completed
        """
        try:
            # Check if user has any new thumbnails (simple polling)
            recent_thumbnail = Thumbnail.objects.filter(user=request.user).order_by('-created_on').first()
            
            if recent_thumbnail:
                return Response({
                    'task_id': task_id,
                    'status': 'SUCCESS',
                    'result': ThumbnailSerializer(recent_thumbnail).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'task_id': task_id,
                    'status': 'PENDING'
                }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f'Failed to get task status: {e}')
            return Response(
                {'task_id': task_id, 'status': 'PENDING'},
                status=status.HTTP_200_OK
            )



class ThumbnailSearchAPIView(APIView):
    """
    API endpoint for thumbnail search.
    
    Supports two search modes:
    1. Text search: Search YouTube videos by keywords
    2. Similar thumbnail search: Extract tags from thumbnail and search
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Search YouTube thumbnails.
        
        Query parameters:
            - query (str, optional): Text search query
            - thumbnailUrl (str, optional): Thumbnail URL for similar search
        
        Returns:
            - For thumbnailUrl: {'tags': 'comma,separated,tags'}
            - For query: List of video objects with details
        """
        query = request.query_params.get('query')
        thumbnail_url = request.query_params.get('thumbnailUrl')
        
        # Mode 1: Extract tags from thumbnail URL
        if thumbnail_url:
            try:
                from services.ai_service import get_ai_service
                
                ai_service = get_ai_service()
                tags = ai_service.extract_tags_from_thumbnail(thumbnail_url)
                
                logger.info(f'Extracted tags from thumbnail: {tags}')
                
                return Response({
                    'tags': tags
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                logger.error(f'Failed to extract tags from thumbnail: {e}')
                return Response(
                    {'error': 'Failed to extract tags from thumbnail'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        # Mode 2: Search YouTube videos by query
        if query:
            try:
                from services.youtube_service import get_youtube_service
                
                youtube_service = get_youtube_service()
                videos = youtube_service.search_videos(query, max_results=20)
                
                logger.info(f'Found {len(videos)} videos for query: {query}')
                
                return Response(videos, status=status.HTTP_200_OK)
                
            except Exception as e:
                logger.error(f'YouTube search failed for query "{query}": {e}')
                return Response(
                    {'error': 'Failed to search YouTube videos'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        # No query parameters provided
        return Response(
            {'error': 'Query parameter required (query or thumbnailUrl)'},
            status=status.HTTP_400_BAD_REQUEST
        )
