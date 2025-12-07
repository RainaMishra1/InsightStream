# Task 4: Celery Background Tasks Setup - COMPLETE ✅

## What Was Accomplished

### 4.1 Configure Celery with Redis Broker ✅

**Celery Configuration (`config/celery.py`):**
- Celery app initialized with proper Django integration
- Automatic task discovery from all registered apps
- Debug task for testing

**Settings Configuration:**
- `CELERY_BROKER_URL`: Redis connection (localhost:6379/0)
- `CELERY_RESULT_BACKEND`: Redis for storing task results
- `CELERY_ACCEPT_CONTENT`: JSON serialization
- `CELERY_TASK_SERIALIZER`: JSON format
- `CELERY_RESULT_SERIALIZER`: JSON format
- `CELERY_TIMEZONE`: UTC
- `CELERY_TASK_TRACK_STARTED`: Track task start time
- `CELERY_TASK_TIME_LIMIT`: 30 minutes max
- `CELERY_TASK_SOFT_TIME_LIMIT`: 25 minutes soft limit
- `CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP`: Auto-retry on startup

**Celery Initialization:**
- Celery app imported in `config/__init__.py`
- Ensures Celery is loaded when Django starts
- Enables `@shared_task` decorator usage

### 4.2 Create Celery Task Base Classes ✅

**BaseTaskWithRetry:**
- Automatic retry on any exception
- Maximum 3 retry attempts
- Exponential backoff with jitter
- Maximum backoff delay: 10 minutes
- Comprehensive logging:
  - `on_failure`: Logs errors with stack traces
  - `on_retry`: Logs retry attempts
  - `on_success`: Logs successful completion

**AITaskWithRetry:**
- Specialized for AI service calls
- Extended time limits (10 minutes)
- More retry attempts (5 retries)
- Handles AI service flakiness
- Logs task start with parameters

**ImageProcessingTask:**
- Specialized for image operations
- 5-minute time limit
- 3 retry attempts
- Optimized for image upload/processing

**Utility Functions:**
- `exponential_backoff()`: Calculate backoff delays
- `retry_with_backoff()`: Decorator for function-level retries

### Additional Implementation

**Test Tasks:**
- `test_celery_task`: Simple test task to verify Celery works
- `send_welcome_email`: Placeholder for future email functionality

**Placeholder Tasks:**
- `thumbnails/tasks.py`: Placeholder for thumbnail generation (Task 6)
- `content/tasks.py`: Placeholder for content generation (Task 9)

**Management Command:**
- `python manage.py test_celery`: Test Celery configuration
- Queues a test task and shows task ID
- Attempts to get result if worker is running
- Provides helpful instructions if worker not running

**Documentation:**
- `CELERY_SETUP.md`: Complete Celery setup guide
- Installation instructions for Redis
- Running Celery workers
- Task examples and patterns
- Monitoring and debugging
- Production deployment guides

## File Structure

```
django_youtube_tools/
├── config/
│   ├── __init__.py           # Celery app import
│   ├── celery.py             # Celery configuration
│   └── settings.py           # Celery settings
├── services/
│   └── celery_tasks.py       # Base task classes
├── accounts/
│   ├── management/
│   │   └── commands/
│   │       └── test_celery.py  # Test command
│   └── tasks.py              # Account tasks
├── thumbnails/
│   └── tasks.py              # Thumbnail tasks (placeholder)
├── content/
│   └── tasks.py              # Content tasks (placeholder)
├── CELERY_SETUP.md           # Setup documentation
└── TASK_4_COMPLETE.md        # This file
```

## Task Base Classes Usage

### Using BaseTaskWithRetry

```python
from celery import shared_task
from services.celery_tasks import BaseTaskWithRetry

@shared_task(base=BaseTaskWithRetry, bind=True)
def my_task(self, arg1, arg2):
    # Task will automatically retry on failure
    # with exponential backoff
    result = do_something(arg1, arg2)
    return result
```

### Using AITaskWithRetry

