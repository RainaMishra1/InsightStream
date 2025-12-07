"""
Management command to test Celery configuration.
"""
from django.core.management.base import BaseCommand
from accounts.tasks import test_celery_task


class Command(BaseCommand):
    help = 'Test Celery task execution'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing Celery...'))
        
        # Queue the test task
        result = test_celery_task.delay('Testing Celery from management command!')
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Task queued successfully!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Task ID: {result.id}')
        )
        self.stdout.write(
            self.style.WARNING('\nTo see the task execute, make sure:')
        )
        self.stdout.write('1. Redis is running: redis-server')
        self.stdout.write('2. Celery worker is running: celery -A config worker -l info')
        
        # Try to get result (will timeout if worker not running)
        try:
            task_result = result.get(timeout=5)
            self.stdout.write(
                self.style.SUCCESS(f'\n✅ Task completed: {task_result}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'\n⚠️  Could not get task result: {e}')
            )
            self.stdout.write(
                self.style.WARNING('This is normal if Celery worker is not running.')
            )
