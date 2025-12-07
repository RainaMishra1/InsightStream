# Environment Variables Setup Guide

This guide explains how to configure all environment variables for the Django YouTube Tools application.

## Quick Start

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Generate SECRET_KEY:**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **Fill in all REQUIRED values in `.env`**

4. **Start the application** (see Running the Application section)

## Required Environment Variables

### Django Settings

#### SECRET_KEY (REQUIRED)
- **Purpose:** Cryptographic signing for sessions, cookies, CSRF tokens
- **How to get:** Generate with Python command above
- **Example:** `django-insecure-abc123...`
- **Production:** MUST be different from development, keep secret

#### DEBUG (REQUIRED)
- **Purpose:** Enable/disable debug mode
- **Values:** `True` or `False`
- **Development:** `True`
- **Production:** `False` (CRITICAL for security)

#### ALLOWED_HOSTS (REQUIRED)
- **Purpose:** Allowed hostnames for the application
- **Format:** Comma-separated list
- **Development:** `localhost,127.0.0.1`
- **Production:** `yourdomain.com,www.yourdomain.com`

### Database Configuration

#### DATABASE_URL (OPTIONAL)
- **Purpose:** PostgreSQL database connection
- **Format:** `postgresql://user:password@host:port/database`
- **Default:** Uses SQLite if not provided
- **Development:** Can use SQLite (no DATABASE_URL needed)
- **Production:** MUST use PostgreSQL
- **Example:** `postgresql://postgres:password@localhost:5432/youtube_tools`

### Redis & Celery

#### CELERY_BROKER_URL (REQUIRED)
- **Purpose:** Message broker for Celery tasks
- **Default:** `redis://localhost:6379/0`
- **How to get:** Install and run Redis
- **Installation:**
  - Windows: Download from https://redis.io/download
  - Mac: `brew install redis`
  - Linux: `sudo apt-get install redis-server`
- **Start Redis:** `redis-server`

#### CELERY_RESULT_BACKEND (REQUIRED)
- **Purpose:** Store Celery task results
- **Default:** `redis://localhost:6379/0`
- **Same as:** CELERY_BROKER_URL (usually)

### AI Service API Keys

#### GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3 (REQUIRED)
- **Purpose:** Google Gemini AI for keyword research
- **How to get:**
  1. Visit https://makersuite.google.com/app/apikey
  2. Sign in with Google account
  3. Create API key
  4. Copy key to .env
- **Why 3 keys:** Rotation to avoid rate limits
- **Can use same key:** Yes, but not recommended
- **Free tier:** Available

#### REPLICATE_API_TOKEN (REQUIRED)
- **Purpose:** AI thumbnail generation with FLUX model
- **How to get:**
  1. Visit https://replicate.com
  2. Sign up for account
  3. Go to https://replicate.com/account/api-tokens
  4. Create token
  5. Copy to .env
- **Pricing:** Pay per use
- **Free tier:** Limited credits

#### OPENROUTER_API_KEY (REQUIRED)
- **Purpose:** AI content generation (titles, descriptions, tags)
- **How to get:**
  1. Visit https://openrouter.ai
  2. Sign up for account
  3. Go to https://openrouter.ai/keys
  4. Create API key
  5. Copy to .env
- **Pricing:** Pay per use
- **Free tier:** Limited credits

#### HF_API_TOKEN (OPTIONAL)
- **Purpose:** HuggingFace models (alternative AI)
- **How to get:**
  1. Visit https://huggingface.co
  2. Sign up for account
  3. Go to https://huggingface.co/settings/tokens
  4. Create token
  5. Copy to .env
- **Currently:** Not actively used, but available for future features

### ImageKit Configuration

#### IMAGEKIT_PUBLIC_KEY (REQUIRED)
- **Purpose:** Image CDN for thumbnail storage
- **How to get:**
  1. Visit https://imagekit.io
  2. Sign up for account
  3. Go to https://imagekit.io/dashboard/developer/api-keys
  4. Copy public key
- **Free tier:** 20GB storage, 20GB bandwidth

#### IMAGEKIT_PRIVATE_KEY (REQUIRED)
- **Purpose:** Server-side image uploads
- **How to get:** Same dashboard as public key
- **Security:** Keep private, never expose in frontend

#### IMAGEKIT_URL_ENDPOINT (REQUIRED)
- **Purpose:** Base URL for ImageKit CDN
- **Format:** `https://ik.imagekit.io/your_imagekit_id`
- **How to get:** Same dashboard as keys
- **Example:** `https://ik.imagekit.io/abc123xyz`

