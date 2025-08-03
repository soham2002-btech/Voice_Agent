#!/usr/bin/env python3
"""
Voice Calibration Tool
=====================

This script helps calibrate the voice detection sensitivity.
Speak into your microphone and see the volume levels.
"""

import pyaudio
import numpy as np
import time

# Audio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

def calibrate_voice_detection():
    """Calibrate voice detection sensitivity"""
    audio = pyaudio.PyAudio()
    
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    
    print("🎤 Voice Calibration Tool")
    print("="*50)
    print("Speak into your microphone to see volume levels")
    print("Press Ctrl+C to exit")
    print("="*50)
    
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            audio_squared = np.maximum(audio_data**2, 0)
            volume = np.sqrt(np.mean(audio_squared))
            
            # Show volume bar
            bar_length = 50
            filled_length = int(bar_length * min(volume / 1000, 1.0))
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            
            print(f"🔊 Volume: {volume:6.0f} | {bar} | {'SPEAKING' if volume > 300 else 'SILENCE'}", end="\r")
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\n✅ Calibration complete!")
    
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    calibrate_voice_detection() 