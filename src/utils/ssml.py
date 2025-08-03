"""
SSML Enhancement Utility
=======================

Text enhancement with SSML tags for better TTS output.
"""

from typing import List


class SSMLEnhancer:
    """SSML enhancement for better TTS output"""
    
    def __init__(self):
        self.important_words = [
            "important", "critical", "essential", "key", "vital", "urgent",
            "significant", "crucial", "necessary", "required"
        ]
        self.technical_terms = [
            "API", "URL", "HTTP", "JSON", "XML", "SQL", "AI", "ML", "GPT",
            "CPU", "GPU", "RAM", "SSD", "USB", "WiFi", "Bluetooth", "VPN"
        ]
        self.emotional_words = [
            "amazing", "incredible", "fantastic", "wonderful", "terrible",
            "horrible", "excellent", "perfect", "awful", "brilliant"
        ]
    
    def enhance_text(self, text: str, context: str = "general") -> str:
        """
        Enhance text with SSML tags
        
        Args:
            text: Original text
            context: Context for enhancement (general, technical, casual)
            
        Returns:
            Enhanced text with SSML tags
        """
        enhanced = text
        
        # Add emphasis to important words
        enhanced = self._add_emphasis(enhanced)
        
        # Add say-as for technical terms and acronyms
        enhanced = self._add_say_as(enhanced)
        
        # Add prosody for questions and exclamations
        enhanced = self._add_prosody(enhanced)
        
        # Add breaks for better pacing
        enhanced = self._add_breaks(enhanced)
        
        # Context-specific enhancements
        enhanced = self._add_context_enhancements(enhanced, context)
        
        # Wrap in speak tag
        return f'<speak>{enhanced}</speak>'
    
    def _add_emphasis(self, text: str) -> str:
        """Add emphasis to important words"""
        for word in self.important_words + self.emotional_words:
            if word in text.lower():
                # Use case-insensitive replacement
                import re
                pattern = re.compile(re.escape(word), re.IGNORECASE)
                text = pattern.sub(f'<emphasis level="moderate">{word}</emphasis>', text)
        
        return text
    
    def _add_say_as(self, text: str) -> str:
        """Add say-as for technical terms and acronyms"""
        for term in self.technical_terms:
            if term in text:
                text = text.replace(term, f'<say-as interpret-as="spell-out">{term}</say-as>')
        
        return text
    
    def _add_prosody(self, text: str) -> str:
        """Add prosody for questions and exclamations"""
        # Questions
        if text.strip().endswith('?'):
            text = f'<prosody pitch="+2st" rate="medium">{text}</prosody>'
        
        # Exclamations
        elif text.strip().endswith('!'):
            text = f'<prosody pitch="+3st" rate="fast">{text}</prosody>'
        
        return text
    
    def _add_breaks(self, text: str) -> str:
        """Add breaks for better pacing"""
        # Add breaks after sentences
        text = text.replace('. ', '.<break time="0.3s"/> ')
        text = text.replace('! ', '!<break time="0.3s"/> ')
        text = text.replace('? ', '?<break time="0.3s"/> ')
        
        # Add breaks after commas
        text = text.replace(', ', ',<break time="0.2s"/> ')
        
        # Add breaks after colons and semicolons
        text = text.replace(': ', ':<break time="0.2s"/> ')
        text = text.replace('; ', ';<break time="0.2s"/> ')
        
        return text
    
    def _add_context_enhancements(self, text: str, context: str) -> str:
        """Add context-specific enhancements"""
        if context == "technical":
            text = f'<prosody rate="slow">{text}</prosody>'
        elif context == "casual":
            text = f'<prosody rate="fast">{text}</prosody>'
        elif context == "formal":
            text = f'<prosody rate="medium" pitch="-1st">{text}</prosody>'
        elif context == "excited":
            text = f'<prosody rate="fast" pitch="+2st">{text}</prosody>'
        
        return text 