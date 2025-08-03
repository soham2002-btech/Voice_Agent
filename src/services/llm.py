"""
Large Language Model Service
===========================

OpenAI GPT integration for generating AI responses.
"""

import asyncio
from typing import List, Dict, Any, Optional
from openai import OpenAI
try:
    from ..config.settings import LLMConfig
except ImportError:
    from config.settings import LLMConfig


class LLMService:
    """Large Language Model service using OpenAI GPT"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = OpenAI(api_key=config.api_key)
        self.conversation_history: List[Dict[str, str]] = []
    
    async def generate_response(self, user_input: str) -> str:
        """
        Generate AI response to user input
        
        Args:
            user_input: User's transcribed speech
            
        Returns:
            AI-generated response
        """
        if not self.config.api_key:
            return self._generate_fallback_response(user_input)
        
        try:
            # Prepare conversation messages
            messages = [
                {"role": "system", "content": self.config.system_prompt}
            ]
            
            # Add conversation history
            messages.extend(self.conversation_history[-10:])  # Keep last 10 exchanges
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})
            
            # Generate response
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            print(f"❌ LLM Error: {e}")
            return self._generate_fallback_response(user_input)
    
    def _generate_fallback_response(self, user_input: str) -> str:
        """
        Generate fallback response when LLM is unavailable
        
        Args:
            user_input: User's input
            
        Returns:
            Fallback response
        """
        user_input_lower = user_input.lower()
        
        # Simple keyword-based responses
        if any(word in user_input_lower for word in ["hello", "hi", "hey"]):
            return "Hello! How can I help you today?"
        
        elif any(word in user_input_lower for word in ["how are you", "how do you do"]):
            return "I'm doing well, thank you for asking! How can I assist you?"
        
        elif any(word in user_input_lower for word in ["bye", "goodbye", "see you"]):
            return "Goodbye! Have a great day!"
        
        elif any(word in user_input_lower for word in ["thank you", "thanks"]):
            return "You're welcome! Is there anything else I can help you with?"
        
        elif "?" in user_input:
            return "That's an interesting question. Let me think about that for a moment."
        
        else:
            return "I understand what you're saying. Could you tell me more about that?"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history.copy() 