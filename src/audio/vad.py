"""
Voice Activity Detection (VAD)
=============================

Real-time voice activity detection with noise filtering and turn management.
"""

import time
import numpy as np
from typing import Dict, Any
try:
    from ..config.settings import VADConfig
except ImportError:
    from config.settings import VADConfig


class VoiceActivityDetector:
    """Voice Activity Detection with configurable parameters and noise filtering"""
    
    def __init__(self, config: VADConfig):
        self.config = config
        self.is_speaking = False
        self.silence_start = None
        self.speech_start = None
        
        # Consecutive frame counters for noise filtering
        self.consecutive_speech_frames = 0
        self.consecutive_silence_frames = 0
    
    def detect_voice_activity(self, audio_chunk: bytes) -> Dict[str, Any]:
        """
        Detect voice activity in audio chunk with noise filtering
        
        Args:
            audio_chunk: Raw audio data bytes
            
        Returns:
            Dictionary with detection results
        """
        # Calculate volume from audio data
        audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
        audio_squared = np.maximum(audio_data**2, 0)
        volume = np.sqrt(np.mean(audio_squared))
        
        current_time = time.time()
        
        # Detect speech with consecutive frame counting
        if volume > self.config.speech_threshold:
            self.consecutive_speech_frames += 1
            self.consecutive_silence_frames = 0
            
            # Only start speaking if we have enough consecutive speech frames
            if not self.is_speaking and self.consecutive_speech_frames >= self.config.speech_frame_threshold:
                self.is_speaking = True
                self.speech_start = current_time
                self.silence_start = None
                print(f"\n🎤 Speech started! Volume: {volume:.1f} (after {self.consecutive_speech_frames} frames)")
            
            return {
                "is_speaking": self.is_speaking,
                "volume": volume,
                "speech_duration": current_time - self.speech_start if self.speech_start and self.is_speaking else 0,
                "silence_duration": 0,
                "turn_ended": False
            }
        
        # Detect silence with consecutive frame counting
        elif volume < self.config.silence_threshold:
            self.consecutive_silence_frames += 1
            self.consecutive_speech_frames = 0
            
            if self.is_speaking:
                # Only start silence detection if we have enough consecutive silence frames
                if self.consecutive_silence_frames >= self.config.silence_frame_threshold:
                    if self.silence_start is None:
                        self.silence_start = current_time
                        print(f"🔇 Silence confirmed! Volume: {volume:.1f} (after {self.consecutive_silence_frames} frames)")
                    
                    silence_duration = current_time - self.silence_start
                    
                    # Check if silence is long enough to end turn
                    if silence_duration > self.config.silence_duration:
                        self.is_speaking = False
                        self.speech_start = None
                        self.silence_start = None
                        print(f"✅ Turn ended! Silence duration: {silence_duration:.1f}s")
                        return {
                            "is_speaking": False,
                            "volume": volume,
                            "speech_duration": 0,
                            "silence_duration": silence_duration,
                            "turn_ended": True
                        }
                
                # Still in speech mode during silence
                return {
                    "is_speaking": True,
                    "volume": volume,
                    "speech_duration": current_time - self.speech_start if self.speech_start else 0,
                    "silence_duration": current_time - self.silence_start if self.silence_start else 0,
                    "turn_ended": False
                }
            
            # Not speaking
            return {
                "is_speaking": False,
                "volume": volume,
                "speech_duration": 0,
                "silence_duration": current_time - self.silence_start if self.silence_start else 0,
                "turn_ended": False
            }
        
        # In between - reset counters and maintain current state
        else:
            self.consecutive_speech_frames = 0
            self.consecutive_silence_frames = 0
            
            return {
                "is_speaking": self.is_speaking,
                "volume": volume,
                "speech_duration": current_time - self.speech_start if self.speech_start and self.is_speaking else 0,
                "silence_duration": current_time - self.silence_start if self.silence_start and not self.is_speaking else 0,
                "turn_ended": False
            }
    
    def reset(self):
        """Reset the VAD state"""
        self.is_speaking = False
        self.silence_start = None
        self.speech_start = None
        self.consecutive_speech_frames = 0
        self.consecutive_silence_frames = 0 