# Design Document: Next.js to Django Migration

## Overview

This design document outlines the architecture and implementation strategy for migrating a Next.js-based YouTube content creation platform to Django. The migration will transform a modern JavaScript full-stack application into a Python-based Django monolith while preserving all functionality, user experience, and external integrations.

The system provides AI-powered tools for YouTube creators including:
- AI thumbnail generation with reference image support
- YouTube thumbnail search and analysis
- Keyword research with YouTube trending data
- AI-powered content generation (titles, descriptions, tags)

The migration strategy focuses on:
1. Replacing Clerk authentication with Django's built-in auth system
2. Converting Drizzle ORM models to Django ORM models
3. Migrating Next.js API routes to Django REST Framework endpoints
4. Replacing Inngest background jobs with Celery tasks
5. Converting React components to Django templates with Alpine.js
6. Maintaining all external service integrations (AI services, ImageKit, YouTube API)

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Browser                        │
│  (Django Templates + Tailwind CSS + Alpine.js/Vanilla JS)  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/AJAX
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Django Application                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Django Middleware Layer                  │  │
│  │  - Authentication Middleware                          │  │
│  │  - CSRF Protection                                    │  │
│  │  - Session Management                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  URL Router                           │  │
│  │  - View Routes (Django Templates)                     │  │
│  │  - API Routes (Django REST Framework)                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  Views Layer                          │  │
│  │  - Template Views (render HTML)                       │  │
│  │  - API Views (return JSON)                            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               Service Layer                           │  │
│  │  - AI Service (Gemini, Replicate, HuggingFace)       │  │
│  │  - ImageKit Service                                   │  │
│  │  - YouTube Service                                    │  │
│  │  - Keyword Research Service                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  Models Layer                         │  │
│  │  - User Model                                         │  │
│  │  - Thumbnail Model                                    │  │
│  │  - AIContent Model                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │    Redis     │  │    Celery    │
│   Database   │  │   (Broker)   │  │   Workers    │
└──────────────┘  └──────────────┘  └──────────────┘
        │                                  │
        │                                  ▼
        │                          ┌──────────────┐
        │                          │  Background  │
        │                          │    Tasks     │
        │                          └──────────────┘
        │
        └──────────────────────────────────────────┐
                                                    ▼
                                    ┌───────────────────────────┐
                                    │   External Services       │
                                    │  - Gemini AI              │
                                    │  - Replicate AI           │
                                    │  - HuggingFace            │
                                    │  - OpenRouter             │
                                    │  - ImageKit CDN           │
                                    │  - YouTube Data API       │
                                    └───────────────────────────┘
```

### Django Project Structure

```
django_youtube_tools/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── accounts/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   └── templates/
│   │       └── accounts/
│   │           ├── login.html
│   │           └── register.html
│   ├── thumbnails/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── api_views.py
│   │   ├── urls.py
│   │   ├── tasks.py
│   │   ├── services.py
│   │   └── templates/
│   │       └── thumbnails/
│   │           ├── generator.html
│   │           └── search.html
│   ├── content/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── api_views.py
│   │   ├── urls.py
│   │   ├── tasks.py
│   │   ├── services.py
│   │   └── templates/
│   │       └── content/
│   │           └── generator.html
│   └── keywords/
│       ├── __init__.py
│       ├── views.py
│       ├── api_views.py
│       ├── urls.py
│       ├── services.py
│       └── templates/
│           └── keywords/
│               └── research.html
├── services/
│   ├── __init__.py
│   ├── ai_service.py
│   ├── imagekit_service.py
│   ├── youtube_service.py
│   └── gemini_rotation.py
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── thumbnail-generator.js
│       ├── thumbnail-search.js
│       ├── keyword-research.js
│       └── content-generator.js
├── templates/
│   ├── base.html
│   ├── home.html
│   └── components/
│       ├── header.html
│       └── sidebar.html
└── requirements.txt
```

## Components and Interfaces

### 1. Authentication System

**Django Built-in Auth**
- Uses Django's `django.contrib.auth` for user management
- Custom User model extending AbstractUser if needed
- Session-based authentication with cookies
- Login/Logout views with CSRF protection

**Interface:**
```python
# apps/accounts/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
```

**Views:**
```python
# apps/accounts/views.py
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def login_view(request):
    # Handle login form submission
    pass

