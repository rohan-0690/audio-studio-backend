# Free Audio Separation Setup (5 Minutes)

## Step 1: Install Python (if you don't have it)

**Windows:**
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click Install

**Already have Python?** Skip to Step 2

## Step 2: Install Spleeter

Open Command Prompt (Windows) or Terminal (Mac/Linux):

```bash
pip install spleeter flask flask-cors
```

Wait 2-3 minutes for installation.

## Step 3: Start the Server

```bash
cd backend
python simple_separator.py
```

You'll see something like:
```
🎵 Audio Separator Server Starting...
Local IP: 192.168.1.100
Server URL: http://192.168.1.100:5000

Update your Flutter app with this URL:
  static const String baseUrl = "http://192.168.1.100:5000/api";
```

**Copy that IP address!** (e.g., 192.168.1.100)

## Step 4: Update Flutter App

Open `frontend/lib/services/audio_separation_service.dart`

Change this line:
```dart
static const String baseUrl = 'https://your-api-endpoint.com/api';
```

To your server IP:
```dart
static const String baseUrl = 'http://192.168.1.100:5000/api';  // Use YOUR IP
```

## Step 5: Rebuild App

```bash
cd frontend
flutter run -d RZCW70FA2HN
```

## Step 6: Test It!

1. Open app on your phone
2. Go to Audio Splitter
3. Select an MP3 file
4. Tap "Split Audio"
5. Wait 30-60 seconds
6. Play and adjust sliders!

## Troubleshooting

### "Connection refused"
- Make sure server is running
- Check phone and computer are on same WiFi
- Try turning off Windows Firewall temporarily

### "Module not found"
```bash
pip install --upgrade spleeter flask flask-cors
```

### "Port already in use"
Change port in `simple_separator.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=False)  # Use 5001 instead
```

### First run is slow
Spleeter downloads AI models (~100MB) on first use. This only happens once.

## How It Works

1. **Your Phone** → Sends MP3 to server
2. **Your Computer** → Runs AI to separate vocals/instruments
3. **Your Phone** ← Downloads separated tracks
4. **Your Phone** → Plays them with volume controls

## Cost

**100% FREE!**
- No API fees
- No subscriptions
- Unlimited usage
- Runs on your computer

## Performance

- **3-minute song**: ~30-60 seconds
- **Quality**: Professional grade
- **Formats**: MP3, WAV, FLAC supported

## Keep Server Running

While using the app, keep the Command Prompt/Terminal window open with the server running.

To stop: Press `Ctrl+C`

## Next Steps

Once it's working, you can:
1. Deploy to a cloud server (free tier on Railway/Render)
2. Use it from anywhere
3. Share with friends

## Need Help?

Common issues:
- **Firewall blocking**: Allow Python in Windows Firewall
- **Wrong IP**: Make sure to use the IP shown when server starts
- **Different WiFi**: Phone and computer must be on same network

That's it! You now have free AI audio separation! 🎉
