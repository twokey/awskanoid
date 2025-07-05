#!/usr/bin/env python3
"""
Demo script to showcase the new control selection feature
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_control_settings():
    """Demonstrate the control settings functionality"""
    print("🎮 AWSKANOID Control Selection Feature Demo")
    print("=" * 50)
    
    from utils.settings import SettingsManager
    from utils.constants import CONTROL_MODE_KEYBOARD, CONTROL_MODE_MOUSE
    
    # Create settings manager
    settings = SettingsManager()
    
    print(f"📋 Current control mode: {settings.get_control_mode().upper()}")
    print()
    
    print("🔄 Testing control mode switching...")
    
    # Demonstrate keyboard mode
    settings.set_control_mode(CONTROL_MODE_KEYBOARD)
    print(f"✓ Set to KEYBOARD mode")
    print(f"  - Keyboard enabled: {settings.is_keyboard_mode()}")
    print(f"  - Mouse enabled: {settings.is_mouse_mode()}")
    print()
    
    # Demonstrate mouse mode
    settings.set_control_mode(CONTROL_MODE_MOUSE)
    print(f"✓ Set to MOUSE mode")
    print(f"  - Keyboard enabled: {settings.is_keyboard_mode()}")
    print(f"  - Mouse enabled: {settings.is_mouse_mode()}")
    print()
    
    # Demonstrate toggle
    print("🔄 Testing toggle functionality...")
    original_mode = settings.get_control_mode()
    settings.toggle_control_mode()
    new_mode = settings.get_control_mode()
    print(f"✓ Toggled from {original_mode.upper()} to {new_mode.upper()}")
    print()
    
    print("💾 Settings are automatically saved to 'game_settings.json'")
    print()
    
    print("🎯 How to use in game:")
    print("1. Start the game: python3 main.py")
    print("2. Click 'Settings' from main menu")
    print("3. Click 'Controls' to choose your preferred input method")
    print("4. Select either 'Keyboard' or 'Mouse'")
    print("5. Your choice is saved and used in gameplay")
    print()
    
    print("🎮 Control Behavior:")
    print("📱 KEYBOARD MODE:")
    print("   • LEFT/RIGHT arrow keys move paddle")
    print("   • Mouse movement ignored during gameplay")
    print("   • ESC always works for pause")
    print()
    print("🖱️  MOUSE MODE:")
    print("   • Mouse movement controls paddle")
    print("   • Arrow keys ignored during gameplay")
    print("   • ESC always works for pause")
    print()
    
    print("✨ Benefits:")
    print("• No accidental input from unused control method")
    print("• Cleaner, more predictable gameplay")
    print("• Player can choose their preferred style")
    print("• Settings persist between game sessions")

if __name__ == "__main__":
    demo_control_settings()
