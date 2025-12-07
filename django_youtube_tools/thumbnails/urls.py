"""
URL configuration for thumbnails app.
"""
from django.urls import path
from . import api_views, views

app_name = 'thumbnails'

urlpatterns = [
    # Template views
    path('generator/', views.generator_view, name='generator'),
    path('search/', views.search_view, name='search'),
]
