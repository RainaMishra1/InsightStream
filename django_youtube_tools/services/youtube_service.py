"""
YouTube Service for interacting with YouTube Data API v3.
"""
import logging
import requests
from urllib.parse import urlencode
from django.conf import settings

logger = logging.getLogger(__name__)


class YouTubeService:
    """
    Service class for YouTube API operations.
    Handles video search, details fetching, and trending keywords.
    """
    
    def __init__(self):
        """Initialize YouTube service with API key from settings."""
        self.api_key = settings.YOUTUBE_API_KEY
        self.base_url = 'https://www.googleapis.com/youtube/v3'
    
    def search_videos(self, query, max_results=20):
        """
        Search YouTube videos by query.
        
        Args:
            query: Search query string
            max_results: Maximum number of results (default: 20)
        
        Returns:
            list: List of video objects with details
        
        Raises:
            ValueError: If API key not configured
            Exception: If API call fails
        """
        if not self.api_key:
            raise ValueError("YouTube API key not configured")
        
        try:
            # Step 1: Search for videos
            search_params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': max_results,
                'key': self.api_key
            }
            
            search_url = f"{self.base_url}/search?{urlencode(search_params)}"
            search_response = requests.get(search_url, timeout=30)
            search_response.raise_for_status()
            
            search_data = search_response.json()
            
            # Extract video IDs
            video_ids = [
                item['id']['videoId']
                for item in search_data.get('items', [])
                if item.get('id', {}).get('videoId')
            ]
            
            if not video_ids:
                logger.warning(f"No videos found for query: {query}")
                return []
            
            # Step 2: Get detailed video information
            return self.get_video_details(video_ids)
            
        except Exception as e:
            logger.error(f"YouTube search failed for query '{query}': {e}")
            raise
    
    def get_video_details(self, video_ids):
        """
        Get detailed video information including statistics.
        
        Args:
            video_ids: List of video IDs or comma-separated string
        
        Returns:
            list: List of video objects with full details
        
        Raises:
            ValueError: If API key not configured
            Exception: If API call fails
        """
        if not self.api_key:
            raise ValueError("YouTube API key not configured")
        
        try:
            # Convert list to comma-separated string if needed
            if isinstance(video_ids, list):
                video_ids = ','.join(video_ids)
            
            # Get video details
            details_params = {
                'part': 'snippet,statistics',
                'id': video_ids,
                'key': self.api_key
            }
            
            details_url = f"{self.base_url}/videos?{urlencode(details_params)}"
            details_response = requests.get(details_url, timeout=30)
            details_response.raise_for_status()
            
            details_data = details_response.json()
            
            # Format response
            videos = []
            for item in details_data.get('items', []):
                video = {
                    'id': item.get('id'),
                    'title': item.get('snippet', {}).get('title'),
                    'description': item.get('snippet', {}).get('description'),
                    'thumbnail': item.get('snippet', {}).get('thumbnails', {}).get('high', {}).get('url'),
                    'channelTitle': item.get('snippet', {}).get('channelTitle'),
                    'publishedAt': item.get('snippet', {}).get('publishedAt'),
                    'viewCount': item.get('statistics', {}).get('viewCount', 0),
                    'likeCount': item.get('statistics', {}).get('likeCount', 0),
                    'commentCount': item.get('statistics', {}).get('commentCount', 0),
                }
                videos.append(video)
            
            logger.info(f"Successfully fetched details for {len(videos)} videos")
            return videos
            
        except Exception as e:
            logger.error(f"YouTube video details fetch failed: {e}")
            raise
    
    def get_trending_keywords(self, topic, max_results=10):
        """
        Get trending video titles for a topic (used for keyword research).
        
        Args:
            topic: Topic to search for
            max_results: Maximum number of results (default: 10)
        
        Returns:
            list: List of video titles
        
        Raises:
            ValueError: If API key not configured
            Exception: If API call fails
        """
        if not self.api_key:
            logger.warning("YouTube API key not configured, returning topic as fallback")
            return [topic]
        
        try:
            # Search for trending videos (ordered by view count)
            search_params = {
                'part': 'snippet',
                'q': topic,
                'type': 'video',
                'maxResults': max_results,
                'order': 'viewCount',  # Most viewed = trending
                'key': self.api_key
            }
            
            search_url = f"{self.base_url}/search?{urlencode(search_params)}"
            response = requests.get(search_url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract video titles
            titles = [
                item.get('snippet', {}).get('title')
                for item in data.get('items', [])
                if item.get('snippet', {}).get('title')
            ]
            
            logger.info(f"Successfully fetched {len(titles)} trending titles for topic: {topic}")
            return titles[:max_results]
            
        except Exception as e:
            logger.error(f"YouTube trending keywords fetch failed: {e}")
            # Return topic as fallback
            return [topic]
    
    def get_channel_info(self, channel_id):
        """
        Get channel information.
        
        Args:
            channel_id: YouTube channel ID
        
        Returns:
            dict: Channel information
        
        Raises:
            ValueError: If API key not configured
            Exception: If API call fails
        """
        if not self.api_key:
            raise ValueError("YouTube API key not configured")
        
        try:
            params = {
                'part': 'snippet,statistics',
                'id': channel_id,
                'key': self.api_key
            }
            
            url = f"{self.base_url}/channels?{urlencode(params)}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('items'):
                item = data['items'][0]
                return {
                    'id': item.get('id'),
                    'title': item.get('snippet', {}).get('title'),
                    'description': item.get('snippet', {}).get('description'),
                    'thumbnail': item.get('snippet', {}).get('thumbnails', {}).get('high', {}).get('url'),
                    'subscriberCount': item.get('statistics', {}).get('subscriberCount', 0),
                    'videoCount': item.get('statistics', {}).get('videoCount', 0),
                    'viewCount': item.get('statistics', {}).get('viewCount', 0),
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"YouTube channel info fetch failed: {e}")
            raise


# Singleton instance
_youtube_service_instance = None

def get_youtube_service():
    """Get or create YouTube service singleton instance."""
    global _youtube_service_instance
    if _youtube_service_instance is None:
        _youtube_service_instance = YouTubeService()
    return _youtube_service_instance
