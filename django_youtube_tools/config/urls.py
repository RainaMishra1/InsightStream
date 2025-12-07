"""
URL configuration for Django YouTube Tools project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('accounts/', include('accounts.urls')),
    
    # App URLs (template views)
    path('thumbnails/', include('thumbnails.urls')),
    path('content/', include('content.urls')),
    path('keywords/', include('keywords.urls')),
    
    # API URLs
    path('api/', include('config.api_urls')),
    
    # Home page - redirect to dashboard
    path('', RedirectView.as_view(url='/accounts/dashboard/', permanent=False), name='home'),
    path('dashboard/', RedirectView.as_view(url='/accounts/dashboard/', permanent=False), name='dashboard'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
