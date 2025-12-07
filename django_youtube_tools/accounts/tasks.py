"""
Celery tasks for accounts app.
"""
from celery import shared_task
from services.celery_tasks import BaseTaskWithRetry
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(base=BaseTaskWithRetry, bind=True)
def test_celery_task(self, message='Hello from Celery!'):
    """
    Test task to verify Celery is working correctly.
    
    Args:
        message: Test message to log
    
    Returns:
        dict: Success status and message
    """
    logger.info(f'Test task executing: {message}')
    return {
        'success': True,
        'message': message,
        'task_id': self.request.id
    }


@shared_task(base=BaseTaskWithRetry, bind=True)
def send_welcome_email(self, user_email):
    """
    Send welcome email to new user (placeholder for future implementation).
    
    Args:
        user_email: Email address of the new user
    
    Returns:
        dict: Success status
    """
    logger.info(f'Sending welcome email to {user_email}')
    
    # TODO: Implement actual email sending in future
    # For now, just log the action
    
    return {
        'success': True,
        'email': user_email,
        'message': 'Welcome email sent (placeholder)'
    }
