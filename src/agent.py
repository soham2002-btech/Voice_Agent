"""
Voice Agent
==========

Main voice agent class that orchestrates all components.
"""

import asyncio
import os
import time
from typing import Optional

try:
    from .config.settings import settings
    from .audio.vad import VoiceActivityDetector
    from .audio.recorder import AudioRecorder
    from .services.stt import STTService
    from .services.llm import LLMService
    from .services.tts import TTSService
    from .utils.metrics import MetricsCollector
except ImportError:
    from config.settings import settings
    from audio.vad import VoiceActivityDetector
    from audio.recorder import AudioRecorder
    from services.stt import STTService
    from services.llm import LLMService
    from services.tts import TTSService
    from utils.metrics import MetricsCollector


class VoiceAgent:
    """Main voice agent that orchestrates all components"""
    
    def __init__(self):
        # Validate configuration
        if not settings.validate():
            raise ValueError("Invalid configuration. Please check your API keys.")
        
        # Initialize components
        self.vad = VoiceActivityDetector(settings.vad)
        self.audio_recorder = AudioRecorder(settings.audio)
        self.stt_service = STTService(settings.stt)
        self.llm_service = LLMService(settings.llm)
        self.tts_service = TTSService(settings.tts)
        self.metrics = MetricsCollector()
        
        # State management
        self.is_running = False
        self.current_turn_start: Optional[float] = None
    
    async def start(self):
        """Start the voice agent"""
        print("🎯 Voice Pipeline Agent")
        print("=" * 50)
        settings.print_summary()
        print("=" * 50)
        
        # Test API connections
        await self._test_connections()
        
        self.is_running = True
        print("\n🎤 Ready for continuous voice interaction!")
        print("💡 Speak naturally - the system will detect your turns")
        print("🤖 AI will respond with voice and text")
        print("🛑 Press Ctrl+C to exit")
        print("=" * 50)
        
        # Start the main loop
        await self._run_continuous_loop()
    
    async def stop(self):
        """Stop the voice agent"""
        self.is_running = False
        self.audio_recorder.stop_recording()
        self.tts_service.cleanup()
        self.metrics.end_session()
        print("\n✅ Voice agent stopped successfully!")
    
    async def _test_connections(self):
        """Test API connections"""
        print("🔍 Testing API connections...")
        
        # Test OpenAI
        try:
            test_response = await self.llm_service.generate_response("Hello")
            print("✅ OpenAI connection successful!")
        except Exception as e:
            print(f"❌ OpenAI connection failed: {e}")
            raise
        
        # Test Deepgram (create a silent audio file for testing)
        try:
            import wave
            import numpy as np
            
            # Create a silent WAV file for testing
            test_file = "test_audio.wav"
            with wave.open(test_file, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                # Create a longer silent audio file
                silent_audio = np.zeros(32000, dtype=np.int16)  # 2 seconds of silence
                wf.writeframes(silent_audio.tobytes())
            
            # Test transcription
            result = await self.stt_service.transcribe_audio(test_file)
            os.remove(test_file)
            
            # Deepgram will return empty transcript for silent audio, which is expected
            if result.get("success") or "Empty transcription result" in result.get("error", ""):
                print("✅ Deepgram connection successful!")
            else:
                print(f"❌ Deepgram connection failed: {result.get('error')}")
                raise Exception("Deepgram connection failed")
                
        except Exception as e:
            print(f"❌ Deepgram connection failed: {e}")
            raise
    
    async def _run_continuous_loop(self):
        """Run the main continuous voice processing loop"""
        self.audio_recorder.start_recording()
        
        try:
            while self.is_running:
                # Record audio chunk
                audio_chunk = self.audio_recorder.record_chunk()
                if audio_chunk is None:
                    continue
                
                # VAD processing
                vad_result = self.vad.detect_voice_activity(audio_chunk)
                
                # Debug output
                self._print_debug_info(vad_result)
                
                # Start turn if speaking detected
                if vad_result.get("is_speaking") and not self.current_turn_start:
                    self.current_turn_start = time.time()
                    self.metrics.start_turn()
                    print(f"\n🎤 Voice detected! Volume: {vad_result.get('volume', 0):.0f} - starting turn...")
                
                # End turn if silence detected
                if vad_result.get("turn_ended", False) and self.current_turn_start:
                    await self._process_turn()
                    self.current_turn_start = None
                
                # Small delay to prevent excessive CPU usage
                await asyncio.sleep(0.01)
        
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping voice agent...")
        finally:
            await self.stop()
    
    def _print_debug_info(self, vad_result: dict):
        """Print debug information for VAD"""
        volume = vad_result.get("volume", 0)
        is_speaking = vad_result.get('is_speaking', False)
        silence_duration = vad_result.get('silence_duration', 0)
        turn_ended = vad_result.get('turn_ended', False)
        
        if turn_ended:
            print(f"🎯 TURN ENDED! Volume: {volume:.1f} | Silence: {silence_duration:.1f}s")
        else:
            speech_frames = self.vad.consecutive_speech_frames
            silence_frames = self.vad.consecutive_silence_frames
            print(f"🔊 Volume: {volume:.1f} | Speaking: {is_speaking} | Speech: {speech_frames}/3 | Silence: {silence_frames}/5", end="\r")
    
    async def _process_turn(self):
        """Process a completed turn"""
        if not self.current_turn_start:
            return
        
        turn_duration = time.time() - self.current_turn_start
        print(f"🎤 Turn ended after {turn_duration:.1f}s - processing...")
        
        try:
            # Save current audio
            temp_audio_file = f"temp_audio_{int(time.time())}.wav"
            self.audio_recorder.save_audio(temp_audio_file)
            
            # STT processing
            self.metrics.record_stt_start()
            stt_result = await self.stt_service.transcribe_audio(temp_audio_file)
            self.metrics.record_stt_end(
                stt_result.get("final_transcript", ""),
                stt_result.get("final_confidence", 0.0)
            )
            
            if not stt_result.get("success") or not stt_result.get("final_transcript"):
                print("❌ No speech detected")
                self.metrics.end_turn(success=False, error="No speech detected")
                self._cleanup_temp_file(temp_audio_file)
                return
            
            transcript = stt_result["final_transcript"]
            confidence = stt_result["final_confidence"]
            
            print(f"🎤 Transcript: {transcript}")
            print(f"📊 Confidence: {confidence:.2f}")
            
            # LLM processing
            self.metrics.record_llm_start()
            response = await self.llm_service.generate_response(transcript)
            self.metrics.record_llm_end(response)
            
            # TTS processing
            self.metrics.record_tts_start()
            tts_success = await self.tts_service.speak_text(response)
            self.metrics.record_tts_end()
            
            # Display response
            print(f"\n🤖 Assistant: {response}")
            
            # End turn
            self.metrics.end_turn(success=tts_success)
            
            # Clean up temp file
            self._cleanup_temp_file(temp_audio_file)
            
        except Exception as e:
            print(f"❌ Error processing turn: {e}")
            self.metrics.end_turn(success=False, error=str(e))
    
    def _cleanup_temp_file(self, filename: str):
        """Clean up temporary audio file"""
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except:
            pass 