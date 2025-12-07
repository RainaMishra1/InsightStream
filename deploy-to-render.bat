@echo off
REM 🚀 Quick Deploy to Render Script (Windows)
REM This script prepares your Django app for Render deployment

echo 🚀 Preparing Django YouTube Tools for Render deployment...
echo.

REM Navigate to django_youtube_tools directory
cd django_youtube_tools

REM Step 1: Install required packages
echo ✅ Step 1: Installing deployment dependencies...
pip install gunicorn dj-database-url psycopg2-binary

REM Step 2: Update requirements.txt
echo ✅ Step 2: Updating requirements.txt...
pip freeze > requirements.txt

REM Step 3: Go back to root
cd ..

REM Step 4: Git operations
echo ✅ Step 3: Committing changes...
git add .
git commit -m "Ready for Render deployment"

echo.
echo 🎉 Preparation complete!
echo.
echo 📋 Next Steps:
echo 1. Push to GitHub: git push origin main
echo 2. Go to https://render.com
echo 3. Sign up with GitHub
echo 4. Click 'New +' → 'Blueprint'
echo 5. Select your repository
echo 6. Render will auto-detect render.yaml
echo 7. Add your environment variables
echo 8. Click 'Apply'
echo.
echo 📖 Full guide: Read RENDER_DEPLOYMENT.md
echo.
echo 🚀 Ready to deploy!
echo.
pause
