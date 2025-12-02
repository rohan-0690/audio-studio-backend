# Deploy to Railway (Free) - 5 Minutes

## Step 1: Sign Up for Railway

1. Go to https://railway.app/
2. Click "Start a New Project"
3. Sign up with GitHub (free account)

## Step 2: Deploy Backend

### Option A: Deploy from GitHub (Recommended)

1. **Push your code to GitHub**:
```bash
cd "C:\Users\Rohan\OneDrive\Desktop\Band App"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/audio-studio.git
git push -u origin main
```

2. **In Railway**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Select the `backend` folder
   - Click "Deploy"

### Option B: Deploy with Railway CLI

1. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

2. **Login**:
```bash
railway login
```

3. **Deploy**:
```bash
cd backend
railway init
railway up
```

## Step 3: Get Your Railway URL

After deployment (takes 3-5 minutes):
1. Go to your Railway dashboard
2. Click on your project
3. Go to "Settings" tab
4. Click "Generate Domain"
5. Copy the URL (e.g., `https://your-app.railway.app`)

## Step 4: Update Flutter App

Open `frontend/lib/services/audio_separation_service.dart`:

```dart
static const String baseUrl = 'https://your-app.railway.app/api';
```

## Step 5: Rebuild App

```bash
cd frontend
flutter run -d RZCW70FA2HN
```

## Done! 🎉

Now your app works from anywhere:
- ✅ No need to run server on your computer
- ✅ Works on any WiFi/mobile data
- ✅ Always available
- ✅ Free tier: 500 hours/month (plenty!)

## Railway Free Tier

- **Execution Time**: 500 hours/month
- **Memory**: 512MB RAM
- **Storage**: 1GB
- **Cost**: $0

Perfect for your app!

## Alternative Free Hosts

If Railway doesn't work:

### Render.com
1. Sign up: https://render.com/
2. New Web Service
3. Connect GitHub
4. Deploy

### Fly.io
1. Sign up: https://fly.io/
2. Install CLI: `curl -L https://fly.io/install.sh | sh`
3. Run: `fly launch`
4. Deploy

All have free tiers!

## Testing

Once deployed:
1. Open Audio Splitter on phone
2. Select MP3 file
3. Tap "Split Audio"
4. Wait 30-60 seconds
5. Play and adjust sliders
6. **Hear real vocal/instrument separation!**

## Monitoring

Check Railway dashboard to see:
- Server status
- Request logs
- Usage stats

## Troubleshooting

### Deployment failed
- Check Dockerfile is correct
- Ensure requirements.txt exists
- Check Railway logs

### App can't connect
- Verify URL in audio_separation_service.dart
- Check Railway service is running
- Test URL in browser: `https://your-app.railway.app/api/health`

### Slow processing
- Normal for free tier
- First request downloads AI models (one-time)
- Subsequent requests are faster

## Cost

**$0/month** with free tier limits:
- 500 hours execution time
- More than enough for personal use
- ~1000 songs per month

Need more? Upgrade to $5/month for unlimited.

---

Want me to help you deploy it? Just:
1. Create a Railway account
2. Tell me when ready
3. I'll guide you through!
