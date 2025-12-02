"""
Simple test script for the Audio Splitter API
Run this after starting the server to verify it works
"""
import requests
import sys

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check passed:", response.json())
            return True
        else:
            print("❌ Health check failed:", response.status_code)
            return False
    except Exception as e:
        print("❌ Could not connect to server:", e)
        return False

def test_root():
    """Test the root endpoint"""
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Root endpoint passed:", response.json())
            return True
        else:
            print("❌ Root endpoint failed:", response.status_code)
            return False
    except Exception as e:
        print("❌ Error:", e)
        return False

def test_separation(audio_file_path):
    """Test audio separation with a real file"""
    try:
        with open(audio_file_path, 'rb') as f:
            files = {'audio': f}
            print(f"📤 Uploading {audio_file_path}...")
            response = requests.post("http://localhost:8000/api/separate", files=files)
            
        if response.status_code == 200:
            result = response.json()
            print("✅ Separation successful!")
            print(f"   Vocals: {result['vocals_url']}")
            print(f"   Instruments: {result['instruments_url']}")
            return True
        else:
            print("❌ Separation failed:", response.status_code, response.text)
            return False
    except FileNotFoundError:
        print(f"❌ File not found: {audio_file_path}")
        return False
    except Exception as e:
        print("❌ Error:", e)
        return False

if __name__ == "__main__":
    print("🧪 Testing Audio Splitter API\n")
    
    # Test basic endpoints
    health_ok = test_health()
    root_ok = test_root()
    
    if not (health_ok and root_ok):
        print("\n❌ Basic tests failed. Make sure the server is running:")
        print("   python app.py")
        sys.exit(1)
    
    print("\n✅ All basic tests passed!")
    
    # Test separation if audio file provided
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        print(f"\n🎵 Testing separation with: {audio_file}")
        test_separation(audio_file)
    else:
        print("\n💡 To test separation, run:")
        print("   python test_api.py path/to/your/audio.mp3")
