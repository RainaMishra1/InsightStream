# 🚀 Render Deployment Guide - Django YouTube Tools

## 📋 Pre-Deployment Checklist

### ✅ Files Already Ready:
- ✅ `django_youtube_tools/build.sh` - Build script
- ✅ `django_youtube_tools/render.yaml` - Render configuration
- ✅ `django_youtube_tools/requirements.txt` - Dependencies

### 🔧 Quick Setup Commands:

```bash
# 1. Make build script executable
cd django_youtube_tools
chmod +x build.sh

# 2. Ensure gunicorn is in requirements
pip install gunicorn dj-database-url
pip freeze > requirements.txt

# 3. Commit and push to GitHub
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

---

## 🚀 Render Deployment Steps

### Step 1: Create Render Account
1. Go to **https://render.com**
2. Click **"Get Started"**
3. Sign up with **GitHub account**
4. Authorize Render to access your repositories

### Step 2: Deploy Using Blueprint (Easiest Method!)

#### Option A: Using render.yaml (Recommended)
1. Click **"New +"** → **"Blueprint"**
2. Connect your GitHub repository
3. Select repository: `InsightStream-main`
4. Render will automatically detect `render.yaml`
5. Click **"Apply"**
6. Render will create:
   - ✅ Web Service (Django app)
   - ✅ PostgreSQL Database
   - ✅ Redis Instance
   - ✅ Celery Worker

#### Option B: Manual Setup
If blueprint doesn't work, follow manual steps below.

---

### Step 3: Manual Setup (If needed)

#### 3.1 Create PostgreSQL Database
1. Click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name:** `youtube-tools-db`
   - **Database:** `youtube_tools`
   - **User:** `youtube_tools_user`
   - **Region:** `Oregon` (or closest to you)
   - **Plan:** `Free`
3. Click **"Create Database"**
4. **Copy Internal Database URL** (starts with `postgresql://`)

#### 3.2 Create Redis Instance
1. Click **"New +"** → **"Redis"**
2. Configure:
   - **Name:** `youtube-tools-redis`
   - **Region:** `Oregon` (same as database)
   - **Plan:** `Free`
3. Click **"Create Redis"**
4. **Copy Internal Redis URL** (starts with `redis://`)

#### 3.3 Create Web Service (Django)
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name:** `django-youtube-tools`
   - **Environment:** `Python 3`
   - **Region:** `Oregon`
   - **Branch:** `main`
   - **Root Directory:** `django_youtube_tools`
   - **Build Command:** 
     ```bash
     ./build.sh
     ```
   - **Start Command:** 
     ```bash
     gunicorn config.wsgi:application
     ```
   - **Plan:** `Free`

#### 3.4 Create Celery Worker
1. Click **"New +"** → **"Background Worker"**
2. Connect same repository
3. Configure:
   - **Name:** `celery-worker`
   - **Environment:** `Python 3`
   - **Region:** `Oregon`
   - **Branch:** `main`
   - **Root Directory:** `django_youtube_tools`
   - **Build Command:** 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:** 
     ```bash
     celery -A config worker -l info
     ```
   - **Plan:** `Free`

---

## 🔐 Environment Variables Setup

### For Web Service:

Go to **Web Service** → **"Environment"** tab and add:

#### Django Core Settings
```bash
SECRET_KEY=<generate-new-secret-key-here>
DEBUG=False
ALLOWED_HOSTS=.onrender.com
```

**Generate SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Database & Cache
```bash
DATABASE_URL=<your-postgres-internal-url>
REDIS_URL=<your-redis-internal-url>
CELERY_BROKER_URL=<your-redis-internal-url>
CELERY_RESULT_BACKEND=<your-redis-internal-url>
```

#### AI Service Keys (Required!)
```bash
GEMINI_API_KEY_1=<your-gemini-key-1>
GEMINI_API_KEY_2=<your-gemini-key-2>
GEMINI_API_KEY_3=<your-gemini-key-3>
REPLICATE_API_TOKEN=<your-replicate-token>
OPENROUTER_API_KEY=<your-openrouter-key>
```

#### ImageKit (Required!)
```bash
IMAGEKIT_PUBLIC_KEY=<your-imagekit-public-key>
IMAGEKIT_PRIVATE_KEY=<your-imagekit-private-key>
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_id
```

#### YouTube API (Required!)
```bash
YOUTUBE_API_KEY=<your-youtube-api-key>
```

### For Celery Worker:

Add **same environment variables** as Web Service.

---

## ✅ Post-Deployment Steps

### 1. Wait for Deployment
- Render will build and deploy (takes 5-10 minutes)
- Check **"Logs"** tab for progress
- Wait for **"Live"** status

### 2. Get Your App URL
Your app will be available at:
```
https://django-youtube-tools.onrender.com
```

### 3. Create Superuser
1. Go to **Web Service** → **"Shell"** tab
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Enter:
   - Username: `admin`
   - Email: `your-email@example.com`
   - Password: `<strong-password>`

### 4. Test Your App

Visit these URLs:

✅ **Homepage:**
```
https://django-youtube-tools.onrender.com/
```

✅ **Admin Panel:**
```
https://django-youtube-tools.onrender.com/admin/
```

✅ **Login:**
```
https://django-youtube-tools.onrender.com/accounts/login/
```

