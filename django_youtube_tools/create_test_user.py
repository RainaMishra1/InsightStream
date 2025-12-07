"""
Script to create a test user for development.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User

# Create test user
email = 'test@example.com'
username = 'testuser'
password = 'testpass123'

if not User.objects.filter(email=email).exists():
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    print(f'✅ Test user created successfully!')
    print(f'Email: {email}')
    print(f'Password: {password}')
else:
    print(f'⚠️  User with email {email} already exists.')
