#!/bin/bash

# 🚀 Quick Deploy to Render Script
# This script prepares your Django app for Render deployment

echo "🚀 Preparing Django YouTube Tools for Render deployment..."
echo ""

# Navigate to django_youtube_tools directory
cd django_youtube_tools || exit

# Step 1: Make build script executable
echo "✅ Step 1: Making build.sh executable..."
chmod +x build.sh

# Step 2: Install required packages
echo "✅ Step 2: Installing deployment dependencies..."
pip install gunicorn dj-database-url psycopg2-binary

# Step 3: Update requirements.txt
echo "✅ Step 3: Updating requirements.txt..."
pip freeze > requirements.txt

# Step 4: Go back to root
cd ..

# Step 5: Git operations
echo "✅ Step 4: Committing changes..."
git add .
git commit -m "Ready for Render deployment - $(date '+%Y-%m-%d %H:%M:%S')"

echo ""
echo "🎉 Preparation complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Push to GitHub: git push origin main"
echo "2. Go to https://render.com"
echo "3. Sign up with GitHub"
echo "4. Click 'New +' → 'Blueprint'"
echo "5. Select your repository"
echo "6. Render will auto-detect render.yaml"
echo "7. Add your environment variables"
echo "8. Click 'Apply'"
echo ""
echo "📖 Full guide: Read RENDER_DEPLOYMENT.md"
echo ""
echo "🚀 Ready to deploy!"
