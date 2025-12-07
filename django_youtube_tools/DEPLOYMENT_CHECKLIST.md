# Deployment Checklist - Django YouTube Tools

## ⚠️ CRITICAL: Before Deployment

### 1. Environment Variables Setup ✅
**Status:** MUST DO FIRST

```bash
# Production me ye environment variables set karne ZAROORI hain:

# Django Settings
SECRET_KEY=<new-production-secret-key>  # ⚠️ Development wala mat use karo!
DEBUG=False  # ⚠️ CRITICAL - Production me True mat rakho!
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL REQUIRED)
DATABASE_URL=postgresql://user:password@host:port/database

# Redis & Celery
CELERY_BROKER_URL=redis://your-redis-host:6379/0
CELERY_RESULT_BACKEND=redis://your-redis-host:6379/0

# AI Service Keys (Production keys use karo)
GEMINI_API_KEY_1=<production-key-1>
GEMINI_API_KEY_2=<production-key-2>
GEMINI_API_KEY_3=<production-key-3>
REPLICATE_API_TOKEN=<production-token>
OPENROUTER_API_KEY=<production-key>

# ImageKit
IMAGEKIT_PUBLIC_KEY=<production-key>
IMAGEKIT_PRIVATE_KEY=<production-key>
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_id

# YouTube API
YOUTUBE_API_KEY=<production-key>
```

### 2. Database Migration ✅
**Status:** MUST DO

```bash
# Production database me migrations run karo
python manage.py migrate

# Superuser create karo
python manage.py createsuperuser
```

### 3. Static Files ✅
**Status:** MUST DO

```bash
# Static files collect karo
python manage.py collectstatic --noinput
```

### 4. Dependencies ✅
**Status:** MUST DO

```bash
# Production dependencies install karo
pip install -r requirements.txt

# Production server install karo
pip install gunicorn
```

## 🚀 Deployment Options

### Option 1: Railway (Recommended - Easiest)

**Pros:**
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ Built-in PostgreSQL
- ✅ Built-in Redis
- ✅ Easy environment variables
- ✅ Automatic HTTPS

**Steps:**
1. Push code to GitHub
2. Go to https://railway.app
3. Sign up with GitHub
4. Click "New Project" → "Deploy from GitHub repo"
5. Select your repository
6. Add PostgreSQL service
7. Add Redis service
8. Add environment variables
9. Deploy!

**Cost:** Free tier → $5-20/month for production

### Option 2: Render

**Pros:**
- ✅ Free tier available
- ✅ Automatic deployments
- ✅ Built-in PostgreSQL
- ✅ Built-in Redis
- ✅ Easy setup

**Steps:**
1. Push code to GitHub
2. Go to https://render.com
3. Sign up with GitHub
4. Create Web Service
5. Connect GitHub repo
6. Add PostgreSQL database
7. Add Redis instance
8. Set environment variables
9. Deploy!

**Cost:** Free tier → $7-25/month for production

### Option 3: Heroku

**Pros:**
- ✅ Popular platform
- ✅ Good documentation
- ✅ Add-ons available

**Cons:**
- ❌ No free tier anymore
- ❌ More expensive

**Cost:** $7-25/month minimum

### Option 4: DigitalOcean / AWS / GCP

**Pros:**
- ✅ Full control
- ✅ Scalable

**Cons:**
- ❌ More complex setup
- ❌ Need to manage server

**Cost:** $5-50/month depending on usage

## 📝 Required Files for Deployment

### 1. requirements.txt ✅
**Status:** ALREADY EXISTS

```txt
Django==5.0.1
djangorestframework==3.14.0
django-cors-headers==4.3.1
celery==5.3.4
redis==5.0.1
python-dotenv==1.0.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
google-generativeai==0.3.2
replicate==0.22.0
imagekitio==3.2.0
requests==2.31.0
```

### 2. Procfile (for Heroku/Railway)
**Status:** NEED TO CREATE

```bash
# Create Procfile
cat > Procfile << EOF
web: gunicorn config.wsgi --bind 0.0.0.0:\$PORT
worker: celery -A config worker -l info
EOF
```

### 3. runtime.txt (Optional)
**Status:** OPTIONAL

```bash
# Specify Python version
echo "python-3.10.10" > runtime.txt
```

### 4. .gitignore ✅
**Status:** VERIFY

```bash
# Make sure these are in .gitignore
.env
*.pyc
__pycache__/
db.sqlite3
staticfiles/
media/
logs/
*.log
```

## ⚙️ Production Settings

### Create production settings file:

```python
# config/settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Database
DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
```

