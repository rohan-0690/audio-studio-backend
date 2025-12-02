# Local Testing Guide

Test your audio splitter backend before deploying to Railway.

## 🖥️ Setup Local Environment

### Windows

```bash
cd backend
start.bat
```

The script will:
- Create virtual environment
- Install dependencies
- Start server on http://localhost:8000

### Manual Setup (All Platforms)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
python app.py
```

## ✅ Test the API

### 1. Test Health Endpoint

Open browser: http://localhost:8000/health

Should see:
```json
{"status":"healthy","service":"audio-splitter"}
```

### 2. Test API Info

Open browser: http://localhost:8000/

Should see API information.

### 3. Test Audio Separation

Using Python test script:
```bash
python test_api.py path/to/your/song.mp3
```

Using curl:
```bash
curl -X POST -F "audio=@path/to/song.mp3" http://localhost:8000/api/separate
```

## 📱 Test with Flutter App

### 1. Find Your Computer's IP Address

**Windows:**
```bash
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

**Mac/Linux:**
```bash
ifconfig
```
Look for "inet" address

### 2. Update Flutter App

Edit `frontend/lib/services/audio_separation_service.dart`:
```dart
static const String baseUrl = 'http://YOUR-IP:8000/api';
```

Replace `YOUR-IP` with your computer's IP (e.g., 192.168.1.100)

### 3. Run Flutter App

Make sure:
- Backend server is running
- Phone/emulator is on same WiFi network
- Firewall allows port 8000

```bash
cd frontend
flutter run
```

### 4. Test in App

1. Open Audio Splitter screen
2. Select an MP3 file
3. Click "SPLIT AUDIO"
4. Wait 30-60 seconds
5. Play separated tracks!

## 🔍 Troubleshooting

### Server won't start

**Error: "Port 8000 already in use"**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill
```

**Error: "Module not found"**
```bash
pip install -r requirements.txt
```

### Flutter can't connect

**Check server is running:**
- Look for "Uvicorn running on http://0.0.0.0:8000"

**Check IP address:**
- Use `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
- Update Flutter app with correct IP

**Check firewall:**
- Allow Python through Windows Firewall
- Allow port 8000

**Check WiFi:**
- Phone and computer must be on same network
- Some public WiFi blocks device-to-device communication

### Separation fails

**Error: "Spleeter not found"**
```bash
pip install spleeter
```

**Error: "TensorFlow error"**
- First separation initializes model (1-2 minutes)
- Check logs for specific error
- May need to reinstall TensorFlow:
```bash
pip uninstall tensorflow
pip install tensorflow==2.15.0
```

**Takes too long:**
- First separation: 1-2 minutes (normal)
- Subsequent: 30-60 seconds (normal)
- Use smaller files for testing

## 📊 Monitor Logs

Server logs show:
- Incoming requests
- Processing status
- Errors and warnings
- Completion messages

Watch for:
```
INFO: Saving uploaded file: uploads/xxx.mp3
INFO: Starting separation for job xxx
INFO: Separation completed for job xxx
```

## 🎯 Expected Performance

| Operation | Time |
|-----------|------|
| Server startup | 5-10 seconds |
| First separation | 1-2 minutes |
| Subsequent separations | 30-60 seconds |
| File download | 1-5 seconds |

## ✨ Success Indicators

- [ ] Server starts without errors
- [ ] Health endpoint returns 200 OK
- [ ] Test script passes all tests
- [ ] Flutter app connects successfully
- [ ] Audio file uploads successfully
- [ ] Separation completes without errors
- [ ] Separated files download correctly
- [ ] Vocals and instruments play in app

## 🚀 Ready for Production?

Once local testing works:
1. Follow [QUICK_DEPLOY.md](../QUICK_DEPLOY.md) to deploy to Railway
2. Update Flutter app with Railway URL
3. Test production deployment
4. Share your app!

## 💡 Tips

1. **Use small audio files** for testing (< 5MB)
2. **Keep server running** while testing Flutter app
3. **Check logs** if something fails
4. **Test on WiFi** not mobile data
5. **Allow firewall** access when prompted

---

Happy testing! 🎉
