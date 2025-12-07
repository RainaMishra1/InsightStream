"""
Gemini API Key Rotation Utility.
Rotates between multiple API keys to avoid rate limits.
"""
import logging
from django.conf import settings
import threading

logger = logging.getLogger(__name__)


class GeminiKeyRotation:
    """
    Manages rotation of multiple Gemini API keys.
    Thread-safe implementation for concurrent requests.
    """
    
    def __init__(self):
        """Initialize key rotation with keys from settings."""
        self.keys = []
        
        # Collect all configured Gemini API keys
        if settings.GEMINI_API_KEY_1:
            self.keys.append(settings.GEMINI_API_KEY_1)
        if settings.GEMINI_API_KEY_2:
            self.keys.append(settings.GEMINI_API_KEY_2)
        if settings.GEMINI_API_KEY_3:
            self.keys.append(settings.GEMINI_API_KEY_3)
        
        if not self.keys:
            logger.warning("No Gemini API keys configured")
        else:
            logger.info(f"Initialized Gemini key rotation with {len(self.keys)} keys")
        
        self.current_index = 0
        self.lock = threading.Lock()
        self.usage_count = {i: 0 for i in range(len(self.keys))}
    
    def get_next_key(self):
        """
        Get the next API key in rotation.
        Thread-safe round-robin selection.
        
        Returns:
            str: Next API key
        
        Raises:
            ValueError: If no keys configured
        """
        if not self.keys:
            raise ValueError("No Gemini API keys configured")
        
        with self.lock:
            # Get current key
            key = self.keys[self.current_index]
            
            # Track usage
            self.usage_count[self.current_index] += 1
            
            # Move to next key for next request
            self.current_index = (self.current_index + 1) % len(self.keys)
            
            logger.debug(f"Selected Gemini key #{self.current_index} (used {self.usage_count[self.current_index]} times)")
            
            return key
    
    def get_key_by_index(self, index):
        """
        Get a specific key by index.
        
        Args:
            index: Key index (0-based)
        
        Returns:
            str: API key at index
        
        Raises:
            IndexError: If index out of range
        """
        if not self.keys:
            raise ValueError("No Gemini API keys configured")
        
        if index < 0 or index >= len(self.keys):
            raise IndexError(f"Key index {index} out of range (0-{len(self.keys)-1})")
        
        return self.keys[index]
    
    def get_usage_stats(self):
        """
        Get usage statistics for all keys.
        
        Returns:
            dict: Usage count for each key
        """
        with self.lock:
            return dict(self.usage_count)
    
    def reset_usage_stats(self):
        """Reset usage statistics."""
        with self.lock:
            self.usage_count = {i: 0 for i in range(len(self.keys))}
            logger.info("Reset Gemini key usage statistics")
    
    def get_total_keys(self):
        """
        Get total number of configured keys.
        
        Returns:
            int: Number of keys
        """
        return len(self.keys)
    
    def is_configured(self):
        """
        Check if at least one key is configured.
        
        Returns:
            bool: True if keys available
        """
        return len(self.keys) > 0


# Singleton instance
_gemini_rotation_instance = None
_instance_lock = threading.Lock()


def get_gemini_rotation():
    """
    Get or create Gemini key rotation singleton instance.
    Thread-safe singleton pattern.
    
    Returns:
        GeminiKeyRotation: Singleton instance
    """
    global _gemini_rotation_instance
    
    if _gemini_rotation_instance is None:
        with _instance_lock:
            # Double-check locking pattern
            if _gemini_rotation_instance is None:
                _gemini_rotation_instance = GeminiKeyRotation()
    
    return _gemini_rotation_instance


def get_next_gemini_key():
    """
    Convenience function to get next Gemini API key.
    
    Returns:
        str: Next API key in rotation
    """
    rotation = get_gemini_rotation()
    return rotation.get_next_key()


def get_gemini_usage_stats():
    """
    Convenience function to get usage statistics.
    
    Returns:
        dict: Usage statistics
    """
    rotation = get_gemini_rotation()
    return rotation.get_usage_stats()