def register_view(request):
    # Handle registration form submission
    pass

@login_required
def logout_view(request):
    # Handle logout
    pass
```

### 2. Database Models

**User Model**
```python
# apps/accounts/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
```

**Thumbnail Model**
```python
# apps/thumbnails/models.py
from django.db import models
from django.conf import settings

class Thumbnail(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='thumbnails'
    )
    user_input = models.CharField(max_length=500)
    thumbnail_url = models.URLField(max_length=1000)
    ref_image = models.URLField(max_length=500, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'thumbnails'
        ordering = ['-created_on']
```

**AIContent Model**
```python
# apps/content/models.py
from django.db import models
from django.conf import settings

class AIContent(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_contents'
    )
    user_input = models.CharField(max_length=500)
    content = models.JSONField()  # Stores titles, description, tags
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ai_content'
        ordering = ['-created_on']
```

### 3. Service Layer

**AI Service**
```python
# services/ai_service.py
from google.generativeai import GenerativeModel
import replicate
import requests

class AIService:
    def __init__(self):
        self.gemini_client = None
        self.replicate_client = None
        
    def generate_thumbnail_with_replicate(self, prompt, ref_image=None):
        """Generate thumbnail using Replicate FLUX model"""
        pass
        
    def generate_thumbnail_with_pollinations(self, prompt):
        """Fallback thumbnail generation using Pollinations"""
        pass
        
    def generate_keywords_with_gemini(self, topic, youtube_data):
        """Generate keyword research using Gemini"""
        pass
        
    def extract_tags_from_thumbnail(self, thumbnail_url):
        """Extract keywords from thumbnail using AI"""
        pass
        
    def generate_content_metadata(self, user_input):
        """Generate titles, description, and tags"""
        pass
```

**ImageKit Service**
```python
# services/imagekit_service.py
from imagekitio import ImageKit

class ImageKitService:
    def __init__(self):
        self.imagekit = ImageKit(
            public_key=settings.IMAGEKIT_PUBLIC_KEY,
            private_key=settings.IMAGEKIT_PRIVATE_KEY,
            url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
        )
    
    def upload_image(self, file_buffer, filename, folder='/thumbnails'):
        """Upload image to ImageKit and return URL"""
        pass
```

**YouTube Service**
```python
# services/youtube_service.py
import requests

class YouTubeService:
    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
        self.base_url = 'https://www.googleapis.com/youtube/v3'
    
    def search_videos(self, query, max_results=20):
        """Search YouTube videos by query"""
        pass
        
    def get_video_details(self, video_ids):
        """Get detailed video information including statistics"""
        pass
        
    def get_trending_keywords(self, topic):
        """Get trending video titles for a topic"""
        pass
```

**Gemini Key Rotation**
```python
# services/gemini_rotation.py
class GeminiKeyRotation:
    def __init__(self):
        self.keys = [
            settings.GEMINI_API_KEY_1,
            settings.GEMINI_API_KEY_2,
            settings.GEMINI_API_KEY_3,
        ]
        self.current_index = 0
    
    def get_next_key(self):
        """Rotate through API keys to avoid rate limits"""
        key = self.keys[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.keys)
        return key
```

### 4. API Views (Django REST Framework)

**Thumbnail API**
```python
# apps/thumbnails/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import generate_thumbnail_task

class ThumbnailGenerateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Queue thumbnail generation task"""
        user_input = request.data.get('userInput')
        ref_image = request.FILES.get('refImage')
        
        # Queue Celery task
        task = generate_thumbnail_task.delay(
            user_input=user_input,
            ref_image=ref_image,
            user_email=request.user.email
        )
        
        return Response({
            'task_id': task.id,
            'status': 'processing'
        })
    
    def get(self, request):
        """Get user's thumbnail history"""
        thumbnails = Thumbnail.objects.filter(user=request.user)
        serializer = ThumbnailSerializer(thumbnails, many=True)
        return Response(serializer.data)
```

**Thumbnail Search API**
```python
# apps/thumbnails/api_views.py
class ThumbnailSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Search YouTube thumbnails by query or thumbnail URL"""
        query = request.query_params.get('query')
        thumbnail_url = request.query_params.get('thumbnailUrl')
        
        if thumbnail_url:
            # Extract tags using AI
            ai_service = AIService()
            tags = ai_service.extract_tags_from_thumbnail(thumbnail_url)
            return Response({'tags': tags})
        
        if query:
            # Search YouTube
            youtube_service = YouTubeService()
            results = youtube_service.search_videos(query)
            return Response(results)
        
        return Response({'error': 'Query parameter required'}, status=400)
```

**Keyword Research API**
```python
# apps/keywords/api_views.py
class KeywordResearchAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Generate keyword research for a topic"""
        topic = request.data.get('topic')
        
        # Get YouTube trending data
        youtube_service = YouTubeService()
        trending_keywords = youtube_service.get_trending_keywords(topic)
        
        # Generate keywords with AI
        ai_service = AIService()
        keyword_data = ai_service.generate_keywords_with_gemini(
            topic, trending_keywords
        )
        
        return Response({
            'success': True,
            'data': keyword_data,
            'topic': topic
        })
```

**Content Generator API**
```python
# apps/content/api_views.py
class ContentGeneratorAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Queue content generation task"""
        user_input = request.data.get('userInput')
        ref_image = request.FILES.get('refImage')
        
        # Queue Celery task
        task = generate_content_task.delay(
            user_input=user_input,
            ref_image=ref_image,
            user_email=request.user.email
        )
        
        return Response({
            'task_id': task.id,
            'status': 'processing'
        })
    
    def get(self, request):
        """Get user's content history"""
        contents = AIContent.objects.filter(user=request.user)
        serializer = AIContentSerializer(contents, many=True)
        return Response(serializer.data)
```

### 5. Celery Background Tasks

**Celery Configuration**
```python
# config/celery.py
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('django_youtube_tools')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

**Thumbnail Generation Task**
```python
# apps/thumbnails/tasks.py
from celery import shared_task
from services.ai_service import AIService
from services.imagekit_service import ImageKitService
from .models import Thumbnail

@shared_task(bind=True, max_retries=3)
def generate_thumbnail_task(self, user_input, ref_image, user_email):
    try:
        ai_service = AIService()
        imagekit_service = ImageKitService()
        
        # Generate thumbnail
        if ref_image:
            image_blob = ai_service.generate_thumbnail_with_replicate(
                user_input, ref_image
            )
        else:
            try:
                image_blob = ai_service.generate_thumbnail_with_replicate(
                    user_input
                )
            except Exception:
                image_blob = ai_service.generate_thumbnail_with_pollinations(
                    user_input
                )
        
        # Upload to ImageKit
        thumbnail_url = imagekit_service.upload_image(
            image_blob, f'thumbnail_{int(time.time())}.png'
        )
        
        # Save to database
        user = User.objects.get(email=user_email)
        Thumbnail.objects.create(
            user=user,
            user_input=user_input,
            thumbnail_url=thumbnail_url,
            ref_image=ref_image
        )
        
        return {'success': True, 'thumbnail_url': thumbnail_url}
        
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
```

**Content Generation Task**
```python
# apps/content/tasks.py
from celery import shared_task
from services.ai_service import AIService
from .models import AIContent

@shared_task(bind=True, max_retries=3)
def generate_content_task(self, user_input, ref_image, user_email):
    try:
        ai_service = AIService()
        
        # Generate content metadata
        content_data = ai_service.generate_content_metadata(user_input)
        
        # Save to database
        user = User.objects.get(email=user_email)
        AIContent.objects.create(
            user=user,
            user_input=user_input,
            content=content_data
        )
        
        return {'success': True, 'content': content_data}
        
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
```

### 6. Frontend Templates

**Base Template**
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}YouTube Tools{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body>
    {% include 'components/header.html' %}
    
    <div class="flex">
        {% include 'components/sidebar.html' %}
        
        <main class="flex-1 p-6">
            {% block content %}{% endblock %}
        </main>
    </div>
    
    {% block scripts %}{% endblock %}
</body>
</html>
```

**Thumbnail Generator Template**
```html
<!-- apps/thumbnails/templates/thumbnails/generator.html -->
{% extends 'base.html' %}

{% block content %}
<div x-data="thumbnailGenerator()">
    <h1 class="text-2xl font-bold mb-4">AI Thumbnail Generator</h1>
    
    <form @submit.prevent="generateThumbnail">
        <input 
            type="text" 
            x-model="userInput" 
            placeholder="Enter video title or description"
            class="w-full p-2 border rounded"
        />
        
        <input 
            type="file" 
            @change="handleFileUpload"
            accept="image/*"
            class="mt-2"
        />
        
        <button 
            type="submit"
            :disabled="loading"
            class="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
        >
            <span x-show="!loading">Generate</span>
            <span x-show="loading">Generating...</span>
        </button>
    </form>
    
    <div x-show="thumbnailUrl" class="mt-6">
        <img :src="thumbnailUrl" alt="Generated Thumbnail" class="max-w-md" />
    </div>
    
    <div class="mt-8">
        <h2 class="text-xl font-bold mb-4">Your Thumbnails</h2>
        <div class="grid grid-cols-3 gap-4">
            <template x-for="thumb in thumbnails" :key="thumb.id">
                <img :src="thumb.thumbnail_url" class="w-full rounded" />
            </template>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script src="{% static 'js/thumbnail-generator.js' %}"></script>
{% endblock %}
```

**Alpine.js Component**
```javascript
// static/js/thumbnail-generator.js
function thumbnailGenerator() {
    return {
        userInput: '',
        refImage: null,
        loading: false,
        thumbnailUrl: '',
        thumbnails: [],
        
        async init() {
            await this.loadThumbnails();
        },
        
        handleFileUpload(event) {
            this.refImage = event.target.files[0];
        },
        
        async generateThumbnail() {
            this.loading = true;
            
            const formData = new FormData();
            formData.append('userInput', this.userInput);
            if (this.refImage) {
                formData.append('refImage', this.refImage);
            }
            
            try {
                const response = await fetch('/api/generate-thumbnail', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    this.thumbnailUrl = data.thumbnailUrl;
                    await this.loadThumbnails();
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to generate thumbnail');
            } finally {
                this.loading = false;
            }
        },
        
        async loadThumbnails() {
            const response = await fetch('/api/generate-thumbnail');
            this.thumbnails = await response.json();
        }
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
```

## Data Models

### Entity Relationship Diagram

```
┌─────────────────────┐
│       User          │
│─────────────────────│
│ id (PK)             │
│ username            │
│ email (UNIQUE)      │
│ password            │
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │
           │ 1:N
           │
     ┌─────┴──────┬──────────────┐
     │            │              │
     ▼            ▼              ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│Thumbnail│  │AIContent│  │  Other  │
│─────────│  │─────────│  │─────────│
│id (PK)  │  │id (PK)  │  │         │
│user_id  │  │user_id  │  │         │
│(FK)     │  │(FK)     │  │         │
│user_    │  │user_    │  │         │
│input    │  │input    │  │         │
│thumbnail│  │content  │  │         │
│_url     │  │(JSON)   │  │         │
│ref_image│  │thumbnail│  │         │
│created_ │  │_url     │  │         │
│on       │  │created_ │  │         │
│         │  │on       │  │         │
└─────────┘  └─────────┘  └─────────┘
```

### Model Relationships

1. **User → Thumbnail**: One-to-Many
   - One user can have multiple thumbnails
   - Cascade delete: When user is deleted, all thumbnails are deleted

2. **User → AIContent**: One-to-Many
   - One user can have multiple AI-generated content records
   - Cascade delete: When user is deleted, all content is deleted

### Data Flow

**Thumbnail Generation Flow:**
```
User Input → API View → Celery Task → AI Service → ImageKit → Database → Response
```

**Keyword Research Flow:**
```
User Topic → API View → YouTube Service → AI Service → Response
```

## Correctnes
s Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: User Registration Creates Database Record
*For any* valid email and password combination, when a user registers, the system should create a user record in the database with that email.
**Validates: Requirements 1.1**

### Property 2: Valid Credentials Authenticate Successfully
*For any* registered user with valid credentials, login should succeed and create an authenticated session.
**Validates: Requirements 1.2**

### Property 3: Authenticated Sessions Access Protected Routes
*For any* authenticated user session, accessing protected routes should succeed without redirect.
**Validates: Requirements 1.3**

### Property 4: Unauthenticated Requests Are Blocked
*For any* protected route, unauthenticated requests should be redirected to the login page.
**Validates: Requirements 1.4**

### Property 5: Logout Terminates Session
*For any* authenticated user, logging out then attempting to access protected routes should fail (round-trip property).
**Validates: Requirements 1.5**

### Property 6: Cascading Delete Maintains Referential Integrity
*For any* user with associated thumbnails and content, deleting the user should also delete all related records.
**Validates: Requirements 2.4**

### Property 7: Text Description Generates Thumbnail
*For any* valid text description, thumbnail generation should return a valid thumbnail URL.
**Validates: Requirements 3.1**

### Property 8: Reference Image Generation Succeeds
*For any* valid reference image and text description, thumbnail generation should return a valid thumbnail URL.
**Validates: Requirements 3.2**

### Property 9: Generated Thumbnails Upload to ImageKit
*For any* generated thumbnail, the system should upload it to ImageKit and return a valid ImageKit URL.
**Validates: Requirements 3.3**

### Property 10: AI Service Fallback Works
*For any* thumbnail generation request, if the primary AI service fails, the fallback service should be used and generation should succeed.
**Validates: Requirements 3.4**

### Property 11: Thumbnail Generation Round-Trip
*For any* generated thumbnail, querying the database should return the thumbnail record with correct user association.
**Validates: Requirements 3.5**

### Property 12: Thumbnail History Ordering
*For any* user with multiple thumbnails, requesting history should return thumbnails ordered by creation date descending.
**Validates: Requirements 3.6**

### Property 13: YouTube Search Returns Results
*For any* valid search query, YouTube search should return video results with thumbnails.
**Validates: Requirements 4.1**

### Property 14: AI Extracts Tags from Thumbnails
*For any* thumbnail URL, AI should extract and return relevant keywords.
**Validates: Requirements 4.2**

### Property 15: Tag Extraction Enables Search
*For any* thumbnail URL, extracting tags then searching YouTube with those tags should return relevant videos.
**Validates: Requirements 4.3**

### Property 16: YouTube Results Include Required Fields
*For any* YouTube search result, the response should include title, thumbnail, views, likes, and comments.
**Validates: Requirements 4.4**

### Property 17: High-Quality Thumbnails in Results
*For any* YouTube search result, the thumbnail URL should be the high-quality version.
**Validates: Requirements 4.5**

### Property 18: Keyword Research Fetches Trending Videos
*For any* topic, keyword research should fetch trending YouTube videos for that topic.
**Validates: Requirements 5.1**

### Property 19: YouTube Data Sent to AI
*For any* keyword research request, YouTube trending data should be sent to AI for analysis.
**Validates: Requirements 5.2**

### Property 20: AI Generates Keywords with Metadata
*For any* topic, AI should generate primary keywords with search volume and competition metrics.
**Validates: Requirements 5.3**

### Property 21: Keywords Are Categorized
*For any* keyword research result, keywords should be categorized into primary, long-tail, and trending.
**Validates: Requirements 5.4**

### Property 22: Keyword Research Returns Complete JSON
*For any* keyword research request, the response should include keywords, related topics, and content suggestions.
**Validates: Requirements 5.5**

### Property 23: API Key Rotation Prevents Rate Limits
*For any* set of concurrent requests, the system should rotate between multiple Gemini API keys.
**Validates: Requirements 5.6**

### Property 24: Content Generation Returns Three Titles
*For any* video topic, content generation should return exactly three title options.
**Validates: Requirements 6.1**

### Property 25: Titles Include SEO Scores
*For any* generated title, an SEO score should be included.
**Validates: Requirements 6.2**

### Property 26: Description Is Generated
*For any* video topic, content generation should return a non-empty description.
**Validates: Requirements 6.3**

### Property 27: Ten Tags Are Generated
*For any* content generation request, exactly ten tags should be returned.
**Validates: Requirements 6.4**

### Property 28: Content Generation Round-Trip
*For any* generated content, querying the database should return the content record with correct user association.
**Validates: Requirements 6.5**

### Property 29: Malformed AI Responses Handled Gracefully
*For any* malformed AI response, the system should parse gracefully and return fallback data without crashing.
**Validates: Requirements 6.6**

### Property 30: Thumbnail Requests Queue Celery Tasks
*For any* thumbnail generation request, a Celery task should be created and queued.
**Validates: Requirements 7.1**

### Property 31: Content Requests Queue Celery Tasks
*For any* content generation request, a Celery task should be created and queued.
**Validates: Requirements 7.2**

### Property 32: Celery Tasks Execute in Background
*For any* queued Celery task, the task should execute in a background worker.
**Validates: Requirements 7.3**

### Property 33: Completed Tasks Update Database
*For any* completed background task, the database should be updated with results.
**Validates: Requirements 7.4**

### Property 34: Failed Tasks Retry with Backoff
*For any* failed background task, the system should retry with exponential backoff.
**Validates: Requirements 7.5**

### Property 35: Task Status Is Queryable
*For any* queued task, requesting status should return the current Celery task status.
**Validates: Requirements 7.6**

### Property 36: Protected Endpoints Require Authentication
*For any* protected API endpoint, unauthenticated requests should be rejected.
**Validates: Requirements 8.7**

### Property 37: API Responses Match Next.js Format
*For any* API endpoint response, the JSON structure should match the original Next.js response format.
**Validates: Requirements 8.8**

### Property 38: Forms Submit via AJAX
*For any* form submission, the request should be sent via AJAX to the appropriate API endpoint.
**Validates: Requirements 9.3**

### Property 39: DOM Updates Without Page Reload
*For any* API response, the DOM should update dynamically without triggering a page reload.
**Validates: Requirements 9.4**

### Property 40: AI Services Use Configured Keys
*For any* AI service call, the system should use the configured API key from environment variables.
**Validates: Requirements 10.2**

### Property 41: ImageKit Uses Configured Credentials
*For any* image upload, the system should use ImageKit configuration from environment variables.
**Validates: Requirements 10.3**

### Property 42: YouTube API Uses Configured Key
*For any* YouTube API call, the system should use the configured YouTube API key.
**Validates: Requirements 10.4**

### Property 43: Errors Are Logged with Stack Traces
*For any* API endpoint error, the system should log the error with a complete stack trace.
**Validates: Requirements 11.1**

### Property 44: External API Failures Return Friendly Messages
*For any* external API failure, the system should return a user-friendly error message (not raw error details).
**Validates: Requirements 11.2**

### Property 45: Database Failures Trigger Rollback
*For any* database operation failure, the system should rollback the transaction and log the error.
**Validates: Requirements 11.3**

### Property 46: Malformed AI Responses Use Fallback
*For any* malformed AI response, the system should parse gracefully and use fallback data.
**Validates: Requirements 11.4**

### Property 47: Background Task Failures Are Logged and Retried
*For any* background task failure, the system should log the failure and retry according to the configured policy.
**Validates: Requirements 11.5**

## Error Handling

### Error Categories

1. **Authentication Errors**
   - Invalid credentials → Return 401 with message "Invalid email or password"
   - Missing session → Redirect to login page
   - Expired session → Clear session and redirect to login

2. **Validation Errors**
   - Missing required fields → Return 400 with field-specific error messages
   - Invalid file types → Return 400 with "Invalid file type. Please upload an image."
   - File size too large → Return 413 with "File size exceeds maximum limit"

3. **External Service Errors**
   - AI service timeout → Retry with fallback service
   - ImageKit upload failure → Return 500 with "Failed to upload image. Please try again."
   - YouTube API rate limit → Return 429 with "Rate limit exceeded. Please try again later."
   - YouTube API error → Return 500 with "Failed to fetch YouTube data"

4. **Database Errors**
   - Connection failure → Log error and return 500 with "Database connection error"
   - Constraint violation → Rollback transaction and return 400 with specific error
   - Query timeout → Log error and return 500 with "Request timeout"

5. **Background Task Errors**
   - Task failure → Retry with exponential backoff (3 attempts)
   - Max retries exceeded → Log error and mark task as failed
   - Task timeout → Cancel task and log error

### Error Handling Strategy

```python
# Example error handling in API views
from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Log all errors
    logger.error(
        f"API Error: {exc}",
        exc_info=True,
        extra={'context': context}
    )
    
    # Customize error responses
    if response is None:
        # Handle non-DRF exceptions
        return Response(
            {'error': 'An unexpected error occurred'},
            status=500
        )
    
    return response
```

### Retry Logic for External Services

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def call_external_api(url, data):
    """Retry external API calls with exponential backoff"""
    response = requests.post(url, json=data, timeout=30)
    response.raise_for_status()
    return response.json()
```

## Testing Strategy

### Testing Approach

The Django migration will use a comprehensive testing strategy combining:

1. **Unit Tests** - Test individual components in isolation
2. **Property-Based Tests** - Verify universal properties hold across all inputs
3. **Integration Tests** - Test component interactions and external services
4. **End-to-End Tests** - Verify complete user workflows

### Property-Based Testing

We will use **Hypothesis** (Python's property-based testing library) to implement the correctness properties defined above.

**Configuration:**
- Each property-based test will run a minimum of 100 iterations
- Tests will use Hypothesis strategies to generate random valid inputs
- Each test will be tagged with a comment referencing the design document property

**Example Property Test:**
```python
# tests/test_authentication.py
from hypothesis import given, strategies as st
from django.test import TestCase
from apps.accounts.models import User

class TestAuthenticationProperties(TestCase):
    
    @given(
        email=st.emails(),
        password=st.text(min_size=8, max_size=50)
    )
    def test_user_registration_creates_database_record(self, email, password):
        """
        **Feature: nextjs-to-django-migration, Property 1: User Registration Creates Database Record**
        
        For any valid email and password, registration should create a user record.
        """
        # Register user
        response = self.client.post('/api/register', {
            'email': email,
            'password': password
        })
        
        # Verify user exists in database
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email=email).exists())
```

### Unit Testing

Unit tests will cover:
- Model methods and properties
- Service layer functions
- Utility functions
- Form validation
- Serializer behavior

**Example Unit Test:**
```python
# tests/test_models.py
from django.test import TestCase
from apps.thumbnails.models import Thumbnail
from apps.accounts.models import User

class ThumbnailModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_thumbnail_creation(self):
        """Test thumbnail model creation"""
        thumbnail = Thumbnail.objects.create(
            user=self.user,
            user_input='Test video title',
            thumbnail_url='https://imagekit.io/test.png'
        )
        
        self.assertEqual(thumbnail.user, self.user)
        self.assertEqual(thumbnail.user_input, 'Test video title')
        self.assertIsNotNone(thumbnail.created_on)
    
    def test_cascade_delete(self):
        """Test that deleting user deletes thumbnails"""
        Thumbnail.objects.create(
            user=self.user,
            user_input='Test',
            thumbnail_url='https://test.com/img.png'
        )
        
        user_id = self.user.id
        self.user.delete()
        
        # Verify thumbnails are deleted
        self.assertEqual(
            Thumbnail.objects.filter(user_id=user_id).count(),
            0
        )
```

### Integration Testing

Integration tests will verify:
- API endpoint behavior
- Database transactions
- External service integrations (with mocking)
- Celery task execution
- Authentication middleware

**Example Integration Test:**
```python
# tests/test_api_integration.py
from django.test import TestCase
from unittest.mock import patch, MagicMock
from apps.accounts.models import User

class ThumbnailAPIIntegrationTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(email='test@example.com', password='testpass123')
    
    @patch('services.ai_service.AIService.generate_thumbnail_with_replicate')
    @patch('services.imagekit_service.ImageKitService.upload_image')
    def test_thumbnail_generation_flow(self, mock_upload, mock_generate):
        """Test complete thumbnail generation flow"""
        # Mock external services
        mock_generate.return_value = b'fake_image_data'
        mock_upload.return_value = 'https://imagekit.io/generated.png'
        
        # Make request
        response = self.client.post('/api/generate-thumbnail', {
            'userInput': 'Test video title'
        })
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertIn('task_id', response.json())
        
        # Verify services were called
        mock_generate.assert_called_once()
        mock_upload.assert_called_once()
```

### End-to-End Testing

E2E tests will verify complete user workflows using Selenium or Playwright:
- User registration and login flow
- Thumbnail generation from UI
- Keyword research workflow
- Content generation workflow

### Test Coverage Goals

- Minimum 80% code coverage
- 100% coverage of critical paths (authentication, payment, data persistence)
- All correctness properties implemented as property-based tests
- All API endpoints covered by integration tests

### Continuous Integration

Tests will run automatically on:
- Every commit (unit tests + property tests)
- Pull requests (full test suite)
- Pre-deployment (full test suite + E2E tests)

## Deployment Considerations

### Environment Setup

**Development:**
- SQLite database for local development
- Redis for Celery (Docker container)
- Environment variables in `.env` file
- Django debug mode enabled

**Production:**
- Neon PostgreSQL database
- Redis Cloud or AWS ElastiCache
- Environment variables from hosting platform
- Django debug mode disabled
- Static files served via CDN
- Gunicorn + Nginx for serving

### Required Environment Variables

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# AI Services
GEMINI_API_KEY_1=your-key-1
GEMINI_API_KEY_2=your-key-2
GEMINI_API_KEY_3=your-key-3
REPLICATE_API_TOKEN=your-replicate-token
HF_API_TOKEN=your-huggingface-token
OPENROUTER_API_KEY=your-openrouter-key

# ImageKit
IMAGEKIT_PUBLIC_KEY=your-public-key
IMAGEKIT_PRIVATE_KEY=your-private-key
IMAGEKIT_URL_ENDPOINT=your-endpoint

# YouTube
YOUTUBE_API_KEY=your-youtube-key
```

### Deployment Steps

1. Set up PostgreSQL database
2. Set up Redis instance
3. Configure environment variables
4. Run database migrations
5. Collect static files
6. Start Gunicorn workers
7. Start Celery workers
8. Configure Nginx reverse proxy
9. Set up SSL certificates
10. Configure monitoring and logging

### Monitoring and Logging

- Use Django's logging framework
- Log all errors with stack traces
- Monitor Celery task queue length
- Track API response times
- Monitor external service failures
- Set up alerts for critical errors

## Migration Strategy

### Phase 1: Backend Setup (Week 1)
1. Set up Django project structure
2. Configure database and models
3. Implement authentication system
4. Set up Celery for background tasks

### Phase 2: Core Services (Week 2)
1. Implement AI service integrations
2. Implement ImageKit service
3. Implement YouTube service
4. Implement Gemini key rotation

### Phase 3: API Endpoints (Week 3)
1. Implement thumbnail generation API
2. Implement thumbnail search API
3. Implement keyword research API
4. Implement content generation API

### Phase 4: Frontend Migration (Week 4)
1. Create Django templates
2. Implement Alpine.js components
3. Style with Tailwind CSS
4. Implement AJAX interactions

### Phase 5: Testing & Deployment (Week 5)
1. Write unit tests
2. Write property-based tests
3. Write integration tests
4. Deploy to production
5. Monitor and fix issues

## Conclusion

This design document provides a comprehensive blueprint for migrating the Next.js YouTube content creation platform to Django. The migration maintains all functionality while replacing external dependencies (Clerk, Inngest) with Django-native solutions (Django Auth, Celery). The architecture follows Django best practices with clear separation of concerns, comprehensive error handling, and a robust testing strategy using property-based testing to ensure correctness.
