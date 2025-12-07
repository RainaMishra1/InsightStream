# Django YouTube Tools

AI-powered YouTube content creation platform built with Django. Generate thumbnails, research keywords, search similar videos, and create optimized content for your YouTube channel.

## 🚀 Features

1. **AI Thumbnail Generator** - Generate stunning thumbnails using AI (Replicate FLUX model)
2. **Thumbnail Search** - Find similar videos on YouTube with AI-powered tag extraction
3. **Keyword Research** - Discover trending keywords with search volume and competition metrics
4. **Content Generator** - Create SEO-optimized titles, descriptions, and tags using AI

## 🛠️ Tech Stack

- **Backend:** Django 5.0.1 + Django REST Framework
- **Database:** PostgreSQL (SQLite for development)
- **Cache/Queue:** Redis + Celery
- **Frontend:** Django Templates + Tailwind CSS + Alpine.js
- **AI Services:** Gemini, Replicate, OpenRouter
- **CDN:** ImageKit
- **API:** YouTube Data API v3

## 📋 Prerequisites

- Python 3.10+
- Redis
- PostgreSQL (for production)
- API Keys (see Environment Setup)

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd django_youtube_tools
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Start Services

**Terminal 1 - Redis:**
```bash
redis-server
```

**Terminal 2 - Celery Worker:**
```bash
celery -A config worker -l info
```

**Terminal 3 - Django Server:**
```bash
python manage.py runserver
```

### 8. Access Application
- **Application:** http://localhost:8000
- **Admin:** http://localhost:8000/admin
- **Login:** http://localhost:8000/accounts/login/

## 📁 Project Structure

```
django_youtube_tools/
├── config/              # Django settings and configuration
├── accounts/            # User authentication
├── thumbnails/          # Thumbnail generation and search
├── content/             # Content generation
├── keywords/            # Keyword research
├── services/            # External service integrations
├── templates/           # Django templates
├── static/              # Static files
├── logs/                # Application logs
└── manage.py            # Django management script
```

## 🔑 Environment Variables

See `ENVIRONMENT_SETUP.md` for detailed instructions on getting API keys.

**Required:**
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `CELERY_BROKER_URL` - Redis URL
- `GEMINI_API_KEY_1/2/3` - Google Gemini AI
- `REPLICATE_API_TOKEN` - Replicate AI
- `OPENROUTER_API_KEY` - OpenRouter AI
- `IMAGEKIT_PUBLIC_KEY` - ImageKit CDN
- `IMAGEKIT_PRIVATE_KEY` - ImageKit CDN
- `IMAGEKIT_URL_ENDPOINT` - ImageKit URL
- `YOUTUBE_API_KEY` - YouTube Data API

## 📚 Documentation

- **Environment Setup:** `ENVIRONMENT_SETUP.md`
- **Deployment Guide:** `DEPLOYMENT_CHECKLIST.md`
- **Task Completion:** `TASK_*_COMPLETE.md` files

## 🧪 Testing

```bash
# Run Django checks
python manage.py check

# Run tests (when implemented)
python manage.py test
```

## 🚀 Deployment

See `DEPLOYMENT_CHECKLIST.md` for complete deployment instructions.

**Recommended Platforms:**
- Railway (easiest)
- Render
- Heroku
- DigitalOcean

**Quick Deploy to Railway:**
1. Push code to GitHub
2. Connect to Railway
3. Add PostgreSQL and Redis
4. Set environment variables
5. Deploy!

## 📊 Features Overview

### 1. Thumbnail Generator
- Text-to-image generation
- Image-to-image with reference
- AI-powered (Replicate FLUX)
- Automatic ImageKit upload
- Background processing with Celery
- History tracking

### 2. Thumbnail Search
- YouTube video search
- AI tag extraction from thumbnails
- Similar thumbnail discovery
- Video statistics (views, likes, comments)

### 3. Keyword Research
- YouTube trending data analysis
- AI-powered keyword categorization
- Primary, long-tail, and trending keywords
- Search volume and competition metrics
- Content suggestions

### 4. Content Generator
- 3 SEO-optimized title options
- Professional YouTube descriptions
- 10 relevant tags
- Background processing
- History tracking

## 🔒 Security

- Session-based authentication
- CSRF protection
- User data isolation
- Secure API key management
- Comprehensive error handling
- Production-ready settings

## 💰 Cost Estimates

**Free Tiers:**
- Gemini AI - Free tier available
- YouTube API - 10,000 units/day
- ImageKit - 20GB storage/bandwidth

**Paid Services:**
- Replicate - ~$0.01-0.10 per thumbnail
- OpenRouter - ~$0.001-0.01 per request

**Monthly:** ~$5-75 depending on usage

## 🤝 Contributing

This is a migrated project from Next.js to Django. All features have been successfully migrated with 100% feature parity.

## 📝 License

[Your License Here]

## 🆘 Support

For issues:
1. Check logs in `logs/django.log`
2. Verify environment variables
3. Check service status (Redis, Celery)
4. Review documentation files

## 🎯 Migration Status

✅ **Complete Migration from Next.js to Django**
- All 4 features migrated
- Frontend converted to Django templates
- Background jobs migrated to Celery
- Authentication migrated to Django Auth
- 100% feature parity achieved

---

**Built with ❤️ using Django**
