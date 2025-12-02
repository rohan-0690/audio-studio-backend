# Audio Splitter Backend API

AI-powered audio separation service that splits songs into vocals and instruments using Spleeter.

## Features

- 🎤 **Vocal Separation** - Extract vocals from any song
- 🎸 **Instrument Isolation** - Get instrumental tracks
- 🚀 **Fast Processing** - 30-60 seconds per song
- 🌐 **REST API** - Easy integration with any frontend
- ☁️ **Railway Ready** - Deploy in minutes

## Quick Start (Local Development)

### 1. Install Dependencies

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Run the Server

```bash
python app.py
```

Server starts at: `http://localhost:8000`

### 3. Test the API

```bash
# Test health
curl http://localhost:8000/health

# Test separation (replace with your audio file)
python test_api.py path/to/song.mp3
```

## API Endpoints

### GET `/`
Get API information

**Response:**
```json
{
  "message": "Audio Splitter API",
  "version": "1.0.0",
  "status": "running"
}
```

### GET `/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "audio-splitter"
}
```

### POST `/api/separate`
Separate audio into vocals and instruments

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `audio` file (mp3, wav, flac, m4a)

**Response:**
```json
{
  "success": true,
  "job_id": "uuid-here",
  "vocals_url": "http://localhost:8000/files/uuid/vocals.wav",
  "instruments_url": "http://localhost:8000/files/uuid/accompaniment.wav",
  "message": "Audio separated successfully"
}
```

### DELETE `/api/cleanup/{job_id}`
Clean up processed files

**Response:**
```json
{
  "success": true,
  "message": "Cleaned up job uuid"
}
```

## Deploy to Railway

See [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md) for detailed deployment instructions.

**Quick steps:**
1. Push code to GitHub
2. Connect Railway to your repo
3. Deploy automatically
4. Get your production URL
5. Update Flutter app with the URL

## Technology Stack

- **FastAPI** - Modern Python web framework
- **Spleeter** - AI audio separation by Deezer
- **TensorFlow** - Machine learning backend
- **Uvicorn** - ASGI server

## Configuration

Environment variables:
- `PORT` - Server port (default: 8000)
- `BASE_URL` - Base URL for file serving (auto-detected)

## File Structure

```
backend/
├── app.py              # Main API application
├── requirements.txt    # Python dependencies
├── Procfile           # Railway deployment config
├── railway.toml       # Railway settings
├── test_api.py        # API test script
├── uploads/           # Temporary upload storage
└── processed/         # Separated audio files
```

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Port already in use"
Change port in app.py or kill the process:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill
```

### Separation takes too long
- First request initializes Spleeter (1-2 minutes)
- Subsequent requests are faster (30-60 seconds)
- Use smaller audio files for testing

### CORS errors from Flutter
- CORS is enabled for all origins
- Check if server is running
- Verify the URL in Flutter app

## Performance

- **First separation:** 1-2 minutes (model initialization)
- **Subsequent separations:** 30-60 seconds
- **File size limit:** Recommended < 10MB
- **Supported formats:** MP3, WAV, FLAC, M4A

## License

MIT License - Free to use for personal and commercial projects

## Credits

- Spleeter by Deezer Research
- Built for AI Audio Studio Flutter app
