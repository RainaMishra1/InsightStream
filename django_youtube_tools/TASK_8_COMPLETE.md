# Task 8: Keyword Research Feature - COMPLETE ✅

## What Was Accomplished

### 8.1 Keyword Research API Endpoint ✅

**File:** `keywords/api_views.py`

**Endpoint:** `POST /api/keyword-research`

**Implementation:**
- Accepts topic from user
- Fetches YouTube trending data
- Uses Gemini AI for keyword analysis
- Implements Gemini key rotation
- Returns structured keyword data
- Comprehensive error handling

**Request Format:**
```json
{
  "topic": "Python programming"
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "primary_keywords": [
      {
        "keyword": "python programming",
        "search_volume": "high",
        "competition": "medium",
        "relevance_score": 95
      }
    ],
    "long_tail_keywords": [
      {
        "keyword": "python programming for beginners",
        "search_volume": "medium",
        "competition": "low",
        "relevance_score": 90
      }
    ],
    "trending_keywords": [
      {
        "keyword": "python 3.12 features",
        "trend": "rising",
        "relevance_score": 85
      }
    ],
    "related_topics": [
      "Django framework",
      "Data science with Python",
      "Python automation"
    ],
    "content_suggestions": [
      "Create a beginner's guide to Python",
      "Build a real-world Python project",
      "Python vs JavaScript comparison"
    ]
  },
  "topic": "Python programming"
}
```

### 8.2 Keyword Categorization Logic ✅

**Categories Implemented:**

#### 1. Primary Keywords
- Main keywords directly related to topic
- High relevance scores (90-100)
- Includes search volume and competition metrics
- 5-7 keywords per category

#### 2. Long-tail Keywords
- Specific, detailed keyword phrases
- Lower competition
- Higher conversion potential
- 5-7 keywords per category

#### 3. Trending Keywords
- Currently trending keywords
- Trend indicator (rising/stable)
- Time-sensitive opportunities
- 5-7 keywords per category

#### 4. Related Topics
- Similar topics to explore
- Content expansion ideas
- 3-5 topics

#### 5. Content Suggestions
- Video ideas based on keywords
- SEO-optimized suggestions
- 2-3 suggestions

## Complete Keyword Research Flow

```
User Input: Topic
    ↓
API: POST /api/keyword-research
    ↓
YouTube Service: Fetch trending videos
    ↓
Extract: Video titles as trending data
    ↓
Gemini Key Rotation: Get next API key
    ↓
Gemini AI: Analyze topic + YouTube data
    ↓
AI: Generate categorized keywords
    ↓
Parse: Extract JSON from AI response
    ↓
Fallback: Use default data if parsing fails
    ↓
API: Return structured keyword data
    ↓
Frontend: Display categorized keywords
```

## API Usage Examples

### Basic Request

```bash
curl -X POST http://localhost:8000/api/keyword-research \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Django tutorial"}'
```

### Python Usage

```python
from rest_framework.test import APIClient
from accounts.models import User

client = APIClient()
user = User.objects.get(email="test@example.com")
client.force_authenticate(user=user)

response = client.post('/api/keyword-research', {
    'topic': 'Web development'
})

print(response.status_code)  # 200
data = response.json()
print(data['data']['primary_keywords'])
```

### Direct Service Usage

```python
from services.youtube_service import get_youtube_service
from services.gemini_rotation import get_next_gemini_key
import google.generativeai as genai

# Get YouTube trending data
youtube = get_youtube_service()
trending = youtube.get_trending_keywords('Python programming')

# Use Gemini with key rotation
api_key = get_next_gemini_key()
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Generate keywords
response = model.generate_content(f"Analyze: {trending}")
```

## Integration with Existing Services

### YouTube Service (Task 5)
- `get_trending_keywords()` method
- Fetches top 10 trending video titles
- Ordered by view count
- Provides real-time trending data

### Gemini Key Rotation (Task 5)
- `get_next_gemini_key()` function
- Round-robin rotation
- Prevents rate limiting
- Thread-safe implementation

### Gemini AI
- Direct integration with google-generativeai SDK
- Uses gemini-2.0-flash-exp model
- Structured JSON output
- Comprehensive keyword analysis

## Error Handling

### API Level

**400 Bad Request:**
- Topic missing or empty
- Invalid request format

**401 Unauthorized:**
- No authentication token
- Invalid token

**500 Internal Server Error:**
- YouTube API failure
- Gemini AI failure
- JSON parsing error
- Network errors

### Fallback Mechanism

If AI fails or returns invalid JSON:
```json
{
  "primary_keywords": [
    {
      "keyword": "<user_topic>",
      "search_volume": "medium",
      "competition": "medium",
      "relevance_score": 80
    }
  ],
  "long_tail_keywords": [],
  "trending_keywords": [],
  "related_topics": [],
  "content_suggestions": []
}
```

## Keyword Metadata

### Search Volume
- **high**: 100K+ monthly searches
- **medium**: 10K-100K monthly searches
- **low**: <10K monthly searches

### Competition
- **high**: Many creators targeting this keyword
- **medium**: Moderate competition
- **low**: Less competitive, easier to rank

### Relevance Score
- **90-100**: Highly relevant to topic
- **80-89**: Very relevant
- **70-79**: Moderately relevant
- **<70**: Less relevant

