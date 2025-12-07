from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def generator_view(request):
    """Render the thumbnail generator page"""
    return render(request, 'thumbnails/generator.html')

@login_required
def search_view(request):
    """Render the thumbnail search page"""
    return render(request, 'thumbnails/search.html')
