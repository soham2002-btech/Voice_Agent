#!/usr/bin/env python3
"""
Setup Script for Voice Pipeline Agent
====================================

This script helps users set up the voice agent system quickly.
"""

import os
import sys
import subprocess
import getpass

def print_banner():
    """Print setup banner"""
    print("🎤 Voice Pipeline Agent Setup")
    print("=" * 50)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - Compatible!")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies!")
        return False

def create_env_file():
    """Create .env file with user input"""
    print("\n🔑 Setting up API keys...")
    
    if os.path.exists(".env"):
        overwrite = input("⚠️  .env file already exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            print("📝 Skipping .env creation...")
            return True
    
    print("Please enter your API keys:")
    print("(Press Enter to skip if you don't have them yet)")
    
    openai_key = getpass.getpass("OpenAI API Key: ").strip()
    deepgram_key = getpass.getpass("Deepgram API Key: ").strip()
    
    env_content = f"""# OpenAI Configuration
OPENAI_API_KEY={openai_key}

# Deepgram Configuration
DEEPGRAM_API_KEY={deepgram_key}

# Optional: Use free TTS alternative
USE_FREE_TTS=false
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_microphone():
    """Test microphone access"""
    print("\n🎤 Testing microphone access...")
    try:
        import pyaudio
        audio = pyaudio.PyAudio()
        device_count = audio.get_device_count()
        input_devices = 0
        
        for i in range(device_count):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices += 1
                print(f"   📱 Found input device: {device_info['name']}")
        
        audio.terminate()
        
        if input_devices > 0:
            print(f"✅ Found {input_devices} microphone device(s)!")
            return True
        else:
            print("❌ No microphone devices found!")
            return False
            
    except ImportError:
        print("❌ PyAudio not installed. Run: pip install pyaudio")
        return False
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        return False

def run_quick_test():
    """Run a quick test to verify setup"""
    print("\n🧪 Running quick test...")
    try:
        # Test imports
        import numpy
        import pygame
        import openai
        import requests
        print("✅ All required modules imported successfully!")
        
        # Test .env file
        if os.path.exists(".env"):
            print("✅ .env file found!")
        else:
            print("⚠️  .env file not found. Please create it manually.")
        
        return True
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎯 Setup Complete! Next Steps:")
    print("=" * 50)
    print()
    print("1. 🔑 Get API Keys (if you haven't already):")
    print("   - OpenAI: https://platform.openai.com/api-keys")
    print("   - Deepgram: https://console.deepgram.com/")
    print()
    print("2. 🎤 Test your microphone:")
    print("   python3 scripts/microphone_diagnostic.py")
    print()
    print("3. 🎯 Run the voice agent:")
    print("   python3 scripts/continuous_voice_agent.py")
    print()
    print("4. 📖 Read the full documentation:")
    print("   cat README.md")
    print()
    print("🚀 Happy voice interacting!")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Test microphone
    if not test_microphone():
        print("⚠️  Microphone test failed. You may need to check permissions.")
    
    # Run quick test
    if not run_quick_test():
        print("⚠️  Quick test failed. Check the error messages above.")
    
    # Print next steps
    print_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1) 