# ⚡ Quick Start - Deploy to Render in 10 Minutes

## 🚀 Super Fast Deployment Guide

### Step 1: Prepare (2 minutes)
```bash
# Windows
deploy-to-render.bat

# Mac/Linux
chmod +x deploy-to-render.sh
./deploy-to-render.sh
```

### Step 2: Push to GitHub (1 minute)
```bash
git push origin main
```

### Step 3: Deploy on Render (5 minutes)

1. **Go to:** https://render.com
2. **Sign up** with GitHub
3. **Click:** "New +" → "Blueprint"
4. **Select:** Your repository
5. **Click:** "Apply"

### Step 4: Add Environment Variables (2 minutes)

Copy from `RENDER_ENV_TEMPLATE.txt` and add:

**Required:**
- `SECRET_KEY` - Generate: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- `GEMINI_API_KEY_1` - Your Gemini key
- `REPLICATE_API_TOKEN` - Your Replicate token
- `IMAGEKIT_PUBLIC_KEY` - Your ImageKit key
- `IMAGEKIT_PRIVATE_KEY` - Your ImageKit key
- `IMAGEKIT_URL_ENDPOINT` - Your ImageKit URL
- `YOUTUBE_API_KEY` - Your YouTube key

**Auto-filled by Render:**
- `DATABASE_URL`
- `REDIS_URL`
- `CELERY_BROKER_URL`

### Step 5: Wait & Test (2 minutes)

1. Wait for "Live" status
2. Visit: `https://your-app.onrender.com`
3. Create superuser in Shell:
   ```bash
   python manage.py createsuperuser
   ```
4. Login and test!

---

## 🎯 That's It!

**Total Time:** ~10 minutes

**Your app is live!** 🎉

---

## 📚 Need More Details?

- **Full Guide:** `RENDER_DEPLOYMENT.md`
- **Checklist:** `DEPLOYMENT_CHECKLIST.md`
- **Environment Variables:** `RENDER_ENV_TEMPLATE.txt`

---

## 🆘 Quick Troubleshooting

### Build Failed?
```bash
cd django_youtube_tools
pip freeze > requirements.txt
git commit -am "Update requirements"
git push
```

### DisallowedHost Error?
```bash
ALLOWED_HOSTS=.onrender.com
```

### Celery Not Working?
- Check Redis service is "Available"
- Check worker logs
- Verify `CELERY_BROKER_URL` is set

---

## 💰 Cost

**Free Tier:**
- Perfect for testing
- 750 hours/month
- Spins down after 15 min inactivity

**Paid:**
- $7/month per service
- Always on
- Better performance

---

## 🚀 Ready to Deploy?

Run this command and follow the steps above:

```bash
# Windows
deploy-to-render.bat

# Mac/Linux
./deploy-to-render.sh
```

**Good luck! 🎉**
