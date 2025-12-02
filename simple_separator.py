"""
Simple Free Audio Separator using Spleeter
Run this on your computer and connect your phone to the same WiFi
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import subprocess
import tempfile
import uuid
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Create temp directories
UPLOAD_DIR = os.path.join(tempfile.gettempdir(), 'audio_uploads')
OUTPUT_DIR = os.path.join(tempfile.gettempdir(), 'audio_separated')
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/api/separate', methods=['POST'])
def separate_audio():
    """Separate audio using Spleeter"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file'}), 400
        
        file = request.files['audio']
        job_id = str(uuid.uuid4())[:8]
        
        # Save uploaded file
        input_path = os.path.join(UPLOAD_DIR, f'{job_id}.mp3')
        file.save(input_path)
        
        # Create output directory
        output_path = os.path.join(OUTPUT_DIR, job_id)
        os.makedirs(output_path, exist_ok=True)
        
        print(f'Separating: {input_path}')
        
        # Run Spleeter command
        cmd = [
            'spleeter',
            'separate',
            '-p', 'spleeter:2stems',  # vocals and accompaniment
            '-o', output_path,
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f'Error: {result.stderr}')
            return jsonify({'error': 'Separation failed'}), 500
        
        # Find separated files
        base_name = Path(input_path).stem
        separated_dir = os.path.join(output_path, base_name)
        
        vocals_file = os.path.join(separated_dir, 'vocals.wav')
        accompaniment_file = os.path.join(separated_dir, 'accompaniment.wav')
        
        if not os.path.exists(vocals_file):
            return jsonify({'error': 'Separation output not found'}), 500
        
        # Get server IP
        host = request.host
        
        return jsonify({
            'job_id': job_id,
            'vocals_url': f'http://{host}/api/download/{job_id}/vocals',
            'instruments_url': f'http://{host}/api/download/{job_id}/accompaniment',
            'status': 'completed'
        }), 200
        
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<job_id>/<track>', methods=['GET'])
def download_track(job_id, track):
    """Download separated track"""
    try:
        # Find the input file
        input_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(job_id)]
        if not input_files:
            return jsonify({'error': 'Job not found'}), 404
        
        base_name = Path(input_files[0]).stem
        separated_dir = os.path.join(OUTPUT_DIR, job_id, base_name)
        
        track_map = {
            'vocals': 'vocals.wav',
            'accompaniment': 'accompaniment.wav',
            'instruments': 'accompaniment.wav'
        }
        
        if track not in track_map:
            return jsonify({'error': 'Invalid track'}), 400
        
        file_path = os.path.join(separated_dir, track_map[track])
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Track not found'}), 404
        
        return send_file(file_path, mimetype='audio/wav')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'service': 'audio-separator'}), 200

if __name__ == '__main__':
    import socket
    
    # Get local IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    
    print('=' * 50)
    print('🎵 Audio Separator Server Starting...')
    print('=' * 50)
    print(f'Local IP: {local_ip}')
    print(f'Server URL: http://{local_ip}:5000')
    print('\nUpdate your Flutter app with this URL:')
    print(f'  static const String baseUrl = "http://{local_ip}:5000/api";')
    print('\nMake sure your phone is on the same WiFi network!')
    print('=' * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
