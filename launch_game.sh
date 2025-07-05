#!/bin/bash

# AWSKANOID Game Launcher
# This script launches the AWSKANOID game with proper error handling

echo "🎮 AWSKANOID - A Modern Breakout Experience"
echo "==========================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 Python version: $PYTHON_VERSION"

# Check if required packages are installed
echo "📦 Checking dependencies..."

if ! python3 -c "import pygame" 2>/dev/null; then
    echo "❌ Pygame not found. Installing..."
    pip3 install pygame
fi

if ! python3 -c "import numpy" 2>/dev/null; then
    echo "❌ NumPy not found. Installing..."
    pip3 install numpy
fi

echo "✅ All dependencies are ready!"

# Change to the game directory
cd "$(dirname "$0")"

# Launch the game
echo "🚀 Starting AWSKANOID..."
echo ""
echo "Controls:"
echo "  Arrow Keys / Mouse - Move paddle"
echo "  Spacebar - Release ball / Shoot laser"
echo "  ESC - Pause game"
echo "  F1 - Toggle FPS counter"
echo ""
echo "Have fun! Press Ctrl+C to quit."
echo ""

python3 main.py
