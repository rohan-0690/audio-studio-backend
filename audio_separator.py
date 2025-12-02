"""
AI Audio Separation Backend using Spleeter
This server provides API endpoints for separating vocals and instruments from audio files.

Requirements:
pip install flask spleeter flask-cors

Usage:
python audio_separator.py
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from spleeter.separator import Separator
import tempfile
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for Flutter app

# Initialize Spleeter separator
# Options: '2stems' (vocals/accompaniment), '4stems', '5stems'
separator = Separator('spleeter:3stems')  # vocals, drums, bass

UPLOAD_FOLDER = tempfile.gettempdir()
OUTPUT_FOLDER = os.path.join(UPLOAD_FOLDER, 'separated')
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/api/separate', methods=['POST'])
def separate_audio():
    """
    Separate audio into vocals, instruments, and other
    """
    try:
        # Check if file was uploaded
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Generate unique ID for this separation job
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        input_path = os.path.join(UPLOAD_FOLDER, f'{job_id}_input.mp3')
        file.save(input_path)
        
        # Create output directory for this job
        output_dir = os.path.join(OUTPUT_FOLDER, job_id)
        os.makedirs(output_dir, exist_ok=True)
        
        # Perform separation
        print(f'Separating audio: {input_path}')
        separator.separate_to_file(input_path, output_dir)
        
        # Get paths to separated files
        # Spleeter creates a subfolder with the input filename
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        separated_dir = os.path.join(output_dir, base_name)
        
        vocals_path = os.path.join(separated_dir, 'vocals.wav')
        accompaniment_path = os.path.join(separated_dir, 'accompaniment.wav')
        drums_path = os.path.join(separated_dir, 'drums.wav')
        bass_path = os.path.join(separated_dir, 'bass.wav')
        other_path = os.path.join(separated_dir, 'other.wav')
        
        # Return URLs to download separated tracks
        base_url = request.host_url
        
        response = {
            'job_id': job_id,
            'vocals_url': f'{base_url}api/download/{job_id}/vocals',
            'instruments_url': f'{base_url}api/download/{job_id}/accompaniment',
            'drums_url': f'{base_url}api/download/{job_id}/drums',
            'bass_url': f'{base_url}api/download/{job_id}/bass',
            'other_url': f'{base_url}api/download/{job_id}/other',
            'status': 'completed'
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<job_id>/<track_type>', methods=['GET'])
def download_track(job_id, track_type):
    """
    Download a separated audio track
    """
    try:
        # Construct file path
        base_name = f'{job_id}_input'
        separated_dir = os.path.join(OUTPUT_FOLDER, job_id, base_name)
        
        track_files = {
            'vocals': 'vocals.wav',
            'accompaniment': 'accompaniment.wav',
            'instruments': 'accompaniment.wav',  # Alias
            'drums': 'drums.wav',
            'bass': 'bass.wav',
            'other': 'other.wav'
        }
        
        if track_type not in track_files:
            return jsonify({'error': 'Invalid track type'}), 400
        
        file_path = os.path.join(separated_dir, track_files[track_type])
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Track not found'}), 404
        
        return send_file(file_path, mimetype='audio/wav')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({'status': 'healthy', 'service': 'audio-separator'}), 200

if __name__ == '__main__':
    print('Starting Audio Separation Server...')
    print('Spleeter model loaded and ready')
    app.run(host='0.0.0.0', port=5000, debug=True)
