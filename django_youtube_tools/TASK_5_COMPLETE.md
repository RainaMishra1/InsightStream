# Task 5: Service Layer for External Integrations - COMPLETE ✅

## What Was Accomplished

### 5.1 AI Service Class ✅

**File:** `services/ai_service.py`

**Features Implemented:**
- **Thumbnail Generation with Replicate**: FLUX model integration for high-quality thumbnails
- **Thumbnail Generation with Pollinations**: Free fallback service
- **Keyword Research with Gemini**: Comprehensive keyword analysis with YouTube data
- **Tag Extraction from Thumbnails**: AI-powered keyword extraction from images
- **Content Metadata Generation**: Titles, descriptions, and tags for videos

**Methods:**
- `generate_thumbnail_with_replicate(prompt, ref_image=None)`: Generate thumbnails using Replicate FLUX
- `generate_thumbnail_with_pollinations(prompt)`: Fallback thumbnail generation
- `generate_keywords_with_gemini(topic, youtube_data)`: Keyword research with AI
- `extract_tags_from_thumbnail(thumbnail_url)`: Extract keywords from thumbnail images
- `generate_content_metadata(user_input)`: Generate video titles, description, and tags

**AI Providers Integrated:**
- ✅ Google Gemini (via google-generativeai SDK)
- ✅ Replicate (FLUX model)
- ✅ Pollinations AI (free fallback)
- ✅ OpenRouter (Gemini API proxy)

**Error Handling:**
- Comprehensive logging for all operations
- Graceful fallback data when AI fails
- JSON parsing with regex extraction
- Proper exception raising with context

### 5.2 ImageKit Service Class ✅

**File:** `services/imagekit_service.py`

**Features Implemented:**
- **Image Upload**: Upload images to ImageKit CDN
- **Upload from URL**: Download and upload images from URLs
- **File Management**: Delete and get file details
- **Base64 Encoding**: Automatic conversion of bytes to base64

**Methods:**
- `upload_image(file_buffer, filename, folder='/thumbnails')`: Upload image bytes
- `upload_from_url(image_url, filename, folder='/thumbnails')`: Upload from URL
- `delete_file(file_id)`: Delete file from ImageKit
- `get_file_details(file_id)`: Get file metadata

**Configuration:**
- Uses ImageKit SDK (imagekitio)
- Credentials from Django settings
- Automatic folder organization
- Unique filename generation

**Error Handling:**
- Validates credentials on initialization
- Comprehensive error logging
- Proper exception propagation

### 5.3 YouTube Service Class ✅

**File:** `services/youtube_service.py`

**Features Implemented:**
- **Video Search**: Search YouTube videos by query
- **Video Details**: Fetch detailed video information with statistics
- **Trending Keywords**: Get trending video titles for keyword research
- **Channel Information**: Fetch channel details and statistics

**Methods:**
- `search_videos(query, max_results=20)`: Search videos and return full details
- `get_video_details(video_ids)`: Get detailed info for specific videos
- `get_trending_keywords(topic, max_results=10)`: Get trending titles for topic
- `get_channel_info(channel_id)`: Get channel information

**YouTube Data API v3 Integration:**
- Search API for video discovery
- Videos API for detailed information
- Statistics included (views, likes, comments)
- High-quality thumbnail URLs
- Proper URL encoding and parameter handling

**Error Handling:**
- Fallback to topic when API fails
- Comprehensive error logging
- Timeout handling (30 seconds)
- Proper HTTP status code checking

### 5.4 Gemini Key Rotation Utility ✅

**File:** `services/gemini_rotation.py`

**Features Implemented:**
- **Round-Robin Rotation**: Automatic key rotation across requests
- **Thread-Safe**: Uses threading locks for concurrent requests
- **Usage Tracking**: Tracks usage count for each key
- **Statistics**: Get usage stats for monitoring

