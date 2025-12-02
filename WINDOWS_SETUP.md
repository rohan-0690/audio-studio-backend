# Windows Setup - Easy Way

## The Problem
Spleeter needs C++ compiler on Windows which causes errors.

## Solution 1: Use Conda (Recommended)

### Step 1: Install Miniconda
1. Download: https://docs.conda.io/en/latest/miniconda.html
2. Run installer (keep all defaults)
3. Close and reopen Command Prompt

### Step 2: Install Spleeter
Open **Anaconda Prompt** (search in Start menu):
```bash
conda create -n spleeter python=3.8 -y
conda activate spleeter
conda install -c conda-forge spleeter -y
pip install flask flask-cors
```

### Step 3: Start Server
```bash
cd "C:\Users\Rohan\OneDrive\Desktop\Band App\backend"
python simple_separator.py
```

Copy the IP address shown!

### Step 4: Update Flutter App
Open `frontend/lib/services/audio_separation_service.dart`

Change line 8 to your IP:
```dart
static const String baseUrl = 'http://YOUR_IP:5000/api';
```

### Step 5: Rebuild App
```bash
cd frontend
flutter run -d RZCW70FA2HN
```

Done! 🎉

---

## Solution 2: Use Docker (No Python Needed!)

### Step 1: Install Docker Desktop
1. Download: https://www.docker.com/products/docker-desktop
2. Install and restart computer

### Step 2: Build & Run
Open Command Prompt:
```bash
cd "C:\Users\Rohan\OneDrive\Desktop\Band App\backend"
docker build -t audio-separator .
docker run -p 5000:5000 audio-separator
```

### Step 3: Get Your IP
Open Command Prompt:
```bash
ipconfig
```
Look for "IPv4 Address" under your WiFi adapter (e.g., 192.168.1.100)

### Step 4: Update Flutter App
Same as Solution 1, Step 4

---

## Solution 3: Use Online Service (Instant!)

Skip the backend entirely and use a free online API:

### Update audio_separation_service.dart:

```dart
import 'dart:io';
import 'package:http/http.dart' as http;
import 'dart:convert';

class AudioSeparationService {
  // Using free online service
  static const String baseUrl = 'https://api.remove-vocals.media.io/api';
  
  static Future<Map<String, String>> separateAudio(String audioFilePath) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/v1/separate'),
    );
    
    request.files.add(
      await http.MultipartFile.fromPath('file', audioFilePath),
    );
    
    var response = await request.send();
    var responseData = await response.stream.bytesToString();
    var jsonData = json.decode(responseData);
    
    return {
      'vocals': jsonData['vocals_url'],
      'instruments': jsonData['music_url'],
    };
  }
}
```

This uses a free online service - no backend needed!

---

## Which Solution?

- **Conda**: Best for repeated use, fully free
- **Docker**: Easiest if you have Docker
- **Online Service**: Instant, but may have limits

## Troubleshooting

### Conda not found
- Restart Command Prompt after installing Miniconda
- Or use "Anaconda Prompt" from Start menu

### Docker not starting
- Enable virtualization in BIOS
- Or use WSL2 (Docker will prompt you)

### Still having issues?
Use Solution 3 (online service) - it works immediately!
