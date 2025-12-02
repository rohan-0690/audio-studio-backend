# Deploy Audio Splitter Backend to Railway

## Quick Deploy Steps

### 1. Prepare Your Code
```bash
cd backend
git init
git add .
git commit -m "Initial commit - Audio Splitter API"
```

### 2. Push to GitHub
```bash
# Create a new repo on GitHub (https://github.com/new)
# Name it: audio-splitter-backend

git remote add origin https://github.com/rohan-0690/audio-splitter-backend.git
git branch -M main
git push -u origin main
```

### 3. Deploy on Railway

1. Go to [Railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `audio-splitter-backend` repository
6. Railway will auto-detect and deploy!

### 4. Configure Environment Variables (Optional)

In Railway dashboard:
- Click on your service
- Go to "Variables" tab
- Add: `BASE_URL` = your Railway URL (e.g., `https://your-app.up.railway.app`)

### 5. Get Your API URL

After deployment:
- Railway will give you a URL like: `https://audio-splitter-backend-production.up.railway.app`
- Copy this URL

### 6. Update Flutter App

Edit `frontend/lib/services/audio_separation_service.dart`:

```dart
static const String baseUrl = 'https://your-railway-url.up.railway.app/api';
```

## Testing Your Deployment

Test the API:
```bash
curl https://your-railway-url.up.railway.app/health
```

Should return:
```json
{"status":"healthy","service":"audio-splitter"}
```

## Features

✅ AI-powered audio separation (Spleeter)
✅ Separates vocals from instruments
✅ Fast processing (30-60 seconds per song)
✅ Automatic file cleanup
✅ CORS enabled for mobile apps
✅ Production-ready with error handling

## Cost

Railway offers:
- $5/month for 500 hours of usage
- Free trial with $5 credit
- Perfect for personal projects!

## Troubleshooting

### Build fails?
- Check Railway logs in dashboard
- Ensure all files are committed to GitHub

### API not responding?
- Check if service is running in Railway dashboard
- Verify the URL is correct
- Check CORS settings if getting network errors

### Separation takes too long?
- First request initializes Spleeter (may take 1-2 minutes)
- Subsequent requests are faster (30-60 seconds)
- Consider upgrading Railway plan for more resources

## Support

Need help? Check:
- Railway docs: https://docs.railway.app
- Spleeter docs: https://github.com/deezer/spleeter