**Methods:**
- `get_next_key()`: Get next key in rotation (thread-safe)
- `get_key_by_index(index)`: Get specific key by index
- `get_usage_stats()`: Get usage statistics for all keys
- `reset_usage_stats()`: Reset usage counters
- `get_total_keys()`: Get number of configured keys
- `is_configured()`: Check if keys are available

**Key Rotation Logic:**
```
Request 1 → Key 1
Request 2 → Key 2
Request 3 → Key 3
Request 4 → Key 1 (cycle repeats)
```

**Thread Safety:**
- Uses `threading.Lock()` for synchronization
- Double-check locking pattern for singleton
- Safe for concurrent Celery tasks

**Convenience Functions:**
- `get_next_gemini_key()`: Quick access to next key
- `get_gemini_usage_stats()`: Quick access to stats

## File Structure

```
django_youtube_tools/
└── services/
    ├── __init__.py
    ├── ai_service.py           # AI integrations (Gemini, Replicate, etc.)
    ├── imagekit_service.py     # ImageKit CDN integration
    ├── youtube_service.py      # YouTube Data API integration
    ├── gemini_rotation.py      # API key rotation utility
    └── celery_tasks.py         # Celery base classes (from Task 4)
```

## Usage Examples

### AI Service

```python
from services.ai_service import get_ai_service

ai_service = get_ai_service()

# Generate thumbnail with Replicate
image_data = ai_service.generate_thumbnail_with_replicate(
    prompt="Gaming tutorial thumbnail",
    ref_image=None
)

# Generate thumbnail with Pollinations (fallback)
image_data = ai_service.generate_thumbnail_with_pollinations(
    prompt="Cooking recipe thumbnail"
)

# Keyword research
keywords = ai_service.generate_keywords_with_gemini(
    topic="Python programming",
    youtube_data=["Learn Python", "Python Tutorial", "Python for Beginners"]
)

# Extract tags from thumbnail
tags = ai_service.extract_tags_from_thumbnail(
    thumbnail_url="https://example.com/thumbnail.jpg"
)

# Generate content metadata
content = ai_service.generate_content_metadata(
    user_input="How to learn Django"
)
```

### ImageKit Service

```python
from services.imagekit_service import get_imagekit_service

imagekit = get_imagekit_service()

# Upload image
url = imagekit.upload_image(
    file_buffer=image_bytes,
    filename="thumbnail_123.png",
    folder="/thumbnails"
)

# Upload from URL
url = imagekit.upload_from_url(
    image_url="https://example.com/image.jpg",
    filename="thumbnail_456.png"
)

# Delete file
imagekit.delete_file(file_id="abc123")
```

### YouTube Service

```python
from services.youtube_service import get_youtube_service

youtube = get_youtube_service()

# Search videos
videos = youtube.search_videos(
    query="Django tutorial",
    max_results=20
)

# Get video details
details = youtube.get_video_details(
    video_ids=["abc123", "def456"]
)

# Get trending keywords
titles = youtube.get_trending_keywords(
    topic="Web development",
    max_results=10
)

# Get channel info
channel = youtube.get_channel_info(
    channel_id="UC123456"
)
```

### Gemini Key Rotation

```python
from services.gemini_rotation import get_next_gemini_key, get_gemini_usage_stats

# Get next key
api_key = get_next_gemini_key()

# Use with Gemini
import google.generativeai as genai
genai.configure(api_key=api_key)

# Get usage stats
stats = get_gemini_usage_stats()
# Output: {0: 10, 1: 8, 2: 12}
```

## Singleton Pattern

All services use the singleton pattern for efficiency:

```python
# First call creates instance
service1 = get_ai_service()

# Subsequent calls return same instance
service2 = get_ai_service()

assert service1 is service2  # True
```

## Error Handling Strategy

### AI Service Errors
- **Replicate fails** → Try Pollinations fallback
- **Gemini fails** → Return fallback data structure
- **JSON parsing fails** → Use regex extraction or fallback
- **All methods log errors** with full context

### ImageKit Service Errors
- **Credentials missing** → Raise ValueError with clear message
- **Upload fails** → Log error and raise exception
- **Network timeout** → Handled by requests library

