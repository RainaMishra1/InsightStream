# Django YouTube Tools

A Django-based YouTube content creation platform with AI-powered tools for creators.

## Features

- 🎨 AI Thumbnail Generator (text-to-image and image-to-image)
- 🔍 YouTube Thumbnail Search & Analysis
- 📊 Keyword Research with YouTube trending data
- ✍️ AI Content Generator (titles, descriptions, tags)

## Tech Stack

- **Backend**: Django 5.0, Django REST Framework
- **Database**: PostgreSQL (production) / SQLite (development)
- **Background Jobs**: Celery + Redis
- **AI Services**: Gemini, Replicate, HuggingFace, OpenRouter
- **Image Storage**: ImageKit CDN
- **Frontend**: Django Templates + Alpine.js + Tailwind CSS

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

### 6. Start Celery Worker (in separate terminal)

```bash
celery -A config worker -l info
```

### 7. Start Redis (if not already running)

```bash
redis-server
```

## Project Structure

```
django_youtube_tools/
├── config/              # Django settings and configuration
├── accounts/            # User authentication
├── thumbnails/          # Thumbnail generation and search
├── content/             # AI content generation
├── keywords/            # Keyword research
├── services/            # External service integrations
├── static/              # Static files (CSS, JS)
├── templates/           # Django templates
└── manage.py
```

## API Endpoints

### Authentication
- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login
- `POST /accounts/logout/` - User logout

### Thumbnails
- `POST /api/generate-thumbnail` - Generate AI thumbnail
- `GET /api/generate-thumbnail` - Get thumbnail history
- `GET /api/thumbnail-search` - Search YouTube thumbnails

### Content
- `POST /api/ai-content-generator` - Generate video metadata
- `GET /api/ai-content-generator` - Get content history

### Keywords
- `POST /api/keyword-research` - Perform keyword research

## Development

### Running Tests

```bash
python manage.py test
```

### Code Style

This project follows PEP 8 style guidelines.

## License

MIT License