### YouTube API

#### YOUTUBE_API_KEY (REQUIRED)
- **Purpose:** YouTube Data API v3 for video search
- **How to get:**
  1. Visit https://console.cloud.google.com
  2. Create new project or select existing
  3. Enable "YouTube Data API v3"
  4. Go to Credentials
  5. Create API key
  6. Copy to .env
- **Free tier:** 10,000 quota units per day
- **Quota:** Each search costs ~100 units

### CORS Configuration

#### CORS_ALLOWED_ORIGINS (OPTIONAL)
- **Purpose:** Allow cross-origin requests
- **Format:** Comma-separated URLs
- **Development:** `http://localhost:3000`
- **Production:** `https://yourdomain.com`
- **Default:** `http://localhost:3000`

## Environment Variable Validation

The application validates required environment variables on startup. Missing variables will cause errors.

### Check Configuration
```bash
python manage.py check
```

### Test API Keys
```bash
# Test Gemini
python manage.py shell
>>> from services.ai_service import get_ai_service
>>> ai = get_ai_service()
>>> # Should not raise errors

# Test ImageKit
>>> from services.imagekit_service import get_imagekit_service
>>> ik = get_imagekit_service()
>>> # Should not raise errors

# Test YouTube
>>> from services.youtube_service import get_youtube_service
>>> yt = get_youtube_service()
>>> # Should not raise errors
```

## Running the Application

### Development

1. **Start Redis:**
   ```bash
   redis-server
   ```

2. **Start Celery Worker (new terminal):**
   ```bash
   celery -A config worker -l info
   ```

3. **Start Django (new terminal):**
   ```bash
   python manage.py runserver
   ```

4. **Visit:** http://localhost:8000

### Production

1. **Set environment variables:**
   - Use environment variables directly (not .env file)
   - Or use secure secret management service

2. **Configure web server:**
   - Use Gunicorn or uWSGI
   - Configure Nginx or Apache

3. **Start Celery:**
   - Use supervisor or systemd
   - Configure multiple workers

4. **Monitor:**
   - Set up logging
   - Configure error tracking
   - Monitor API usage

## Security Best Practices

### Development
- ✅ Use .env file
- ✅ Add .env to .gitignore
- ✅ Use test API keys
- ✅ DEBUG=True is okay

### Production
- ✅ Use environment variables (not .env file)
- ✅ Generate new SECRET_KEY
- ✅ Set DEBUG=False
- ✅ Use production API keys
- ✅ Rotate keys regularly
- ✅ Use HTTPS
- ✅ Configure proper ALLOWED_HOSTS
- ✅ Use PostgreSQL (not SQLite)
- ✅ Use production Redis instance
- ✅ Enable monitoring and logging
- ✅ Set up backups

## Troubleshooting

### "SECRET_KEY not set"
- Generate new key with Python command
- Add to .env file

### "Redis connection refused"
- Start Redis: `redis-server`
- Check Redis is running: `redis-cli ping`

### "API key invalid"
- Verify key is correct
- Check for extra spaces
- Ensure key has proper permissions

### "Database connection failed"
- Check DATABASE_URL format
- Verify PostgreSQL is running
- Check credentials

### "CORS errors"
- Add frontend URL to CORS_ALLOWED_ORIGINS
- Restart Django server

## API Key Costs

### Free Tiers
- **Gemini:** Free tier available
- **YouTube:** 10,000 quota units/day
- **ImageKit:** 20GB storage, 20GB bandwidth

### Paid Services
- **Replicate:** ~$0.01-0.10 per image
- **OpenRouter:** ~$0.001-0.01 per request

### Cost Optimization
- Use Gemini key rotation
- Cache YouTube results
- Optimize image sizes
- Monitor usage regularly

## Support

For issues with:
- **Django:** Check Django logs
- **Celery:** Check Celery worker logs
- **API Keys:** Contact service provider
- **Application:** Check application logs in `logs/django.log`

## Additional Resources

- [Django Settings Documentation](https://docs.djangoproject.com/en/5.0/ref/settings/)
- [Celery Configuration](https://docs.celeryproject.org/en/stable/userguide/configuration.html)
- [Redis Documentation](https://redis.io/documentation)
- [ImageKit Documentation](https://docs.imagekit.io/)
- [YouTube API Documentation](https://developers.google.com/youtube/v3)