✅ **Thumbnail Generator:**
```
https://django-youtube-tools.onrender.com/thumbnails/generator/
```

✅ **Keyword Research:**
```
https://django-youtube-tools.onrender.com/keywords/research/
```

---

## 🔧 Troubleshooting

### Issue 1: Build Failed ❌
**Error:** `ModuleNotFoundError` or `ImportError`

**Solution:**
```bash
cd django_youtube_tools
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Issue 2: Database Connection Error ❌
**Error:** `could not connect to server`

**Solution:**
- Check `DATABASE_URL` is set correctly
- Ensure PostgreSQL service is **"Available"**
- Verify database name matches

### Issue 3: Static Files Not Loading ❌
**Error:** CSS/JS not loading

**Solution:**
- Check `build.sh` runs `collectstatic`
- Verify `STATIC_ROOT` in settings
- Check logs for collectstatic errors

### Issue 4: DisallowedHost Error ❌
**Error:** `Invalid HTTP_HOST header`

**Solution:**
```bash
ALLOWED_HOSTS=.onrender.com,django-youtube-tools.onrender.com
```

### Issue 5: Celery Not Working ❌
**Error:** Background tasks not running

**Solution:**
- Check Redis service is **"Available"**
- Verify `CELERY_BROKER_URL` is set
- Check **Celery Worker logs**
- Ensure worker service is deployed

### Issue 6: API Keys Not Working ❌
**Error:** API calls failing

**Solution:**
- Double-check all API keys
- Remove extra spaces
- Test keys individually
- Check API quotas/limits

---

## 💰 Render Pricing

### Free Tier (Perfect for Testing!)
- ✅ **Web Service:** 750 hours/month
- ✅ **PostgreSQL:** 1GB storage, 1 million rows
- ✅ **Redis:** 25MB storage
- ✅ **Background Worker:** 750 hours/month

**Note:** Free services spin down after 15 minutes of inactivity. First request after spin-down takes ~30 seconds.

### Paid Plans (For Production)
- **Web Service:** $7/month (always on)
- **PostgreSQL:** $7/month (more storage)
- **Redis:** $3/month (more memory)
- **Background Worker:** $7/month (always on)

**Total:** ~$24/month for production-ready setup

---

## 🚀 Auto-Deploy Setup

### Automatic Deployments (Already Enabled!)
- ✅ Every push to `main` branch triggers deployment
- ✅ Build logs available in dashboard
- ✅ Rollback available if needed

### Manual Deploy
1. Go to **Web Service** → **"Manual Deploy"**
2. Select branch: `main`
3. Click **"Deploy latest commit"**

---

## 🌐 Custom Domain (Optional)

### Add Your Domain
1. Go to **Web Service** → **"Settings"** → **"Custom Domains"**
2. Click **"Add Custom Domain"**
3. Enter: `yourdomain.com`
4. Update DNS records:
   ```
   Type: CNAME
   Name: www
   Value: django-youtube-tools.onrender.com
   ```
5. Update environment variable:
   ```bash
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,.onrender.com
   ```

---

## 📊 Monitoring

### Built-in Monitoring
- **Metrics:** CPU, Memory, Response time
- **Logs:** Real-time application logs
- **Alerts:** Email notifications for issues
- **Health Checks:** Automatic restart if app crashes

### View Logs
1. Go to **Web Service** → **"Logs"**
2. Filter by:
   - **Deploy logs:** Build process
   - **Service logs:** Application logs
   - **Event logs:** Service events

---

## 🎯 Production Checklist

Before going live:

- [ ] All environment variables set
- [ ] PostgreSQL database created and connected
- [ ] Redis instance created and connected
- [ ] Celery worker deployed and running
- [ ] Static files collecting properly
- [ ] Migrations running successfully
- [ ] Superuser created
- [ ] All features tested:
  - [ ] Login/Logout
  - [ ] Thumbnail generation
  - [ ] Keyword research
  - [ ] Content generation
  - [ ] Admin panel
- [ ] API keys valid and working
- [ ] Custom domain configured (optional)
- [ ] Monitoring enabled
- [ ] Backup strategy planned

---

## 🔄 Maintenance

### Regular Tasks
- **Weekly:** Check logs for errors
- **Monthly:** Review API usage and costs
- **Quarterly:** Update dependencies
- **As needed:** Scale services if needed

### Backup Database
1. Go to **PostgreSQL** → **"Backups"**
2. Click **"Create Backup"**
3. Download backup file

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
git commit -am "Update dependencies"
git push
```

---

## 🎉 Success!

Your Django YouTube Tools app is now live on Render!

**App URL:** `https://django-youtube-tools.onrender.com`

**Next Steps:**
1. ✅ Test all features thoroughly
2. ✅ Monitor logs for any issues
3. ✅ Set up regular backups
4. ✅ Monitor API usage and costs
5. ✅ Consider upgrading to paid plans for production

---

## 📞 Support

### Render Support
- **Docs:** https://render.com/docs
- **Community:** https://community.render.com
- **Status:** https://status.render.com

### Django YouTube Tools
- **GitHub:** Your repository
- **Issues:** Create GitHub issue

---

**Happy Deploying! 🚀**

**Made with ❤️ for YouTube Creators**