## 🔍 Pre-Deployment Checklist

### Security ✅
- [ ] DEBUG=False set hai?
- [ ] New SECRET_KEY generate kiya?
- [ ] ALLOWED_HOSTS properly set hai?
- [ ] Production API keys use kar rahe ho?
- [ ] .env file .gitignore me hai?

### Database ✅
- [ ] PostgreSQL setup hai?
- [ ] DATABASE_URL set hai?
- [ ] Migrations run kiye?
- [ ] Superuser create kiya?

### Services ✅
- [ ] Redis setup hai?
- [ ] Celery worker chalega?
- [ ] All API keys valid hain?
- [ ] API keys ka quota check kiya?

### Static Files ✅
- [ ] collectstatic run kiya?
- [ ] Static files serve ho rahe hain?

### Testing ✅
- [ ] Local pe sab kuch kaam kar raha hai?
- [ ] All features test kiye?
- [ ] Error handling test kiya?

## 🚨 Common Deployment Issues

### Issue 1: "DisallowedHost" Error
**Solution:**
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

### Issue 2: Static Files Not Loading
**Solution:**
```bash
python manage.py collectstatic --noinput
```

### Issue 3: Database Connection Error
**Solution:**
- Check DATABASE_URL format
- Verify PostgreSQL is running
- Check credentials

### Issue 4: Celery Not Working
**Solution:**
- Ensure Redis is running
- Check CELERY_BROKER_URL
- Start Celery worker separately

### Issue 5: API Keys Not Working
**Solution:**
- Verify environment variables are set
- Check for extra spaces
- Ensure keys have proper permissions

## 📊 Post-Deployment Verification

### 1. Check Application
```bash
# Visit your domain
https://yourdomain.com

# Check admin
https://yourdomain.com/admin

# Test login
https://yourdomain.com/accounts/login/
```

### 2. Check API Endpoints
```bash
# Test thumbnail generation
curl -X POST https://yourdomain.com/api/generate-thumbnail

# Should return 401 (authentication required)
```

### 3. Check Celery
```bash
# Check Celery logs
# Ensure worker is running
```

### 4. Monitor Logs
```bash
# Check application logs
# Look for errors
# Monitor API usage
```

## 💰 Cost Estimates

### Minimal Setup (Railway/Render Free Tier)
- **Web Service:** Free
- **PostgreSQL:** Free (limited)
- **Redis:** Free (limited)
- **API Costs:** ~$5-15/month
- **Total:** ~$5-15/month

### Production Setup
- **Web Service:** $7-10/month
- **PostgreSQL:** $7-10/month
- **Redis:** $3-5/month
- **API Costs:** $25-75/month
- **Total:** ~$42-100/month

## 🎯 Recommended Deployment Flow

### For Testing/Demo:
1. **Railway Free Tier**
2. Use free PostgreSQL
3. Use free Redis
4. Test API keys
5. Monitor usage

### For Production:
1. **Railway/Render Paid**
2. Dedicated PostgreSQL
3. Dedicated Redis
4. Production API keys
5. Set up monitoring
6. Configure backups
7. Set up domain

## 📞 Support

### If Deployment Fails:
1. Check logs first
2. Verify environment variables
3. Test database connection
4. Check Redis connection
5. Verify API keys
6. Check ALLOWED_HOSTS

### Common Commands:
```bash
# Check Django
python manage.py check

# Test database
python manage.py dbshell

# Check migrations
python manage.py showmigrations

# Create superuser
python manage.py createsuperuser

# Collect static
python manage.py collectstatic
```

## ✅ Final Checklist

Before pushing to production:
- [ ] All environment variables set
- [ ] DEBUG=False
- [ ] New SECRET_KEY generated
- [ ] PostgreSQL configured
- [ ] Redis configured
- [ ] Static files collected
- [ ] Migrations run
- [ ] Superuser created
- [ ] All features tested locally
- [ ] API keys validated
- [ ] .env not in git
- [ ] requirements.txt updated
- [ ] Procfile created
- [ ] ALLOWED_HOSTS set
- [ ] Security settings enabled

## 🚀 Ready to Deploy?

**Agar sab checklist items complete hain, toh:**

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Production ready - Django YouTube Tools"
   git push origin main
   ```

2. **Deploy on Railway/Render:**
   - Connect GitHub repo
   - Add services (PostgreSQL, Redis)
   - Set environment variables
   - Deploy!

3. **Monitor:**
   - Check logs
   - Test all features
   - Monitor API usage
   - Set up alerts

**Good luck with deployment! 🎉**
