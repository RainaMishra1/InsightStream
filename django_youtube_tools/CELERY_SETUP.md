# Celery Setup Guide

## Overview

Celery is configured for handling background tasks like AI thumbnail generation, content generation, and other long-running operations.

## Architecture

```
Django App → Celery Task → Redis Broker → Celery Worker → Task Execution
                                ↓
                          Result Backend (Redis)
```

## Prerequisites

### 1. Install Redis

**Windows:**
- Download Redis from: https://github.com/microsoftarchive/redis/releases
- Or use WSL: `sudo apt-get install redis-server`
- Or use Docker: `docker run -d -p 6379:6379 redis`

**Mac:**
```bash
brew install redis
brew services start redis
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

### 2. Install Python Dependencies

```bash
pip install celery redis
```

## Configuration

### Environment Variables

Add to your `.env` file:

```env
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Celery Settings (already configured)

- **Broker**: Redis (localhost:6379/0)
- **Result Backend**: Redis (localhost:6379/0)
- **Serializer**: JSON
- **Task Time Limit**: 30 minutes
- **Soft Time Limit**: 25 minutes
- **Retry**: Automatic with exponential backoff

## Running Celery

### Start Redis Server

```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# If not running, start it
redis-server
```

### Start Celery Worker

**Development (single worker):**
```bash
celery -A config worker -l info
```

**Development (with auto-reload on code changes):**
```bash
celery -A config worker -l info --pool=solo
```

**Production (multiple workers):**
```bash
celery -A config worker -l info --concurrency=4
```

### Monitor Celery

**Flower (Web-based monitoring):**
```bash
pip install flower
celery -A config flower
# Visit: http://localhost:5555
```

## Task Base Classes

### BaseTaskWithRetry

Base class for all tasks with automatic retry logic.

```python
from celery import shared_task
from services.celery_tasks import BaseTaskWithRetry

@shared_task(base=BaseTaskWithRetry, bind=True)
def my_task(self, arg1, arg2):
    # Task implementation
    return result
```

**Features:**
- Automatic retry on failure (max 3 retries)
- Exponential backoff
- Error logging with stack traces
- Success/failure/retry handlers

### AITaskWithRetry

Specialized for AI service calls (longer timeouts, more retries).

```python
from celery import shared_task
from services.celery_tasks import AITaskWithRetry

@shared_task(base=AITaskWithRetry, bind=True)
def ai_generation_task(self, prompt):
    # AI task implementation
    return result
```

**Features:**
- 10-minute time limit
- 5 retry attempts
- Optimized for AI service flakiness

### ImageProcessingTask

Specialized for image processing operations.

```python
from celery import shared_task
from services.celery_tasks import ImageProcessingTask

@shared_task(base=ImageProcessingTask, bind=True)
def process_image_task(self, image_data):
    # Image processing implementation
    return result
```

**Features:**
- 5-minute time limit
- 3 retry attempts
- Optimized for image operations

## Testing Celery

### Test Command

```bash
python manage.py test_celery
```

This will:
1. Queue a test task
2. Show the task ID
3. Try to get the result (if worker is running)

### Manual Test

```python
# In Django shell
python manage.py shell

from accounts.tasks import test_celery_task

# Queue task
result = test_celery_task.delay('Hello Celery!')

# Get task ID
print(result.id)

# Check status
print(result.status)  # PENDING, STARTED, SUCCESS, FAILURE

# Get result (blocks until complete)
print(result.get(timeout=10))
```

## Task Examples

### Simple Task

```python
from celery import shared_task

@shared_task
def add(x, y):
    return x + y

# Usage
result = add.delay(4, 6)
print(result.get())  # 10
```

### Task with Retry

```python
from celery import shared_task
from services.celery_tasks import BaseTaskWithRetry

@shared_task(base=BaseTaskWithRetry, bind=True)
def risky_task(self, url):
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        # Will automatically retry with exponential backoff
        raise
```

### Task with Custom Retry Logic

```python
from celery import shared_task

@shared_task(bind=True, max_retries=5)
def custom_retry_task(self, data):
    try:
        # Task logic
        return process_data(data)
    except SpecificError as exc:
        # Retry after 60 seconds
        raise self.retry(exc=exc, countdown=60)
```

## Monitoring Tasks

### Check Task Status

```python
from celery.result import AsyncResult

task_id = 'abc-123-def-456'
result = AsyncResult(task_id)

print(result.status)  # PENDING, STARTED, SUCCESS, FAILURE, RETRY
print(result.info)    # Task result or exception info
```

### List Active Tasks

```bash
celery -A config inspect active
```

### List Registered Tasks

```bash
celery -A config inspect registered
```

### Purge All Tasks

```bash
celery -A config purge
```

## Common Issues

### Issue: "Connection refused" error

**Solution:** Make sure Redis is running
```bash
redis-cli ping
# Should return: PONG
```

### Issue: Tasks not executing

**Solution:** Make sure Celery worker is running
```bash
celery -A config worker -l info
```

### Issue: Tasks timing out

**Solution:** Increase time limits in settings
```python
CELERY_TASK_TIME_LIMIT = 60 * 60  # 1 hour
```

### Issue: Too many retries

**Solution:** Adjust retry settings in task
```python
@shared_task(max_retries=10, default_retry_delay=60)
def my_task():
    pass
```

## Production Deployment

### Using Supervisor (Linux)

```ini
[program:celery]
command=/path/to/venv/bin/celery -A config worker -l info
directory=/path/to/project
user=www-data
numprocs=1
stdout_logfile=/var/log/celery/worker.log
stderr_logfile=/var/log/celery/worker.log
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=600
```

### Using systemd (Linux)

```ini
[Unit]
Description=Celery Worker
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/path/to/project
ExecStart=/path/to/venv/bin/celery -A config worker -l info
Restart=always

[Install]
WantedBy=multi-user.target
```

### Using Docker

```dockerfile
# Celery worker container
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["celery", "-A", "config", "worker", "-l", "info"]
```

## Next Steps

- Task 6: Implement thumbnail generation tasks
- Task 9: Implement content generation tasks
- Add task monitoring with Flower
- Set up task scheduling with Celery Beat (if needed)

## Resources

- [Celery Documentation](https://docs.celeryproject.org/)
- [Django Celery Integration](https://docs.celeryproject.org/en/stable/django/)
- [Redis Documentation](https://redis.io/documentation)