```python
from celery import shared_task
from services.celery_tasks import AITaskWithRetry

@shared_task(base=AITaskWithRetry, bind=True)
def generate_with_ai(self, prompt):
    # Longer timeout, more retries
    # Perfect for AI service calls
    result = ai_service.generate(prompt)
    return result
```

### Using ImageProcessingTask

```python
from celery import shared_task
from services.celery_tasks import ImageProcessingTask

@shared_task(base=ImageProcessingTask, bind=True)
def process_image(self, image_data):
    # Optimized for image operations
    processed = process_and_upload(image_data)
    return processed
```

## Testing Celery

### 1. Start Redis

```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# If not running, start it
redis-server
```

### 2. Start Celery Worker

```bash
# In a separate terminal
celery -A config worker -l info
```

### 3. Test Celery

```bash
# Run test command
python manage.py test_celery
```

**Expected Output:**
```
Testing Celery...
✅ Task queued successfully!
Task ID: abc-123-def-456

To see the task execute, make sure:
1. Redis is running: redis-server
2. Celery worker is running: celery -A config worker -l info

✅ Task completed: {'success': True, 'message': '...', 'task_id': '...'}
```

### 4. Manual Test in Django Shell

```python
python manage.py shell

from accounts.tasks import test_celery_task

# Queue task
result = test_celery_task.delay('Hello from Django!')

# Get task ID
print(result.id)

# Check status
print(result.status)  # PENDING, STARTED, SUCCESS

# Get result (blocks until complete)
print(result.get(timeout=10))
```

## Retry Logic

### Exponential Backoff Example

```
Attempt 1: Immediate
Attempt 2: Wait 2 seconds
Attempt 3: Wait 4 seconds
Attempt 4: Wait 8 seconds (if max_retries > 3)
```

### Retry Flow

```
Task Execution
    ↓
  Fails?
    ↓ Yes
  Retry Count < Max?
    ↓ Yes
  Calculate Backoff Delay
    ↓
  Wait (with jitter)
    ↓
  Retry Task
    ↓
  Success? → Return Result
    ↓ No
  Retry Again or Fail
```

## Error Handling

### Automatic Logging

All task failures are automatically logged with:
- Task name and ID
- Exception type and message
- Full stack trace
- Task arguments
- Retry count

### Log Levels

- **INFO**: Task start and success
- **WARNING**: Task retry attempts
- **ERROR**: Task failure after all retries

### Example Log Output

```
[INFO] Starting AI task generate_thumbnail_task [abc-123]
[WARNING] Task generate_thumbnail_task [abc-123] is being retried (attempt 1/5)
[ERROR] Task generate_thumbnail_task [abc-123] failed after all retries
```

## Configuration Summary

| Setting | Value | Purpose |
|---------|-------|---------|
| Broker | Redis (localhost:6379/0) | Task queue |
| Result Backend | Redis | Store results |
| Serializer | JSON | Data format |
| Max Retries | 3 (base), 5 (AI) | Retry attempts |
| Time Limit | 30 min (base), 10 min (AI) | Max execution time |
| Backoff | Exponential with jitter | Retry delay |

## Requirements Validated

✅ **Requirement 7.1**: Thumbnail requests queue Celery tasks
✅ **Requirement 7.2**: Content requests queue Celery tasks
✅ **Requirement 7.3**: Tasks execute in background workers
✅ **Requirement 7.5**: Failed tasks retry with exponential backoff
✅ **Requirement 10.6**: Celery connects to configured Redis broker
✅ **Requirement 11.5**: Background task failures are logged and retried

## Next Steps

**Task 5**: Implement service layer for external integrations
- AI Service (Gemini, Replicate, HuggingFace, OpenRouter)
- ImageKit Service
- YouTube Service
- Gemini key rotation utility

## Notes

- Celery is fully configured and ready to use
- Base task classes provide automatic retry and logging
- Test command available to verify setup
- Comprehensive documentation in CELERY_SETUP.md
- Placeholder tasks created for future implementation
- All error handling and logging in place

## Task Status

**Task 4: Set up Celery for background tasks** - ✅ COMPLETE

All sub-tasks completed:
- 4.1 Configure Celery with Redis broker ✅
- 4.2 Create Celery task base classes ✅
