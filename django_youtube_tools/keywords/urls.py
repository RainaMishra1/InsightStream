"""
URL configuration for keywords app.
"""
from django.urls import path
from . import api_views, views

app_name = 'keywords'

urlpatterns = [
    # Template view
    path('research/', views.research_view, name='research'),
]
