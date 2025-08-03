"""
Audio Recorder
=============

Handles microphone input and audio recording functionality.
"""

import pyaudio
import wave
import time
from typing import Optional, List
try:
    from ..config.settings import AudioConfig
except ImportError:
    from config.settings import AudioConfig


class AudioRecorder:
    """Handles continuous audio recording from microphone"""
    
    def __init__(self, config: AudioConfig):
        self.config = config
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.audio_buffer: List[bytes] = []
    
    def start_recording(self):
        """Start continuous audio recording"""
        if self.is_recording:
            return
        
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.config.channels,
            rate=self.config.sample_rate,
            input=True,
            frames_per_buffer=self.config.chunk_size
        )
        
        self.is_recording = True
        self.audio_buffer = []
        print("🎤 Audio recording started")
    
    def record_chunk(self) -> Optional[bytes]:
        """
        Record a single audio chunk
        
        Returns:
            Audio chunk bytes or None if not recording
        """
        if not self.is_recording or not self.stream:
            return None
        
        try:
            data = self.stream.read(self.config.chunk_size, exception_on_overflow=False)
            self.audio_buffer.append(data)
            return data
        except Exception as e:
            print(f"❌ Error recording audio chunk: {e}")
            return None
    
    def save_audio(self, filename: str):
        """
        Save recorded audio to WAV file
        
        Args:
            filename: Output filename
        """
        if not self.audio_buffer:
            print("⚠️  No audio data to save")
            return
        
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.config.channels)
                wf.setsampwidth(2)  # 2 bytes for paInt16
                wf.setframerate(self.config.sample_rate)
                wf.writeframes(b''.join(self.audio_buffer))
            
            print(f"💾 Audio saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving audio: {e}")
    
    def get_audio_data(self) -> bytes:
        """
        Get all recorded audio data
        
        Returns:
            Combined audio data bytes
        """
        return b''.join(self.audio_buffer)
    
    def clear_buffer(self):
        """Clear the audio buffer"""
        self.audio_buffer = []
    
    def stop_recording(self):
        """Stop audio recording"""
        if not self.is_recording:
            return
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        self.is_recording = False
        print("🛑 Audio recording stopped")
    
    def __del__(self):
        """Cleanup audio resources"""
        self.stop_recording()
        if self.audio:
            self.audio.terminate() 