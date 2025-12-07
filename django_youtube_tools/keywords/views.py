from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def research_view(request):
    """Render the keyword research page"""
    return render(request, 'keywords/research.html')
