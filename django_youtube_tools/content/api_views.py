"""
API views for content generation and management.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import AIContent
from .serializers import AIContentSerializer, ContentGenerateRequestSerializer
from .tasks import generate_content_task
import logging

logger = logging.getLogger(__name__)


class ContentGeneratorAPIView(APIView):
    """
    API endpoint for AI content generation.
    
    POST: Queue content generation task
    GET: Get user's content history
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Queue content generation task.
        
        Request body:
            - userInput (str): Video topic for content generation
        
        Returns:
            - task_id: Celery task ID
            - status: Task status
        """
        # Validate request data
        serializer = ContentGenerateRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_input = serializer.validated_data['userInput']
        
        # Queue Celery task
        try:
            task = generate_content_task.delay(
                user_input=user_input,
                user_email=request.user.email
            )
            
            logger.info(f'Content generation task queued: {task.id}')
            
            return Response({
                'success': True,
                'task_id': task.id,
                'status': 'processing',
                'message': 'Content generation started'
            }, status=status.HTTP_202_ACCEPTED)
            
        except Exception as e:
            logger.error(f'Failed to queue content task: {e}')
            return Response(
                {'success': False, 'error': 'Failed to queue content generation'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get(self, request):
        """
        Get user's content history.
        
        Returns:
            List of AI-generated content ordered by creation date (newest first)
        """
        try:
            contents = AIContent.objects.filter(user=request.user)
            serializer = AIContentSerializer(contents, many=True)
            
            logger.info(f'Retrieved {len(serializer.data)} content items for user {request.user.email}')
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f'Failed to retrieve content: {e}')
            return Response(
                {'success': False, 'error': 'Failed to retrieve content'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
