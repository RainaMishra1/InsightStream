"""
AI Service for integrating with multiple AI providers.
Supports Gemini, Replicate, HuggingFace, and OpenRouter.
"""
import logging
import requests
from django.conf import settings
import google.generativeai as genai

logger = logging.getLogger(__name__)


class AIService:
    """
    Service class for AI operations.
    Handles thumbnail generation, keyword extraction, and content generation.
    """
    
    def __init__(self):
        """Initialize AI service with API keys from settings."""
        self.gemini_api_key = settings.GEMINI_API_KEY_1
        self.replicate_api_token = settings.REPLICATE_API_TOKEN
        self.hf_api_token = settings.HF_API_TOKEN
        self.openrouter_api_key = settings.OPENROUTER_API_KEY
        
        # Configure Gemini
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
    
    def generate_thumbnail_with_replicate(self, prompt, ref_image=None):
        """
        Generate thumbnail using Replicate FLUX model.
        
        Args:
            prompt: Text description for thumbnail
            ref_image: Optional reference image URL or base64 data
        
        Returns:
            bytes: Generated image data
        
        Raises:
            Exception: If generation fails
        """
        if not self.replicate_api_token:
            raise ValueError("Replicate API token not configured")
        
        try:
            import replicate
            
            client = replicate.Client(api_token=self.replicate_api_token)
            
            # Prepare input
            input_data = {
                "prompt": f"{prompt}, professional YouTube thumbnail, 16:9 aspect ratio, eye-catching, bold colors, dramatic lighting, vibrant design",
                "num_outputs": 1,
                "aspect_ratio": "16:9",
                "output_format": "png",
                "output_quality": 100,
            }
            
            # Add reference image if provided
            if ref_image:
                input_data["image"] = ref_image
                input_data["prompt_strength"] = 0.4
            
            # Run the model
            output = client.run(
                "black-forest-labs/flux-dev",
                input=input_data
            )
            
            # Download the generated image
            if output and len(output) > 0:
                image_url = output[0]
                response = requests.get(image_url, timeout=30)
                response.raise_for_status()
                
                logger.info(f"Successfully generated thumbnail with Replicate")
                return response.content
            else:
                raise Exception("No output from Replicate")
                
        except Exception as e:
            logger.error(f"Replicate thumbnail generation failed: {e}")
            raise
    
    def generate_thumbnail_with_pollinations(self, prompt):
        """
        Generate thumbnail using Pollinations AI (free fallback).
        
        Args:
            prompt: Text description for thumbnail
        
        Returns:
            bytes: Generated image data
        
        Raises:
            Exception: If generation fails
        """
        try:
            # Pollinations API endpoint
            url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"
            params = {
                "width": 1280,
                "height": 720,
                "model": "flux",
                "enhance": "true",
                "nologo": "true"
            }
            
            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            
            logger.info(f"Successfully generated thumbnail with Pollinations")
            return response.content
            
        except Exception as e:
            logger.error(f"Pollinations thumbnail generation failed: {e}")
            raise
    
    def generate_keywords_with_gemini(self, topic, youtube_data):
        """
        Generate keyword research using Gemini AI.
        
        Args:
            topic: User's topic for keyword research
            youtube_data: List of trending YouTube video titles
        
        Returns:
            dict: Structured keyword data with categories
        
        Raises:
            Exception: If generation fails
        """
        if not self.gemini_api_key:
            raise ValueError("Gemini API key not configured")
        
        try:
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            prompt = f"""Analyze this topic: "{topic}"

Based on these YouTube search trends: {', '.join(youtube_data)}

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
            
            response = model.generate_content(prompt)
            text = response.text
            
            # Extract JSON from response
            import json
            import re
            
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                keyword_data = json.loads(json_match.group(0))
                logger.info(f"Successfully generated keywords with Gemini")
                return keyword_data
            else:
                # Fallback data
                logger.warning("Could not parse Gemini response, using fallback")
                return {
                    "primary_keywords": [
                        {"keyword": topic, "search_volume": "medium", "competition": "medium", "relevance_score": 80}
                    ],
                    "long_tail_keywords": [],
                    "trending_keywords": [],
                    "related_topics": [],
                    "content_suggestions": []
                }
                
        except Exception as e:
            logger.error(f"Gemini keyword generation failed: {e}")
            raise
    
    def extract_tags_from_thumbnail(self, thumbnail_url):
        """
        Extract keywords from thumbnail using AI.
        
        Args:
            thumbnail_url: URL of the thumbnail image
        
        Returns:
            str: Comma-separated tags
        
        Raises:
            Exception: If extraction fails
        """
        if not self.openrouter_api_key:
            raise ValueError("OpenRouter API key not configured")
        
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [
                    {
                        "role": "user",
                        "content": f"""Describe this thumbnail in short keywords suitable for searching similar YouTube videos.
Give me tags comma-separated. Do not give any comment text. Maximum 5 tags.
Make sure after searching that tags will get similar YouTube thumbnails. Thumbnail URL: {thumbnail_url}"""
                    }
                ]
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            tags = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            
            logger.info(f"Successfully extracted tags from thumbnail")
            return tags
            
        except Exception as e:
            logger.error(f"Tag extraction failed: {e}")
            raise
    
    def generate_content_metadata(self, user_input):
        """
        Generate video titles, description, and tags using AI.
        
        Args:
            user_input: User's video topic
        
        Returns:
            dict: Generated content with titles, description, and tags
        
        Raises:
            Exception: If generation fails
        """
        if not self.openrouter_api_key:
            raise ValueError("OpenRouter API key not configured")
        
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json"
            }
            
            system_prompt = f"""You are an expert YouTube SEO strategist. Based on the user input: "{user_input}", generate JSON only:
{{
  "titles": [
    {{"title":"Title 1", "seo_score": 90}},
    {{"title":"Title 2", "seo_score": 85}},
    {{"title":"Title 3", "seo_score": 80}}
  ],
  "description": "A professional YouTube description here.",
  "tags": ["tag1","tag2","tag3","tag4","tag5","tag6","tag7","tag8","tag9","tag10"]
}}"""
            
            data = {
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [
                    {"role": "user", "content": system_prompt}
                ]
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            raw_json = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # Clean and parse JSON
            import json
            formatted_json = raw_json.replace('```json', '').replace('```', '').strip()
            
            if formatted_json:
                content_data = json.loads(formatted_json)
                logger.info(f"Successfully generated content metadata")
                return content_data
            else:
                # Fallback data
                logger.warning("Could not parse AI response, using fallback")
                return {
                    "titles": [
                        {"title": f"{user_input} - Complete Guide", "seo_score": 85},
                        {"title": f"How to {user_input}", "seo_score": 80},
                        {"title": f"{user_input} Tutorial", "seo_score": 75}
                    ],
                    "description": f"Learn everything about {user_input} in this comprehensive guide.",
                    "tags": ["tutorial", "guide", "howto", user_input.lower()]
                }
                
        except Exception as e:
            logger.error(f"Content metadata generation failed: {e}")
            raise


# Singleton instance
_ai_service_instance = None

def get_ai_service():
    """Get or create AI service singleton instance."""
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AIService()
    return _ai_service_instance
