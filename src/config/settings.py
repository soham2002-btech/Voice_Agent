"""
Voice Agent Configuration Settings
=================================

Centralized configuration management for the voice agent system.
"""

import os
from dataclasses import dataclass
from typing import Optional

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, use system environment variables


@dataclass
class VADConfig:
    """Voice Activity Detection configuration"""
    min_endpointing_delay: float = 0.5
    max_endpointing_delay: float = 6.0
    silence_threshold: int = 25
    speech_threshold: int = 45
    silence_duration: float = 1.0
    speech_frame_threshold: int = 3
    silence_frame_threshold: int = 5


@dataclass
class TurnDetectionConfig:
    """Turn detection configuration"""
    mode: str = "vad"
    confidence_threshold: float = 0.7
    min_silence_duration: float = 1.0
    max_turn_silence: float = 10.0


@dataclass
class STTConfig:
    """Speech-to-Text configuration"""
    api_key: Optional[str] = None
    language: str = "en-US"
    model: str = "nova-2"
    smart_format: bool = True
    punctuate: bool = True


@dataclass
class TTSConfig:
    """Text-to-Speech configuration"""
    voice: str = "alloy"
    use_ssml: bool = True
    speed: float = 1.0
    quality: str = "hd"


@dataclass
class LLMConfig:
    """Large Language Model configuration"""
    api_key: Optional[str] = None
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 150
    system_prompt: str = "You are a helpful voice assistant. Keep responses concise and natural for speech."


@dataclass
class AudioConfig:
    """Audio processing configuration"""
    sample_rate: int = 16000
    channels: int = 1
    chunk_size: int = 1024
    format: str = "paInt16"


class Settings:
    """Main settings class that loads configuration from environment"""
    
    def __init__(self):
        # Load API keys from environment
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
        self.use_free_tts = os.getenv("USE_FREE_TTS", "false").lower() == "true"
        
        # Initialize component configurations
        self.vad = VADConfig()
        self.turn_detection = TurnDetectionConfig()
        self.stt = STTConfig(api_key=self.deepgram_api_key)
        self.tts = TTSConfig()
        self.llm = LLMConfig(api_key=self.openai_api_key)
        self.audio = AudioConfig()
    
    def validate(self) -> bool:
        """Validate that all required settings are present"""
        if not self.openai_api_key:
            print("❌ OpenAI API key not found in environment variables")
            return False
        
        if not self.deepgram_api_key:
            print("❌ Deepgram API key not found in environment variables")
            return False
        
        return True
    
    def print_summary(self):
        """Print a summary of current configuration"""
        print("🔧 Configuration Summary:")
        print(f"   VAD: speech_threshold={self.vad.speech_threshold}, silence_threshold={self.vad.silence_threshold}")
        print(f"   Turn Detection: mode={self.turn_detection.mode}, silence_duration={self.turn_detection.min_silence_duration}s")
        print(f"   STT: model={self.stt.model}, language={self.stt.language}")
        print(f"   TTS: voice={self.tts.voice}, ssml={self.tts.use_ssml}")
        print(f"   LLM: model={self.llm.model}, temperature={self.llm.temperature}")
        print(f"   Audio: rate={self.audio.sample_rate}Hz, channels={self.audio.channels}")


# Global settings instance
settings = Settings() 