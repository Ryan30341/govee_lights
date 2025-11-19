"""
Audio Frequency Analyzer
Processes microphone input and maps frequencies to colors
"""
import numpy as np
import pyaudio
from scipy import signal
from typing import Tuple, Optional

class FrequencyAnalyzer:
    """Analyzes audio frequencies and maps them to colors"""
    
    def __init__(self, sample_rate: int = 44100, chunk_size: int = 4096):
        """
        Initialize frequency analyzer
        
        Args:
            sample_rate: Audio sample rate in Hz
            chunk_size: Number of samples per chunk
        """
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.audio = pyaudio.PyAudio()
        self.stream = None
        
        # Frequency ranges for color mapping
        # Typical human hearing: 20 Hz to 20,000 Hz
        self.min_freq = 20
        self.max_freq = 20000
        
    def start_stream(self, device_index: Optional[int] = None):
        """Start audio input stream"""
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=self.chunk_size
        )
    
    def stop_stream(self):
        """Stop audio input stream"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
    
    def get_frequency_spectrum(self) -> np.ndarray:
        """
        Get current frequency spectrum from microphone
        
        Returns:
            Array of frequency magnitudes
        """
        if not self.stream:
            raise RuntimeError("Audio stream not started")
        
        # Read audio data
        data = self.stream.read(self.chunk_size, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Apply FFT
        fft_data = np.fft.fft(audio_data)
        frequencies = np.fft.fftfreq(len(fft_data), 1/self.sample_rate)
        
        # Get magnitude spectrum
        magnitude = np.abs(fft_data)
        
        # Return only positive frequencies
        positive_freq_idx = frequencies >= 0
        return frequencies[positive_freq_idx], magnitude[positive_freq_idx]
    
    def get_dominant_frequency(self) -> float:
        """
        Get the dominant frequency from current audio input
        
        Returns:
            Dominant frequency in Hz
        """
        frequencies, magnitude = self.get_frequency_spectrum()
        
        # Find peak frequency
        peak_idx = np.argmax(magnitude)
        dominant_freq = frequencies[peak_idx]
        
        return dominant_freq
    
    def frequency_to_color(self, frequency: float) -> Tuple[int, int, int]:
        """
        Map frequency to RGB color
        
        Uses a gradient from low (red) to high (blue/violet) frequencies
        
        Args:
            frequency: Frequency in Hz
            
        Returns:
            RGB tuple (r, g, b) with values 0-255
        """
        # Clamp frequency to valid range
        freq_clamped = np.clip(frequency, self.min_freq, self.max_freq)
        
        # Normalize to 0-1 range
        normalized = (freq_clamped - self.min_freq) / (self.max_freq - self.min_freq)
        
        # Create color gradient
        # Low frequencies -> Red
        # Mid frequencies -> Green
        # High frequencies -> Blue
        
        if normalized < 0.33:
            # Red to Yellow
            r = 255
            g = int(255 * (normalized / 0.33))
            b = 0
        elif normalized < 0.66:
            # Yellow to Cyan
            r = int(255 * (1 - (normalized - 0.33) / 0.33))
            g = 255
            b = int(255 * ((normalized - 0.33) / 0.33))
        else:
            # Cyan to Blue/Violet
            r = 0
            g = int(255 * (1 - (normalized - 0.66) / 0.34))
            b = 255
        
        return (r, g, b)
    
    def get_current_color(self) -> Tuple[int, int, int]:
        """
        Get current color based on microphone input
        
        Returns:
            RGB tuple (r, g, b)
        """
        freq = self.get_dominant_frequency()
        return self.frequency_to_color(freq)
    
    def cleanup(self):
        """Clean up audio resources"""
        self.stop_stream()
        if self.audio:
            self.audio.terminate()

