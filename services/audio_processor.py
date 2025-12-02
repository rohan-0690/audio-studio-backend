import librosa
import soundfile as sf
import numpy as np
from scipy import signal
from pydub import AudioSegment
import aubio

class AudioProcessor:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
    
    def get_metadata(self, file_path):
        """Extract audio metadata"""
        audio = AudioSegment.from_file(file_path)
        return {
            "duration": len(audio) / 1000.0,
            "sample_rate": audio.frame_rate,
            "channels": audio.channels,
            "bit_depth": audio.sample_width * 8
        }
    
    def apply_equalizer(self, input_path, output_path, eq_bands):
        """Apply equalizer with frequency bands"""
        y, sr = librosa.load(input_path, sr=self.sample_rate)
        
        # Define frequency bands (Hz)
        frequencies = [60, 250, 1000, 4000, 12000]
        
        # Apply filters for each band
        filtered = y.copy()
        for i, (freq, gain) in enumerate(zip(frequencies, eq_bands)):
            if i < len(frequencies) - 1:
                # Bandpass filter
                sos = signal.butter(4, [freq, frequencies[i+1]], 'bandpass', fs=sr, output='sos')
            else:
                # Highpass filter for last band
                sos = signal.butter(4, freq, 'highpass', fs=sr, output='sos')
            
            band_filtered = signal.sosfilt(sos, y)
            filtered += band_filtered * (gain - 1.0)
        
        # Normalize
        filtered = filtered / np.max(np.abs(filtered))
        sf.write(output_path, filtered, sr)
    
    def apply_compressor(self, input_path, output_path, ratio=4.0, threshold=-20):
        """Apply dynamic range compression"""
        y, sr = librosa.load(input_path, sr=self.sample_rate)
        
        # Convert to dB
        y_db = 20 * np.log10(np.abs(y) + 1e-10)
        
        # Apply compression
        compressed = y.copy()
        mask = y_db > threshold
        compressed[mask] = np.sign(y[mask]) * (
            10 ** ((threshold + (y_db[mask] - threshold) / ratio) / 20)
        )
        
        # Normalize
        compressed = compressed / np.max(np.abs(compressed)) * 0.9
        sf.write(output_path, compressed, sr)
    
    def apply_reverb(self, input_path, output_path, room_size=0.5, damping=0.5):
        """Apply reverb effect"""
        y, sr = librosa.load(input_path, sr=self.sample_rate)
        
        # Simple reverb using convolution with impulse response
        ir_length = int(sr * room_size)
        impulse_response = np.exp(-np.linspace(0, 5 * damping, ir_length))
        impulse_response = impulse_response * np.random.randn(ir_length) * 0.1
        
        # Convolve
        reverb = signal.fftconvolve(y, impulse_response, mode='same')
        
        # Mix dry and wet
        output = 0.7 * y + 0.3 * reverb
        output = output / np.max(np.abs(output)) * 0.9
        
        sf.write(output_path, output, sr)
    
    def ai_enhance(self, input_path, output_path):
        """AI-powered enhancement combining multiple effects"""
        y, sr = librosa.load(input_path, sr=self.sample_rate)
        
        # 1. Noise reduction (spectral gating)
        D = librosa.stft(y)
        magnitude, phase = np.abs(D), np.angle(D)
        
        # Estimate noise floor
        noise_floor = np.median(magnitude, axis=1, keepdims=True)
        mask = magnitude > (noise_floor * 2)
        magnitude = magnitude * mask
        
        # Reconstruct
        D_enhanced = magnitude * np.exp(1j * phase)
        y_enhanced = librosa.istft(D_enhanced)
        
        # 2. Gentle compression
        y_db = 20 * np.log10(np.abs(y_enhanced) + 1e-10)
        threshold = -25
        ratio = 3.0
        mask = y_db > threshold
        y_enhanced[mask] = np.sign(y_enhanced[mask]) * (
            10 ** ((threshold + (y_db[mask] - threshold) / ratio) / 20)
        )
        
        # 3. Subtle high-frequency boost
        sos = signal.butter(2, 3000, 'highpass', fs=sr, output='sos')
        high_freq = signal.sosfilt(sos, y_enhanced)
        y_enhanced = y_enhanced + high_freq * 0.2
        
        # Normalize
        y_enhanced = y_enhanced / np.max(np.abs(y_enhanced)) * 0.9
        sf.write(output_path, y_enhanced, sr)
    
    def detect_bpm(self, file_path):
        """Detect BPM using aubio"""
        y, sr = librosa.load(file_path, sr=self.sample_rate)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        return float(tempo)
