"""
URL configuration for content app.
"""
from django.urls import path
from . import api_views, views

app_name = 'content'

urlpatterns = [
    # Template view
    path('generator/', views.generator_view, name='generator'),
]
