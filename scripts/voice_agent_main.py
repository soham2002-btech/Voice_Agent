#!/usr/bin/env python3
"""
Voice Agent Main Script
======================

Main entry point for the restructured voice agent system.
"""

import asyncio
import sys
import os

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, src_path)

# Import the main agent
from agent import VoiceAgent


async def main():
    """Main function"""
    try:
        # Create and start voice agent
        agent = VoiceAgent()
        await agent.start()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 