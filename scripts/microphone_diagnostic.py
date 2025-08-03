#!/usr/bin/env python3
"""
Microphone Diagnostic Tool
==========================

This script helps diagnose microphone issues and find the right input device.
"""

import pyaudio
import numpy as np
import time

def list_audio_devices():
    """List all available audio devices"""
    audio = pyaudio.PyAudio()
    
    print("🎤 Available Audio Devices:")
    print("="*50)
    
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:  # Input devices only
            print(f"Device {i}: {device_info['name']}")
            print(f"  - Max Input Channels: {device_info['maxInputChannels']}")
            print(f"  - Sample Rate: {device_info['defaultSampleRate']}")
            print(f"  - Default: {'YES' if device_info['index'] == audio.get_default_input_device_info()['index'] else 'NO'}")
            print()
    
    audio.terminate()

def test_microphone_sensitivity(device_index=None):
    """Test microphone sensitivity with different thresholds"""
    audio = pyaudio.PyAudio()
    
    if device_index is None:
        device_index = audio.get_default_input_device_info()['index']
    
    device_info = audio.get_device_info_by_index(device_index)
    print(f"🎤 Testing Device: {device_info['name']}")
    print("="*50)
    
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        input_device_index=device_index,
        frames_per_buffer=1024
    )
    
    print("Speak into your microphone to test sensitivity...")
    print("Press Ctrl+C to exit")
    print("="*50)
    
    try:
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            audio_squared = np.maximum(audio_data**2, 0)
            volume = np.sqrt(np.mean(audio_squared))
            
            # Test different thresholds
            threshold_10 = "🔴" if volume > 10 else "⚪"
            threshold_20 = "🟡" if volume > 20 else "⚪"
            threshold_30 = "🟢" if volume > 30 else "⚪"
            threshold_50 = "🔵" if volume > 50 else "⚪"
            threshold_100 = "🟣" if volume > 100 else "⚪"
            
            bar_length = 40
            filled_length = int(bar_length * min(volume / 200, 1.0))
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            
            print(f"🔊 {volume:6.1f} | {bar} | {threshold_10}{threshold_20}{threshold_30}{threshold_50}{threshold_100}", end="\r")
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\n✅ Test complete!")
    
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

def main():
    """Main diagnostic function"""
    print("🎤 Microphone Diagnostic Tool")
    print("="*50)
    
    # List devices
    list_audio_devices()
    
    # Ask user which device to test
    try:
        device_choice = input("\nEnter device number to test (or press Enter for default): ").strip()
        device_index = int(device_choice) if device_choice else None
    except ValueError:
        print("Invalid input, using default device...")
        device_index = None
    
    # Test microphone
    test_microphone_sensitivity(device_index)

if __name__ == "__main__":
    main() 