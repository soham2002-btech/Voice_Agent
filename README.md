# 🎤 LiveKit Voice Pipeline Agent with Advanced Tuning and Benchmarking

A comprehensive real-time voice interaction system that combines Voice Activity Detection (VAD), Speech-to-Text (STT), Large Language Model (LLM) processing, and Text-to-Speech (TTS) with SSML enhancements.

## 🚀 Features

### Core Capabilities
- **🎤 Real-time Voice Detection**: Advanced VAD with noise filtering and consecutive frame counting
- **🗣️ Speech-to-Text**: Deepgram integration with high accuracy (92-97% confidence)
- **🤖 AI Responses**: OpenAI GPT-4 powered intelligent conversations
- **🎵 Text-to-Speech**: OpenAI TTS with SSML enhancements for natural speech
- **🔄 Continuous Loop**: Never-ending conversation until manually stopped
- **⚡ Performance Monitoring**: Real-time latency tracking for STT, LLM, and TTS

### Advanced Features
- **🎯 Turn Detection**: Automatic turn ending after silence detection
- **🔇 Noise Filtering**: Consecutive frame counting to avoid false triggers
- **🎨 SSML Enhancement**: Automatic prosody, emphasis, and pacing improvements
- **📊 Metrics Collection**: Detailed performance analytics
- **🎛️ Configurable Parameters**: Adjustable VAD thresholds and timing

## 📋 Prerequisites

### Required Software
- Python 3.9 or higher
- pip (Python package manager)
- Microphone access

### Required API Keys
- **OpenAI API Key**: For GPT-4 responses and TTS
- **Deepgram API Key**: For speech-to-text transcription

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd voice-pipeline-agent
```

### 2. Install Dependencies
```bash
# Option 1: Automatic setup (recommended)
python3 setup.py

# Option 2: Manual installation
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root:
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Deepgram Configuration
DEEPGRAM_API_KEY=your_deepgram_api_key_here

# Optional: Use free TTS alternative
USE_FREE_TTS=false
```

### 4. Get API Keys

#### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Go to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

#### Deepgram API Key
1. Visit [Deepgram](https://deepgram.com/)
2. Create an account or sign in
3. Go to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

## 🎯 Quick Start

### Run the Main Voice Agent
```bash
# New restructured version (recommended)
python3 scripts/voice_agent_main.py

# Legacy version
python3 scripts/continuous_voice_agent.py
```

### Test Voice Detection
```bash
python3 scripts/voice_calibration.py
```

### Test Turn Detection
```bash
python3 scripts/test_turn_detection.py
```

### Diagnose Microphone Issues
```bash
python3 scripts/microphone_diagnostic.py
```

## 📖 Usage Guide

### Basic Usage
1. **Start the voice agent**:
   ```bash
   python3 scripts/continuous_voice_agent.py
   ```

2. **Wait for initialization**:
   - The system will test API connections
   - You'll see "Ready for continuous voice interaction!"

3. **Start speaking**:
   - Speak naturally into your microphone
   - The system will detect your voice and start a turn
   - You'll see: `🎤 Voice detected! Volume: XX - starting turn...`

4. **Complete your turn**:
   - Finish speaking your message
   - Stop speaking for 1 second
   - The system will process your speech and respond

5. **Listen to the response**:
   - The AI will respond with both text and voice
   - Wait for the response to complete
   - The system is ready for your next turn

6. **Exit the system**:
   - Press `Ctrl+C` to stop the voice agent

### Understanding the Output

#### Voice Detection Status
```
🔊 Volume: 45.2 | Speaking: True | Speech: 3/3 | Silence: 0/5
```
- **Volume**: Current audio level (0-100+)
- **Speaking**: Whether speech is detected
- **Speech: 3/3**: Consecutive speech frames (needs 3 to start)
- **Silence: 0/5**: Consecutive silence frames (needs 5 to end)

#### Turn Processing
```
🎤 Speech started! Volume: 45.2 (after 3 frames)
🔇 Silence confirmed! Volume: 12.1 (after 5 frames)
✅ Turn ended! Silence duration: 1.2s
🎤 Turn ended after 8.5s - processing...
```

#### Performance Metrics
```
🎤 Transcript: Hello, how are you today?
📊 Confidence: 0.95
🤖 Assistant: Hello! I'm doing well, thank you for asking...
⏱️  STT: 4150.2ms, LLM: 2340.1ms, TTS: 28450.3ms
```

## ⚙️ Configuration

### VAD Parameters
Edit `scripts/continuous_voice_agent.py` to adjust voice detection:

```python
class VADConfig:
    def __init__(self):
        self.min_endpointing_delay = 0.5      # Minimum turn duration
        self.max_endpointing_delay = 6.0      # Maximum turn duration
        self.silence_threshold = 25           # Volume level for silence detection
        self.speech_threshold = 45            # Volume level for speech detection
        self.silence_duration = 1.0           # Seconds of silence to end turn
