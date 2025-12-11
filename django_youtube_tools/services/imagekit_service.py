"""
ImageKit Service for cloud image storage and CDN.
"""
import logging
import base64
from django.conf import settings
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

logger = logging.getLogger(__name__)


class ImageKitService:
    """
    Service class for ImageKit operations.
    Handles image upload to ImageKit CDN.
    """
    
    def __init__(self):
        """Initialize ImageKit service with credentials from settings."""
        self.public_key = settings.IMAGEKIT_PUBLIC_KEY
        self.private_key = settings.IMAGEKIT_PRIVATE_KEY
        self.url_endpoint = settings.IMAGEKIT_URL_ENDPOINT
        
        if not all([self.public_key, self.private_key, self.url_endpoint]):
            logger.warning("ImageKit credentials not fully configured")
            self.imagekit = None
        else:
            self.imagekit = ImageKit(
                public_key=self.public_key,
                private_key=self.private_key,
                url_endpoint=self.url_endpoint
            )
    
    def upload_image(self, file_buffer, filename, folder='/thumbnails'):
        """
        Upload image to ImageKit and return URL.
        
        Args:
            file_buffer: Image data as bytes
            filename: Name for the uploaded file
            folder: ImageKit folder path (default: /thumbnails)
        
        Returns:
            str: URL of uploaded image
        
        Raises:
            ValueError: If ImageKit not configured
            Exception: If upload fails
        """
        if not self.imagekit:
            raise ValueError("ImageKit service not configured. Please set IMAGEKIT credentials in settings.")
        
        try:
            # Convert bytes to base64 string
            if isinstance(file_buffer, bytes):
                file_base64 = base64.b64encode(file_buffer).decode('utf-8')
            else:
                file_base64 = file_buffer
            
            # Upload to ImageKit
            result = self.imagekit.upload_file(
                file=file_base64,
                file_name=filename,
                options=UploadFileRequestOptions(
                    folder=folder,
                    use_unique_file_name=True
                )
            )
            
            if result and hasattr(result, 'url'):
                logger.info(f"Successfully uploaded image to ImageKit: {filename}")
                return result.url
            else:
                raise Exception("ImageKit upload returned no URL")
                
        except Exception as e:
            logger.error(f"ImageKit upload failed for {filename}: {e}")
            raise
    
    def upload_from_url(self, image_url, filename, folder='/thumbnails'):
        """
        Upload image from URL to ImageKit.
        
        Args:
            image_url: URL of the image to upload
            filename: Name for the uploaded file
            folder: ImageKit folder path
        
        Returns:
            str: URL of uploaded image
        
        Raises:
            Exception: If upload fails
        """
        if not self.imagekit:
            raise ValueError("ImageKit service not configured")
        
        try:
            import requests
            
            # Download image from URL
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Upload to ImageKit
            return self.upload_image(response.content, filename, folder)
            
        except Exception as e:
            logger.error(f"ImageKit upload from URL failed: {e}")
            raise
    
    def delete_file(self, file_id):
        """
        Delete file from ImageKit.
        
        Args:
            file_id: ImageKit file ID
        
        Returns:
            bool: True if deletion successful
        
        Raises:
            Exception: If deletion fails
        """
        if not self.imagekit:
            raise ValueError("ImageKit service not configured")
        
        try:
            result = self.imagekit.delete_file(file_id)
            logger.info(f"Successfully deleted file from ImageKit: {file_id}")
            return True
            
        except Exception as e:
            logger.error(f"ImageKit file deletion failed: {e}")
            raise
    
    def get_file_details(self, file_id):
        """
        Get file details from ImageKit.
        
        Args:
            file_id: ImageKit file ID
        
        Returns:
            dict: File details
        
        Raises:
            Exception: If retrieval fails
        """
        if not self.imagekit:
            raise ValueError("ImageKit service not configured")
        
        try:
            result = self.imagekit.get_file_details(file_id)
            return result
            
        except Exception as e:
            logger.error(f"ImageKit file details retrieval failed: {e}")
            raise


# Singleton instance
_imagekit_service_instance = None

def get_imagekit_service():
    """Get or create ImageKit service singleton instance."""
    global _imagekit_service_instance
    if _imagekit_service_instance is None:
        _imagekit_service_instance = ImageKitService()
    return _imagekit_service_instance
