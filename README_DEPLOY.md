# Deploy to Railway - Step by Step

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `audio-studio-backend`
3. Make it **Public** (required for free Railway)
4. Click "Create repository"

## Step 2: Push Code to GitHub

Run these commands in your terminal:

```bash
cd "C:\Users\Rohan\OneDrive\Desktop\Band App"

git init
git add backend/
git add .gitignore
git commit -m "Add audio separation backend"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/audio-studio-backend.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username!

## Step 3: Deploy to Railway

1. Go to https://railway.app/
2. Click "Start a New Project"
3. Click "Deploy from GitHub repo"
4. Sign in with GitHub
5. Authorize Railway
6. Select `audio-studio-backend` repository
7. Click "Deploy Now"

Railway will automatically:
- Detect the Dockerfile
- Build the backend
- Deploy it
- Give you a URL

## Step 4: Get Your URL

1. Wait 3-5 minutes for deployment
2. In Railway dashboard, click "Settings"
3. Scroll to "Domains"
4. Click "Generate Domain"
5. Copy the URL (e.g., `https://audio-studio-backend-production.up.railway.app`)

## Step 5: Update Flutter App

Open `frontend/lib/services/audio_separation_service.dart`

Change line 4:
```dart
static const String baseUrl = 'https://audio-studio-backend-production.up.railway.app/api';
```

Use YOUR Railway URL!

## Step 6: Test It

1. Rebuild app: `flutter run -d RZCW70FA2HN`
2. Open Audio Splitter
3. Select MP3
4. Tap "Split Audio"
5. Wait 30-60 seconds
6. Real AI separation! 🎉

## Troubleshooting

### "Repository not found"
- Make sure repository is Public
- Check you're logged into correct GitHub account

### "Build failed"
- Check Railway logs
- Ensure Dockerfile and requirements.txt are in backend folder

### "Can't connect from app"
- Verify URL in audio_separation_service.dart
- Test URL in browser: `https://your-url.railway.app/api/health`
- Should return: `{"status":"ok"}`

### "Deployment taking too long"
- First deployment downloads AI models (~100MB)
- Takes 5-10 minutes first time
- Subsequent deploys are faster

## Railway Free Tier

- ✅ 500 hours/month execution time
- ✅ 512MB RAM
- ✅ 1GB storage
- ✅ Always-on service
- ✅ Custom domain
- ✅ Automatic HTTPS

More than enough for your app!

## After Deployment

Your backend will be live at:
`https://your-app.railway.app`

Test it:
- Health check: `https://your-app.railway.app/api/health`
- Should return: `{"status":"healthy","service":"audio-separator"}`

## Need Help?

Tell me:
1. Your GitHub username
2. If you created the repository
3. Any errors you see

I'll help you through it!
