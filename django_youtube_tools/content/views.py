from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def generator_view(request):
    """Render the content generator page"""
    return render(request, 'content/generator.html')
