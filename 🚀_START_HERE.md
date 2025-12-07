# 🚀 START HERE - Deploy to Render

## ⚡ Quick Start (10 Minutes)

### Step 1: Run Deployment Script
```bash
# Windows (Double-click or run in CMD)
deploy-to-render.bat

# Mac/Linux (Run in Terminal)
chmod +x deploy-to-render.sh
./deploy-to-render.sh
```

### Step 2: Push to GitHub
```bash
git push origin main
```

### Step 3: Deploy on Render
1. Go to: **https://render.com**
2. Sign up with **GitHub**
3. Click: **"New +"** → **"Blueprint"**
4. Select: **Your repository**
5. Click: **"Apply"**

### Step 4: Add Environment Variables
Open `RENDER_ENV_TEMPLATE.txt` and copy these to Render:

**Required:**
- `SECRET_KEY` - Generate new one
- `GEMINI_API_KEY_1` - Your Gemini key
- `REPLICATE_API_TOKEN` - Your Replicate token
- `IMAGEKIT_PUBLIC_KEY` - Your ImageKit key
- `IMAGEKIT_PRIVATE_KEY` - Your ImageKit key
- `IMAGEKIT_URL_ENDPOINT` - Your ImageKit URL
- `YOUTUBE_API_KEY` - Your YouTube key

### Step 5: Wait & Test
1. Wait for **"Live"** status (5-10 minutes)
2. Visit your app URL
3. Create superuser in Render Shell
4. Test all features!

---

## 📚 Documentation Files

### 🎯 Choose Your Path:

#### First Time Deploying?
👉 **Read:** `RENDER_DEPLOYMENT.md` (Complete guide)
👉 **Follow:** `DEPLOYMENT_CHECKLIST.md` (Step by step)

#### Already Know Render?
👉 **Read:** `QUICK_START_RENDER.md` (10 minutes)

#### Need Environment Variables?
👉 **Copy:** `RENDER_ENV_TEMPLATE.txt`

#### Want Overview?
👉 **Read:** `RENDER_DEPLOYMENT_FILES.md`

---

## ✅ What's Already Done

### Configuration Files (Ready!)
- ✅ `django_youtube_tools/build.sh` - Build script
- ✅ `django_youtube_tools/render.yaml` - Render config
- ✅ `django_youtube_tools/requirements.txt` - Dependencies

### Deployment Scripts (Ready!)
- ✅ `deploy-to-render.bat` - Windows script
- ✅ `deploy-to-render.sh` - Mac/Linux script

### Documentation (Ready!)
- ✅ `RENDER_DEPLOYMENT.md` - Full guide
- ✅ `QUICK_START_RENDER.md` - Quick guide
- ✅ `DEPLOYMENT_CHECKLIST.md` - Checklist
- ✅ `RENDER_ENV_TEMPLATE.txt` - Environment variables

---

## 🎯 Deployment Flow

```
1. Run Script          → Prepares your app
   ↓
2. Push to GitHub      → Updates repository
   ↓
3. Deploy on Render    → Creates services
   ↓
4. Add Env Variables   → Configures app
   ↓
5. Test & Launch       → You're live! 🎉
```

---

## 💰 Cost

### Free Tier (Perfect for Testing!)
- ✅ Web Service: 750 hours/month
- ✅ PostgreSQL: 1GB storage
- ✅ Redis: 25MB storage
- ✅ Worker: 750 hours/month

**Note:** Free services spin down after 15 min inactivity

### Paid Plans (For Production)
- Web Service: $7/month
- PostgreSQL: $7/month
- Redis: $3/month
- Worker: $7/month

**Total:** ~$24/month for always-on production

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
- Check Redis is "Available"
- Check worker logs
- Verify `CELERY_BROKER_URL`

**More help:** See `RENDER_DEPLOYMENT.md` → Section 🔧

---

## 📞 Support

- **Render Docs:** https://render.com/docs
- **Render Community:** https://community.render.com
- **Django Docs:** https://docs.djangoproject.com

---

## 🎉 Ready to Deploy?

### Run this command now:

```bash
# Windows
deploy-to-render.bat

# Mac/Linux
./deploy-to-render.sh
```

Then follow the steps above!

---

## 📋 Checklist

- [ ] Ran deployment script
- [ ] Pushed to GitHub
- [ ] Created Render account
- [ ] Deployed using Blueprint
- [ ] Added environment variables
- [ ] Waited for "Live" status
- [ ] Created superuser
- [ ] Tested all features
- [ ] App is live! 🎉

---

**Good luck with your deployment! 🚀**

**Made with ❤️ for YouTube Creators**
