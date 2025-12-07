"""
API URL configuration for Django YouTube Tools project.
"""
from django.urls import path
from thumbnails import api_views as thumbnail_api
from content import api_views as content_api
from keywords import api_views as keyword_api

urlpatterns = [
    # Thumbnail API endpoints
    path('generate-thumbnail', thumbnail_api.ThumbnailGenerateAPIView.as_view(), name='generate-thumbnail'),
    path('task-status/<str:task_id>', thumbnail_api.TaskStatusAPIView.as_view(), name='task-status'),
    path('thumbnail-search', thumbnail_api.ThumbnailSearchAPIView.as_view(), name='thumbnail-search'),
    
    # Content API endpoints
    path('ai-content-generator', content_api.ContentGeneratorAPIView.as_view(), name='ai-content-generator'),
    
    # Keyword API endpoints
    path('keyword-research', keyword_api.KeywordResearchAPIView.as_view(), name='keyword-research'),
]