### YouTube Service Errors
- **API key missing** → Return fallback data (topic)
- **API call fails** → Log error and raise exception
- **No results** → Return empty list
- **Network timeout** → 30-second timeout configured

### Gemini Rotation Errors
- **No keys configured** → Raise ValueError
- **Index out of range** → Raise IndexError
- **Thread safety** → Handled by locks

## Configuration Requirements

### Environment Variables Needed

```env
# AI Services
GEMINI_API_KEY_1=your-gemini-key-1
GEMINI_API_KEY_2=your-gemini-key-2
GEMINI_API_KEY_3=your-gemini-key-3
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

### Python Dependencies

```
google-generativeai==0.3.2
replicate==0.23.1
imagekitio==3.2.0
requests==2.31.0
```

## Logging

All services use Python's logging module:

```python
import logging
logger = logging.getLogger(__name__)

# Log levels used:
logger.info()     # Successful operations
logger.warning()  # Fallback usage, missing config
logger.error()    # Operation failures
logger.debug()    # Detailed debugging info
```

## Testing Services

### Test AI Service

```python
python manage.py shell

from services.ai_service import get_ai_service

ai = get_ai_service()

# Test keyword generation
keywords = ai.generate_keywords_with_gemini(
    "Python programming",
    ["Learn Python", "Python Tutorial"]
)
print(keywords)
```

### Test ImageKit Service

```python
from services.imagekit_service import get_imagekit_service

imagekit = get_imagekit_service()

# Check if configured
if imagekit.imagekit:
    print("✅ ImageKit configured")
else:
    print("⚠️  ImageKit not configured")
```

### Test YouTube Service

```python
from services.youtube_service import get_youtube_service

youtube = get_youtube_service()

# Test search
videos = youtube.search_videos("Django", max_results=5)
print(f"Found {len(videos)} videos")
```

### Test Gemini Rotation

```python
from services.gemini_rotation import get_gemini_rotation

rotation = get_gemini_rotation()

print(f"Total keys: {rotation.get_total_keys()}")
print(f"Configured: {rotation.is_configured()}")

# Get keys in rotation
for i in range(5):
    key = rotation.get_next_key()
    print(f"Request {i+1}: Key #{rotation.current_index}")

# Check usage
print(rotation.get_usage_stats())
```

## Requirements Validated

✅ **Requirement 3.1**: AI service generates thumbnails from text
✅ **Requirement 3.2**: AI service generates thumbnails with reference images
✅ **Requirement 3.3**: ImageKit service uploads images and returns URLs
✅ **Requirement 3.4**: AI service has fallback mechanism
✅ **Requirement 4.1**: YouTube service searches videos and returns results
✅ **Requirement 4.2**: AI service extracts keywords from thumbnails
✅ **Requirement 5.1**: YouTube service fetches trending videos
✅ **Requirement 5.6**: Gemini key rotation prevents rate limits
✅ **Requirement 6.1**: AI service generates video titles with SEO scores
✅ **Requirement 10.2**: AI services use configured API keys
✅ **Requirement 10.3**: ImageKit uses configured credentials
✅ **Requirement 10.4**: YouTube API uses configured key

## Next Steps

**Task 6**: Implement thumbnail generation feature
- Create thumbnail generation Celery task
- Create thumbnail generation API endpoint
- Create thumbnail history API endpoint
- Integrate AI Service and ImageKit Service

## Notes

- All services are singleton instances for efficiency
- Thread-safe implementation for concurrent requests
- Comprehensive error handling and logging
- Fallback mechanisms for AI services
- Ready for integration in Celery tasks
- All external API integrations complete

## Task Status

**Task 5: Implement service layer for external integrations** - ✅ COMPLETE

All sub-tasks completed:
- 5.1 Create AI Service class ✅
- 5.2 Create ImageKit Service class ✅
- 5.3 Create YouTube Service class ✅
- 5.4 Create Gemini key rotation utility ✅