```

### Frame Counting (Noise Filtering)
```python
self.speech_frame_threshold = 3   # Consecutive speech frames needed to start
self.silence_frame_threshold = 5  # Consecutive silence frames needed to end
```

### TTS Configuration
```python
class AdvancedTTS:
    def __init__(self, use_ssml: bool = True, voice: str = "alloy"):
        # Available voices: "alloy", "echo", "fable", "onyx", "nova", "shimmer"
```

## 🔧 Troubleshooting

### Voice Not Detected
1. **Check microphone permissions**:
   - Ensure your application has microphone access
   - Test with `python3 scripts/microphone_diagnostic.py`

2. **Adjust sensitivity**:
   - Lower `speech_threshold` if voice is too quiet
   - Increase `speech_threshold` if background noise triggers false starts

3. **Check volume levels**:
   - Run calibration: `python3 scripts/voice_calibration.py`
   - Ensure your speech volume is above the threshold

### False Triggers (Background Noise)
1. **Increase thresholds**:
   - Raise `speech_threshold` to 50-60
   - Raise `silence_threshold` to 30-35

2. **Adjust frame counting**:
   - Increase `speech_frame_threshold` to 5
   - Increase `silence_frame_threshold` to 7

### Turn Not Ending
1. **Check silence duration**:
   - Ensure you're stopping for at least 1 second
   - Increase `silence_duration` if needed

2. **Verify silence detection**:
   - Check if volume drops below `silence_threshold`
   - Run diagnostic: `python3 scripts/test_turn_detection.py`

### API Errors
1. **Check API keys**:
   - Verify keys are correct in `.env` file
   - Ensure sufficient API credits

2. **Network issues**:
   - Check internet connection
   - Verify API endpoints are accessible

## 📊 Performance Optimization

### Latency Optimization
- **STT Latency**: 4-16 seconds (Deepgram processing)
- **LLM Latency**: 2-4 seconds (OpenAI GPT-4)
- **TTS Latency**: 20-55 seconds (OpenAI TTS)

### Quality vs Speed Trade-offs
- **Lower thresholds**: Faster detection, more false triggers
- **Higher thresholds**: Slower detection, fewer false triggers
- **More frame counting**: Better noise filtering, slower response
- **Less frame counting**: Faster response, more sensitive to noise

## 🎨 SSML Enhancements

The system automatically enhances TTS output with SSML tags:

### Automatic Enhancements
- **Questions**: `<prosody pitch="+2st" rate="medium">`
- **Exclamations**: `<prosody pitch="+3st" rate="fast">`
- **Technical Terms**: `<say-as interpret-as="spell-out">AI</say-as>`
- **Pauses**: `<break time="0.2s"/>` and `<break time="0.3s"/>`
- **Emphasis**: `<emphasis level="moderate">important</emphasis>`

### Custom SSML
You can modify `SSMLEnhancer` class to add custom enhancements:

```python
def enhance_text(self, text: str, context: str = "general") -> str:
    # Add your custom SSML logic here
    enhanced = text
    # ... your enhancements
    return f'<speak>{enhanced}</speak>'
```

## 📁 Project Structure

```
voice-pipeline-agent/
├── src/                              # Main source code
│   ├── __init__.py                   # Package initialization
│   ├── agent.py                      # Main voice agent orchestrator
│   ├── config/                       # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py               # Centralized settings
│   ├── audio/                        # Audio processing
│   │   ├── __init__.py
│   │   ├── vad.py                    # Voice Activity Detection
│   │   └── recorder.py               # Audio recording
│   ├── services/                     # External API services
│   │   ├── __init__.py
│   │   ├── stt.py                    # Speech-to-Text service
│   │   ├── llm.py                    # Large Language Model service
│   │   └── tts.py                    # Text-to-Speech service
│   └── utils/                        # Utility functions
│       ├── __init__.py
│       ├── ssml.py                   # SSML enhancement
│       └── metrics.py                # Performance metrics
├── scripts/                          # Scripts and tools
│   ├── voice_agent_main.py           # New main entry point
│   ├── continuous_voice_agent.py     # Legacy voice agent
│   ├── voice_calibration.py          # Voice sensitivity testing
│   ├── test_turn_detection.py        # Turn detection testing
│   └── microphone_diagnostic.py      # Microphone troubleshooting
├── requirements.txt                  # Python dependencies
├── setup.py                          # Automated setup script
├── .env                              # Environment variables
└── README.md                         # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenAI**: For GPT-4 and TTS services
- **Deepgram**: For speech-to-text transcription
- **PyAudio**: For audio input/output
- **Pygame**: For audio playback

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run diagnostic scripts
3. Check API key validity
4. Verify microphone permissions
5. Review error messages in the console

## 🔄 Updates

Stay updated with the latest features and improvements by:
- Checking the repository regularly
- Following the changelog
- Testing new configurations
- Providing feedback and suggestions

---

**Happy Voice Interacting! 🎤🤖** 