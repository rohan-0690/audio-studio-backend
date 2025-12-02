import numpy as np
import soundfile as sf
from scipy import signal

class DrumMachine:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
    
    def generate(self, genre, output_path, bpm=120, duration=8):
        """Generate drum beat based on genre"""
        if bpm is None:
            bpm = self._get_default_bpm(genre)
        
        # Calculate beat timing
        beat_duration = 60.0 / bpm
        num_beats = int(duration / beat_duration)
        
        # Generate pattern based on genre
        pattern = self._get_pattern(genre)
        
        # Create audio
        audio = self._create_drum_audio(pattern, beat_duration, num_beats)
        
        # Save
        sf.write(output_path, audio, self.sample_rate)
        return output_path
    
    def _get_default_bpm(self, genre):
        """Get default BPM for genre"""
        bpm_map = {
            'rock': 120,
            'jazz': 140,
            'electronic': 128,
            'metal': 180,
            'hip-hop': 90,
            'pop': 120,
            'funk': 110
        }
        return bpm_map.get(genre.lower(), 120)
    
    def _get_pattern(self, genre):
        """Get drum pattern for genre"""
        patterns = {
            'rock': {
                'kick': [1, 0, 0, 0, 1, 0, 0, 0],
                'snare': [0, 0, 1, 0, 0, 0, 1, 0],
                'hihat': [1, 1, 1, 1, 1, 1, 1, 1]
            },
            'electronic': {
                'kick': [1, 0, 0, 0, 1, 0, 0, 0],
                'snare': [0, 0, 1, 0, 0, 0, 1, 0],
                'hihat': [1, 0, 1, 0, 1, 0, 1, 0]
            },
            'jazz': {
                'kick': [1, 0, 0, 1, 0, 0, 1, 0],
                'snare': [0, 0, 1, 0, 0, 1, 0, 0],
                'hihat': [1, 1, 1, 1, 1, 1, 1, 1]
            },
            'metal': {
                'kick': [1, 1, 0, 0, 1, 1, 0, 0],
                'snare': [0, 0, 1, 0, 0, 0, 1, 0],
                'hihat': [1, 1, 1, 1, 1, 1, 1, 1]
            },
            'hip-hop': {
                'kick': [1, 0, 0, 0, 0, 0, 1, 0],
                'snare': [0, 0, 0, 0, 1, 0, 0, 0],
                'hihat': [1, 0, 1, 1, 0, 1, 1, 0]
            }
        }
        return patterns.get(genre.lower(), patterns['rock'])
    
    def _create_drum_audio(self, pattern, beat_duration, num_beats):
        """Create drum audio from pattern"""
        total_samples = int(beat_duration * num_beats * self.sample_rate)
        audio = np.zeros(total_samples)
        
        # Generate drum sounds
        kick_sound = self._generate_kick()
        snare_sound = self._generate_snare()
        hihat_sound = self._generate_hihat()
        
        sounds = {
            'kick': kick_sound,
            'snare': snare_sound,
            'hihat': hihat_sound
        }
        
        # Place sounds according to pattern
        steps_per_beat = len(pattern['kick'])
        step_duration = beat_duration / steps_per_beat
        
        for beat in range(num_beats):
            for step in range(steps_per_beat):
                step_time = (beat * steps_per_beat + step) * step_duration
                step_sample = int(step_time * self.sample_rate)
                
                for drum_type, drum_pattern in pattern.items():
                    if drum_pattern[step % len(drum_pattern)] == 1:
                        sound = sounds[drum_type]
                        end_sample = min(step_sample + len(sound), total_samples)
                        audio[step_sample:end_sample] += sound[:end_sample - step_sample]
        
        # Normalize
        audio = audio / np.max(np.abs(audio)) * 0.9
        return audio
    
    def _generate_kick(self):
        """Generate kick drum sound"""
        duration = 0.5
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Frequency sweep from 150Hz to 40Hz
        freq = 150 * np.exp(-5 * t)
        kick = np.sin(2 * np.pi * freq * t)
        
        # Envelope
        envelope = np.exp(-8 * t)
        kick = kick * envelope
        
        return kick
    
    def _generate_snare(self):
        """Generate snare drum sound"""
        duration = 0.2
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Tone component (200Hz)
        tone = np.sin(2 * np.pi * 200 * t)
        
        # Noise component
        noise = np.random.randn(samples)
        
        # Mix
        snare = 0.3 * tone + 0.7 * noise
        
        # Envelope
        envelope = np.exp(-15 * t)
        snare = snare * envelope
        
        return snare
    
    def _generate_hihat(self):
        """Generate hi-hat sound"""
        duration = 0.1
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # High-frequency noise
        hihat = np.random.randn(samples)
        
        # High-pass filter
        sos = signal.butter(4, 5000, 'highpass', fs=self.sample_rate, output='sos')
        hihat = signal.sosfilt(sos, hihat)
        
        # Envelope
        envelope = np.exp(-40 * t)
        hihat = hihat * envelope
        
        return hihat
