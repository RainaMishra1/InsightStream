"""
Base Celery task classes with retry logic and error handling.
"""
from celery import Task
from celery.utils.log import get_task_logger
import time

logger = get_task_logger(__name__)


class BaseTaskWithRetry(Task):
    """
    Base task class with automatic retry on failure.
    Implements exponential backoff strategy.
    """
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 3}
    retry_backoff = True
    retry_backoff_max = 600  # 10 minutes
    retry_jitter = True
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        Error handler called when task fails after all retries.
        Logs the error with full stack trace.
        """
        logger.error(
            f'Task {self.name} [{task_id}] failed after all retries',
            exc_info=exc,
            extra={
                'task_id': task_id,
                'args': args,
                'kwargs': kwargs,
                'exception': str(exc),
                'traceback': str(einfo)
            }
        )
        super().on_failure(exc, task_id, args, kwargs, einfo)
    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """
        Handler called when task is retried.
        Logs retry attempt with exception details.
        """
        logger.warning(
            f'Task {self.name} [{task_id}] is being retried',
            extra={
                'task_id': task_id,
                'exception': str(exc),
                'retry_count': self.request.retries
            }
        )
        super().on_retry(exc, task_id, args, kwargs, einfo)
    
    def on_success(self, retval, task_id, args, kwargs):
        """
        Handler called when task succeeds.
        Logs successful completion.
        """
        logger.info(
            f'Task {self.name} [{task_id}] completed successfully',
            extra={
                'task_id': task_id,
                'result': retval
            }
        )
        super().on_success(retval, task_id, args, kwargs)


class AITaskWithRetry(BaseTaskWithRetry):
    """
    Specialized task class for AI service calls.
    Handles AI-specific errors and implements appropriate retry strategy.
    """
    # AI services can be slow, so increase time limits
    time_limit = 600  # 10 minutes
    soft_time_limit = 540  # 9 minutes
    
    # Retry more times for AI tasks as they can be flaky
    retry_kwargs = {'max_retries': 5}
    
    def before_start(self, task_id, args, kwargs):
        """
        Handler called before task execution.
        Logs task start with parameters.
        """
        logger.info(
            f'Starting AI task {self.name} [{task_id}]',
            extra={
                'task_id': task_id,
                'args': args,
                'kwargs': kwargs
            }
        )
        super().before_start(task_id, args, kwargs)


class ImageProcessingTask(BaseTaskWithRetry):
    """
    Specialized task class for image processing operations.
    Handles image upload and processing errors.
    """
    time_limit = 300  # 5 minutes
    soft_time_limit = 270  # 4.5 minutes
    
    retry_kwargs = {'max_retries': 3}


def exponential_backoff(attempt, base_delay=2, max_delay=60):
    """
    Calculate exponential backoff delay.
    
    Args:
        attempt: Current retry attempt number (0-indexed)
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
    
    Returns:
        Delay in seconds
    """
    delay = min(base_delay * (2 ** attempt), max_delay)
    return delay


def retry_with_backoff(func, max_retries=3, base_delay=2):
    """
    Decorator to retry a function with exponential backoff.
    
    Usage:
        @retry_with_backoff(max_retries=3, base_delay=2)
        def my_function():
            # function code
    """
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    # Last attempt, raise the exception
                    logger.error(
                        f'Function {func.__name__} failed after {max_retries} attempts',
                        exc_info=e
                    )
                    raise
                
                # Calculate backoff delay
                delay = exponential_backoff(attempt, base_delay)
                logger.warning(
                    f'Function {func.__name__} failed (attempt {attempt + 1}/{max_retries}), '
                    f'retrying in {delay}s',
                    extra={'exception': str(e)}
                )
                time.sleep(delay)
    
    return wrapper
