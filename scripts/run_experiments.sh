#!/bin/bash

# Run Voice Pipeline Agent Experiments
set -e

echo "🎯 Starting Voice Pipeline Agent Experiments..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📋 Installing dependencies..."
pip install -r requirements.txt

# Check environment variables
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please copy env.example to .env and configure your API keys."
    exit 1
fi

# Load environment variables
export $(cat .env | xargs)

# Create results directory
mkdir -p results

# Run experiments
echo "🧪 Running baseline experiment..."
EXPERIMENT_NAME=baseline python src/experiment_runner.py

echo "🧪 Running VAD parameter tuning..."
for delay in 0.2 0.5 1.0 2.0; do
    MIN_ENDPOINTING_DELAY=$delay EXPERIMENT_NAME="vad_min_delay_$delay" python src/experiment_runner.py
done

echo "🧪 Running STT endpointing experiments..."
for confidence in 0.6 0.8 0.9; do
    TURN_DETECTION_MODE=stt END_OF_TURN_CONFIDENCE_THRESHOLD=$confidence EXPERIMENT_NAME="stt_confidence_$confidence" python src/experiment_runner.py
done

echo "🧪 Running multilingual turn detector..."
TURN_DETECTION_MODE=multilingual EXPERIMENT_NAME=multilingual_turn_detector python src/experiment_runner.py

echo "🧪 Running SSML enhancement test..."
USE_SSML=true EXPERIMENT_NAME=ssml_enhanced python src/experiment_runner.py

echo "🧪 Running optimized configuration..."
MIN_ENDPOINTING_DELAY=0.3 MAX_ENDPOINTING_DELAY=4.0 TURN_DETECTION_MODE=multilingual USE_SSML=true EXPERIMENT_NAME=optimized_full python src/experiment_runner.py

echo "📊 Generating comparative analysis..."
python src/experiment_runner.py --analyze-only

echo "✅ All experiments completed!"
echo "📁 Results saved to: ./results/" 