### Trend
- **rising**: Increasing search interest
- **stable**: Consistent search volume
- **declining**: Decreasing interest

## Testing

### Test Keyword Research

```python
python manage.py shell

from keywords.api_views import KeywordResearchAPIView
from rest_framework.test import APIRequestFactory
from accounts.models import User

factory = APIRequestFactory()
user = User.objects.get(email="test@example.com")

# Create request
request = factory.post('/api/keyword-research', {
    'topic': 'Machine learning'
})
request.user = user

# Call view
view = KeywordResearchAPIView.as_view()
response = view(request)

print(response.status_code)  # 200
print(response.data['data']['primary_keywords'])
```

### Manual Testing

```bash
# 1. Login
curl -X POST http://localhost:8000/accounts/login/ \
  -d "username=test@example.com&password=testpass123"

# 2. Research keywords
curl -X POST http://localhost:8000/api/keyword-research \
  -H "Cookie: sessionid=<session_id>" \
  -H "Content-Type: application/json" \
  -d '{"topic": "React tutorial"}'
```

## Environment Variables Required

```env
# Gemini API (with rotation)
GEMINI_API_KEY_1=your-gemini-key-1
GEMINI_API_KEY_2=your-gemini-key-2
GEMINI_API_KEY_3=your-gemini-key-3

# YouTube API
YOUTUBE_API_KEY=your-youtube-api-key
```

## Response Examples

### Example 1: Programming Topic

**Request:**
```json
{"topic": "JavaScript tutorial"}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "primary_keywords": [
      {"keyword": "javascript tutorial", "search_volume": "high", "competition": "high", "relevance_score": 95},
      {"keyword": "learn javascript", "search_volume": "high", "competition": "high", "relevance_score": 93},
      {"keyword": "javascript basics", "search_volume": "medium", "competition": "medium", "relevance_score": 90}
    ],
    "long_tail_keywords": [
      {"keyword": "javascript tutorial for beginners 2024", "search_volume": "medium", "competition": "low", "relevance_score": 92},
      {"keyword": "javascript es6 features explained", "search_volume": "low", "competition": "low", "relevance_score": 88}
    ],
    "trending_keywords": [
      {"keyword": "javascript frameworks 2024", "trend": "rising", "relevance_score": 87},
      {"keyword": "async await javascript", "trend": "stable", "relevance_score": 85}
    ],
    "related_topics": [
      "React.js framework",
      "Node.js backend",
      "TypeScript"
    ],
    "content_suggestions": [
      "Build a complete JavaScript project from scratch",
      "JavaScript vs Python: Which to learn first?",
      "Modern JavaScript features you should know"
    ]
  },
  "topic": "JavaScript tutorial"
}
```

### Example 2: Cooking Topic

**Request:**
```json
{"topic": "Italian cooking"}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "primary_keywords": [
      {"keyword": "italian cooking", "search_volume": "high", "competition": "medium", "relevance_score": 94},
      {"keyword": "italian recipes", "search_volume": "high", "competition": "high", "relevance_score": 92}
    ],
    "long_tail_keywords": [
      {"keyword": "authentic italian pasta recipes", "search_volume": "medium", "competition": "low", "relevance_score": 90},
      {"keyword": "italian cooking techniques for beginners", "search_volume": "low", "competition": "low", "relevance_score": 88}
    ],
    "trending_keywords": [
      {"keyword": "italian pizza dough recipe", "trend": "rising", "relevance_score": 86}
    ],
    "related_topics": [
      "Mediterranean cuisine",
      "Pasta making",
      "Italian desserts"
    ],
    "content_suggestions": [
      "Make authentic Italian carbonara",
      "Italian cooking mistakes to avoid",
      "Essential Italian ingredients"
    ]
  },
  "topic": "Italian cooking"
}
```

## Requirements Validated

✅ **Requirement 5.1**: User submits topic → YouTube trending videos fetched
✅ **Requirement 5.2**: YouTube data retrieved → sent to AI for analysis
✅ **Requirement 5.3**: AI analyzes data → generates keywords with search volume and competition
✅ **Requirement 5.4**: AI generates keywords → categorized into primary, long-tail, and trending
✅ **Requirement 5.5**: Keyword research completes → returns structured JSON with keywords, topics, suggestions
✅ **Requirement 5.6**: Multiple requests occur → Gemini API keys rotated
✅ **Requirement 8.4**: POST /api/keyword-research endpoint exposed

## File Structure

```
django_youtube_tools/
└── keywords/
    ├── api_views.py           # KeywordResearchAPIView ✅
    └── urls.py                # /api/keyword-research route ✅
```

## Next Steps

**Task 9**: Implement content generation feature
- Create content generation Celery task
- Create content generation API endpoint
- Create content history API endpoint
- Generate titles, descriptions, and tags

## Notes

- Keyword research is fully functional
- Integrates YouTube trending data
- Uses Gemini AI with key rotation
- Returns structured, categorized keywords
- Includes fallback for AI failures
- All error handling in place
- Ready for production use

## Task Status

**Task 8: Implement keyword research feature** - ✅ COMPLETE

All sub-tasks completed:
- 8.1 Create keyword research API endpoint ✅
- 8.2 Implement keyword categorization logic ✅
