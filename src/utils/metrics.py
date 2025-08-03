"""
Metrics Collection Utility
=========================

Performance monitoring and metrics collection.
"""

import time
from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class TurnMetrics:
    """Metrics for a single conversation turn"""
    turn_id: int
    start_time: float
    end_time: float = 0.0
    stt_latency: float = 0.0
    llm_latency: float = 0.0
    tts_latency: float = 0.0
    total_latency: float = 0.0
    stt_confidence: float = 0.0
    transcript: str = ""
    response: str = ""
    success: bool = True
    error: str = ""


@dataclass
class SessionMetrics:
    """Metrics for the entire conversation session"""
    session_id: str
    start_time: float = field(default_factory=time.time)
    end_time: float = 0.0
    total_turns: int = 0
    successful_turns: int = 0
    failed_turns: int = 0
    total_duration: float = 0.0
    average_stt_latency: float = 0.0
    average_llm_latency: float = 0.0
    average_tts_latency: float = 0.0
    average_total_latency: float = 0.0
    average_confidence: float = 0.0
    turns: List[TurnMetrics] = field(default_factory=list)


class MetricsCollector:
    """Collects and manages performance metrics"""
    
    def __init__(self, session_id: str = None):
        self.session_id = session_id or f"session_{int(time.time())}"
        self.session = SessionMetrics(session_id=self.session_id)
        self.current_turn: TurnMetrics = None
        self.turn_counter = 0
    
    def start_turn(self) -> int:
        """Start a new turn and return turn ID"""
        self.turn_counter += 1
        self.current_turn = TurnMetrics(
            turn_id=self.turn_counter,
            start_time=time.time()
        )
        return self.turn_counter
    
    def record_stt_start(self):
        """Record STT processing start"""
        if self.current_turn:
            self.current_turn.stt_start_time = time.time()
    
    def record_stt_end(self, transcript: str, confidence: float):
        """Record STT processing end"""
        if self.current_turn:
            self.current_turn.stt_latency = (time.time() - self.current_turn.stt_start_time) * 1000
            self.current_turn.transcript = transcript
            self.current_turn.stt_confidence = confidence
    
    def record_llm_start(self):
        """Record LLM processing start"""
        if self.current_turn:
            self.current_turn.llm_start_time = time.time()
    
    def record_llm_end(self, response: str):
        """Record LLM processing end"""
        if self.current_turn:
            self.current_turn.llm_latency = (time.time() - self.current_turn.llm_start_time) * 1000
            self.current_turn.response = response
    
    def record_tts_start(self):
        """Record TTS processing start"""
        if self.current_turn:
            self.current_turn.tts_start_time = time.time()
    
    def record_tts_end(self):
        """Record TTS processing end"""
        if self.current_turn:
            self.current_turn.tts_latency = (time.time() - self.current_turn.tts_start_time) * 1000
    
    def end_turn(self, success: bool = True, error: str = ""):
        """End the current turn"""
        if self.current_turn:
            self.current_turn.end_time = time.time()
            self.current_turn.total_latency = (self.current_turn.end_time - self.current_turn.start_time) * 1000
            self.current_turn.success = success
            self.current_turn.error = error
            
            # Add to session
            self.session.turns.append(self.current_turn)
            self.session.total_turns += 1
            
            if success:
                self.session.successful_turns += 1
            else:
                self.session.failed_turns += 1
            
            # Print turn summary
            self._print_turn_summary(self.current_turn)
            
            self.current_turn = None
    
    def end_session(self):
        """End the session and calculate final metrics"""
        self.session.end_time = time.time()
        self.session.total_duration = self.session.end_time - self.session.start_time
        
        if self.session.turns:
            # Calculate averages
            stt_latencies = [t.stt_latency for t in self.session.turns if t.success]
            llm_latencies = [t.llm_latency for t in self.session.turns if t.success]
            tts_latencies = [t.tts_latency for t in self.session.turns if t.success]
            total_latencies = [t.total_latency for t in self.session.turns if t.success]
            confidences = [t.stt_confidence for t in self.session.turns if t.success]
            
            if stt_latencies:
                self.session.average_stt_latency = sum(stt_latencies) / len(stt_latencies)
            if llm_latencies:
                self.session.average_llm_latency = sum(llm_latencies) / len(llm_latencies)
            if tts_latencies:
                self.session.average_tts_latency = sum(tts_latencies) / len(tts_latencies)
            if total_latencies:
                self.session.average_total_latency = sum(total_latencies) / len(total_latencies)
            if confidences:
                self.session.average_confidence = sum(confidences) / len(confidences)
        
        self._print_session_summary()
    
    def _print_turn_summary(self, turn: TurnMetrics):
        """Print summary for a single turn"""
        print(f"\n📊 Turn {turn.turn_id} Summary:")
        print(f"   STT: {turn.stt_latency:.1f}ms (confidence: {turn.stt_confidence:.2f})")
        print(f"   LLM: {turn.llm_latency:.1f}ms")
        print(f"   TTS: {turn.tts_latency:.1f}ms")
        print(f"   Total: {turn.total_latency:.1f}ms")
        if not turn.success:
            print(f"   ❌ Error: {turn.error}")
    
    def _print_session_summary(self):
        """Print summary for the entire session"""
        print(f"\n📈 Session Summary:")
        print(f"   Duration: {self.session.total_duration:.1f}s")
        print(f"   Total Turns: {self.session.total_turns}")
        print(f"   Successful: {self.session.successful_turns}")
        print(f"   Failed: {self.session.failed_turns}")
        print(f"   Success Rate: {(self.session.successful_turns/self.session.total_turns*100):.1f}%")
        print(f"   Avg STT Latency: {self.session.average_stt_latency:.1f}ms")
        print(f"   Avg LLM Latency: {self.session.average_llm_latency:.1f}ms")
        print(f"   Avg TTS Latency: {self.session.average_tts_latency:.1f}ms")
        print(f"   Avg Total Latency: {self.session.average_total_latency:.1f}ms")
        print(f"   Avg Confidence: {self.session.average_confidence:.2f}")
    
    def get_session_metrics(self) -> SessionMetrics:
        """Get the session metrics"""
        return self.session 