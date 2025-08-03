#!/usr/bin/env python3
"""
Test Turn Detection
==================

Simple test to verify turn detection works properly.
"""

import pyaudio
import numpy as np
import time

# Audio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# VAD Configuration
SILENCE_THRESHOLD = 15
SPEECH_THRESHOLD = 35
SILENCE_DURATION = 1.0

def test_turn_detection():
    """Test turn detection with current thresholds"""
    audio = pyaudio.PyAudio()
    
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    
    print("🎤 Turn Detection Test")
    print("="*50)
    print(f"Speech Threshold: {SPEECH_THRESHOLD}")
    print(f"Silence Threshold: {SILENCE_THRESHOLD}")
    print(f"Silence Duration: {SILENCE_DURATION}s")
    print("="*50)
    print("1. Speak for a few seconds")
    print("2. Stop speaking and wait for turn to end")
    print("3. Press Ctrl+C to exit")
    print("="*50)
    
    # VAD state
    is_speaking = False
    speech_start = None
    silence_start = None
    
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            audio_squared = np.maximum(audio_data**2, 0)
            volume = np.sqrt(np.mean(audio_squared))
            
            current_time = time.time()
            
            # Detect speech
            if volume > SPEECH_THRESHOLD:
                if not is_speaking:
                    is_speaking = True
                    speech_start = current_time
                    silence_start = None
                    print(f"\n🎤 Speech started! Volume: {volume:.1f}")
                
                print(f"🔊 Volume: {volume:.1f} | Speaking: True", end="\r")
            
            # Detect silence
            elif volume < SILENCE_THRESHOLD:
                if is_speaking:
                    if silence_start is None:
                        silence_start = current_time
                        print(f"\n🔇 Silence started! Volume: {volume:.1f}")
                    
                    silence_duration = current_time - silence_start
                    
                    if silence_duration > SILENCE_DURATION:
                        is_speaking = False
                        speech_start = None
                        print(f"\n✅ Turn ended! Silence duration: {silence_duration:.1f}s")
                        print("🎯 Turn detection working correctly!")
                        break
                    else:
                        print(f"🔊 Volume: {volume:.1f} | Speaking: True | Silence: {silence_duration:.1f}s", end="\r")
                else:
                    print(f"🔊 Volume: {volume:.1f} | Speaking: False", end="\r")
            
            # In between
            else:
                print(f"🔊 Volume: {volume:.1f} | Speaking: {is_speaking}", end="\r")
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Test stopped by user")
    
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    test_turn_detection() 