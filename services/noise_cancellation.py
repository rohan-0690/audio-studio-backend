import noisereduce as nr
import librosa
import soundfile as sf
import numpy as np

class NoiseCanceller:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
    
    def process(self, input_path, output_path):
        """Apply noise cancellation using noisereduce library"""
        # Load audio
        y, sr = librosa.load(input_path, sr=self.sample_rate)
        
        # Apply noise reduction
        # Use first 0.5 seconds as noise profile
        noise_sample_length = int(0.5 * sr)
        noise_sample = y[:noise_sample_length]
        
        # Reduce noise
        reduced_noise = nr.reduce_noise(
            y=y,
            sr=sr,
            stationary=True,
            prop_decrease=0.8
        )
        
        # Normalize
        reduced_noise = reduced_noise / np.max(np.abs(reduced_noise)) * 0.9
        
        # Save
        sf.write(output_path, reduced_noise, sr)
        
        return output_path
    
    def process_realtime_chunk(self, audio_chunk, sr):
        """Process audio chunk for real-time noise cancellation"""
        reduced = nr.reduce_noise(
            y=audio_chunk,
            sr=sr,
            stationary=True,
            prop_decrease=0.8
        )
        return reduced
