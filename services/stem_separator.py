import os
from pathlib import Path
import subprocess

class StemSeparator:
    def __init__(self):
        self.models = ['2stems', '4stems', '5stems']
    
    def separate(self, input_path, output_dir, model='4stems'):
        """Separate audio into stems using Spleeter"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Use spleeter command line
        cmd = [
            'spleeter',
            'separate',
            '-p', f'spleeter:{model}',
            '-o', output_dir,
            input_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            # Fallback: manual implementation
            return self._manual_separation(input_path, output_dir)
        
        # Return paths to separated stems
        stems = {}
        stem_names = ['vocals', 'drums', 'bass', 'other']
        
        for stem_name in stem_names:
            stem_path = os.path.join(output_dir, Path(input_path).stem, f"{stem_name}.wav")
            if os.path.exists(stem_path):
                stems[stem_name] = stem_path
        
        return stems
    
    def _manual_separation(self, input_path, output_dir):
        """Fallback: Simple frequency-based separation"""
        import librosa
        import soundfile as sf
        import numpy as np
        from scipy import signal
        
        y, sr = librosa.load(input_path, sr=44100)
        
        # Vocals (mid frequencies)
        sos_vocals = signal.butter(4, [200, 3000], 'bandpass', fs=sr, output='sos')
        vocals = signal.sosfilt(sos_vocals, y)
        
        # Bass (low frequencies)
        sos_bass = signal.butter(4, 200, 'lowpass', fs=sr, output='sos')
        bass = signal.sosfilt(sos_bass, y)
        
        # Drums (transients)
        drums = y - vocals - bass
        
        # Other (high frequencies)
        sos_other = signal.butter(4, 3000, 'highpass', fs=sr, output='sos')
        other = signal.sosfilt(sos_other, y)
        
        # Save stems
        stems = {}
        for name, audio in [('vocals', vocals), ('bass', bass), ('drums', drums), ('other', other)]:
            path = os.path.join(output_dir, f"{name}.wav")
            sf.write(path, audio / np.max(np.abs(audio)) * 0.9, sr)
            stems[name] = path
        
        return stems
