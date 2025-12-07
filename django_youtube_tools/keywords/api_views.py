"""
API views for keyword research.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from services.youtube_service import get_youtube_service
from services.ai_service import get_ai_service
from services.gemini_rotation import get_next_gemini_key
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)


class KeywordResearchAPIView(APIView):
    """
    API endpoint for keyword research.
    
    POST: Generate keyword research for a topic
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Generate keyword research for a topic.
        
        Request body:
            - topic (str): Topic for keyword research
        
        Returns:
            - success: Boolean
            - data: Keyword research data with categories
            - topic: Original topic
        """
        topic = request.data.get('topic')
        
        if not topic or not topic.strip():
            return Response(
                {'success': False, 'error': 'Topic is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        topic = topic.strip()
        
        try:
            # Step 1: Get YouTube trending keywords
            logger.info(f'Fetching YouTube trending data for topic: {topic}')
            youtube_service = get_youtube_service()
            youtube_keywords = youtube_service.get_trending_keywords(topic, max_results=10)
            
            # Step 2: Generate keywords with AI
            logger.info(f'Generating keyword research with AI for topic: {topic}')
            
            # Get next Gemini API key (rotation)
            api_key = get_next_gemini_key()
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            # Create prompt
            prompt = f"""Analyze this topic: "{topic}"

Based on these YouTube search trends: {', '.join(youtube_keywords)}

Generate a comprehensive keyword research report in JSON format:
{{
  "primary_keywords": [
    {{"keyword": "main keyword 1", "search_volume": "high/medium/low", "competition": "high/medium/low", "relevance_score": 95}}
  ],
  "long_tail_keywords": [
    {{"keyword": "specific long tail keyword", "search_volume": "medium", "competition": "low", "relevance_score": 90}}
  ],
  "trending_keywords": [
    {{"keyword": "trending keyword", "trend": "rising/stable", "relevance_score": 85}}
  ],
  "related_topics": ["topic1", "topic2", "topic3"],
  "content_suggestions": ["suggestion 1", "suggestion 2"]
}}

Provide 5-7 keywords in each category. Focus on YouTube SEO."""
            
            # Generate with AI
            response = model.generate_content(prompt)
            text = response.text
            
            # Extract JSON from response
            import json
            import re
            
            json_match = re.search(r'\{[\s\S]*\}', text)
            
            if json_match:
                keyword_data = json.loads(json_match.group(0))
                logger.info(f'Successfully generated keyword research for topic: {topic}')
            else:
                # Fallback data
                logger.warning('Could not parse AI response, using fallback data')
                keyword_data = {
                    "primary_keywords": [
                        {
                            "keyword": topic,
                            "search_volume": "medium",
                            "competition": "medium",
                            "relevance_score": 80
                        }
                    ],
                    "long_tail_keywords": [],
                    "trending_keywords": [],
                    "related_topics": [],
                    "content_suggestions": []
                }
            
            return Response({
                'success': True,
                'data': keyword_data,
                'topic': topic
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f'Keyword research failed for topic "{topic}": {e}', exc_info=True)
            return Response(
                {'success': False, 'error': 'Failed to generate keyword research'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
