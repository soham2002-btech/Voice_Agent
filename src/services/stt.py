"""
Speech-to-Text Service
=====================

Deepgram integration for speech transcription.
"""

import asyncio
import os
import requests
import urllib3
from typing import Dict, Any, Optional
try:
    from ..config.settings import STTConfig
except ImportError:
    from config.settings import STTConfig

# Disable SSL warnings for Deepgram
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class STTService:
    """Speech-to-Text service using Deepgram API"""
    
    def __init__(self, config: STTConfig):
        self.config = config
        self.api_key = config.api_key
        self.base_url = "https://api.deepgram.com/v1/listen"
    
    async def transcribe_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe audio file using Deepgram
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Transcription result dictionary
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "Deepgram API key not configured"
            }
        
        try:
            headers = {
                "Authorization": f"Token {self.api_key}",
                "Content-Type": "audio/wav"
            }
            
            # Prepare request parameters
            params = {
                "model": self.config.model,
                "language": self.config.language,
                "smart_format": str(self.config.smart_format).lower(),
                "punctuate": str(self.config.punctuate).lower()
            }
            
            with open(audio_file_path, 'rb') as audio_file:
                response = await asyncio.to_thread(
                    requests.post,
                    self.base_url,
                    headers=headers,
                    params=params,
                    data=audio_file,
                    verify=False,
                    timeout=30
                )
            
            if response.status_code == 200:
                return self._parse_response(response.json())
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Transcription error: {e}"
            }
    
    def _parse_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Deepgram API response
        
        Args:
            result: Raw API response
            
        Returns:
            Parsed transcription result
        """
        try:
            if 'results' not in result:
                return {
                    "success": False,
                    "error": "Invalid response format"
                }
            
            # Extract transcription from results
            channels = result['results'].get('channels', [])
            if not channels:
                return {
                    "success": False,
                    "error": "No audio channels found"
                }
            
            alternatives = channels[0].get('alternatives', [])
            if not alternatives:
                return {
                    "success": False,
                    "error": "No transcription alternatives found"
                }
            
            # Get the best alternative
            best_alternative = alternatives[0]
            transcript = best_alternative.get('transcript', '').strip()
            confidence = best_alternative.get('confidence', 0.0)
            
            if not transcript:
                return {
                    "success": False,
                    "error": "Empty transcription result"
                }
            
            return {
                "success": True,
                "final_transcript": transcript,
                "final_confidence": confidence,
                "partial_transcript": transcript,
                "partial_confidence": confidence,
                "turn_ended": True
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Response parsing error: {e}"
            } 