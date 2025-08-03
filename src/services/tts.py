"""
Text-to-Speech Service
=====================

OpenAI TTS integration with SSML enhancement.
"""

import asyncio
import os
import pygame
from typing import Optional
from openai import OpenAI
try:
    from ..config.settings import TTSConfig
    from ..utils.ssml import SSMLEnhancer
except ImportError:
    from config.settings import TTSConfig
    from utils.ssml import SSMLEnhancer


class TTSService:
    """Text-to-Speech service using OpenAI TTS with SSML enhancement"""
    
    def __init__(self, config: TTSConfig):
        self.config = config
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.ssml_enhancer = SSMLEnhancer() if config.use_ssml else None
        self.audio_dir = "temp_audio"
        
        # Create temp directory if it doesn't exist
        os.makedirs(self.audio_dir, exist_ok=True)
        
        # Initialize pygame mixer
        pygame.mixer.init()
    
    async def speak_text(self, text: str, context: str = "general") -> bool:
        """
        Convert text to speech and play it
        
        Args:
            text: Text to convert to speech
            context: Context for SSML enhancement
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Enhance text with SSML if enabled
            if self.ssml_enhancer and self.config.use_ssml:
                enhanced_text = self.ssml_enhancer.enhance_text(text, context)
                print(f"🎵 SSML Enhanced: {enhanced_text}")
            else:
                enhanced_text = text
            
            # Generate speech
            audio_file = await self._generate_speech(enhanced_text)
            if not audio_file:
                return False
            
            # Play the audio
            await self._play_audio(audio_file)
            
            # Clean up temp file
            try:
                os.remove(audio_file)
            except:
                pass
            
            return True
            
        except Exception as e:
            print(f"❌ TTS Error: {e}")
            return False
    
    async def _generate_speech(self, text: str) -> Optional[str]:
        """
        Generate speech from text using OpenAI TTS
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Path to generated audio file or None if failed
        """
        try:
            # Remove SSML tags for OpenAI TTS (it doesn't support SSML)
            clean_text = self._remove_ssml_tags(text)
            print(f"🔊 Converting to speech: '{clean_text}'")
            
            response = await asyncio.to_thread(
                self.client.audio.speech.create,
                model="tts-1",
                voice=self.config.voice,
                input=clean_text
            )
            
            # Save to temporary file
            timestamp = int(asyncio.get_event_loop().time())
            audio_file = os.path.join(self.audio_dir, f"speech_{timestamp}.mp3")
            
            with open(audio_file, "wb") as f:
                f.write(response.content)
            
            return audio_file
            
        except Exception as e:
            print(f"❌ Speech generation error: {e}")
            return None
    
    async def _play_audio(self, audio_file: str):
        """
        Play audio file using pygame
        
        Args:
            audio_file: Path to audio file
        """
        try:
            # Load and play audio
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for audio to finish
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
                
        except Exception as e:
            print(f"❌ Audio playback error: {e}")
    
    def _remove_ssml_tags(self, text: str) -> str:
        """
        Remove SSML tags from text for OpenAI TTS
        
        Args:
            text: Text with SSML tags
            
        Returns:
            Clean text without SSML tags
        """
        import re
        
        # Remove common SSML tags
        text = re.sub(r'<speak>|</speak>', '', text)
        text = re.sub(r'<prosody[^>]*>|</prosody>', '', text)
        text = re.sub(r'<emphasis[^>]*>|</emphasis>', '', text)
        text = re.sub(r'<say-as[^>]*>|</say-as>', '', text)
        text = re.sub(r'<break[^>]*/>', ' ', text)
        
        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def cleanup(self):
        """Clean up resources"""
        pygame.mixer.quit() 