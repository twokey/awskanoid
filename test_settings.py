#!/usr/bin/env python3
"""
Test script to verify the new control settings functionality
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_settings_manager():
    """Test the settings manager functionality"""
    print("Testing Settings Manager...")
    
    try:
        from utils.settings import SettingsManager
        from utils.constants import CONTROL_MODE_KEYBOARD, CONTROL_MODE_MOUSE
        
        # Create settings manager
        settings = SettingsManager()
        print("✓ Settings manager created successfully")
        
        # Test default control mode
        default_mode = settings.get_control_mode()
        print(f"✓ Default control mode: {default_mode}")
        
        # Test setting keyboard mode
        settings.set_control_mode(CONTROL_MODE_KEYBOARD)
        assert settings.is_keyboard_mode() == True
        assert settings.is_mouse_mode() == False
        print("✓ Keyboard mode set and verified")
        
        # Test setting mouse mode
        settings.set_control_mode(CONTROL_MODE_MOUSE)
        assert settings.is_keyboard_mode() == False
        assert settings.is_mouse_mode() == True
        print("✓ Mouse mode set and verified")
        
        # Test toggle functionality
        settings.toggle_control_mode()
        assert settings.is_keyboard_mode() == True
        print("✓ Control mode toggle works")
        
        return True
        
    except Exception as e:
        print(f"✗ Settings manager test failed: {e}")
        return False

def test_menu_imports():
    """Test that new menu classes can be imported"""
    print("\nTesting Menu Imports...")
    
    try:
        from ui.menu import SettingsMenu, ControlSettingsMenu
        from utils.settings import SettingsManager
        
        # Test menu creation
        settings_manager = SettingsManager()
        settings_menu = SettingsMenu(settings_manager)
        control_menu = ControlSettingsMenu(settings_manager)
        
        print("✓ Settings menu created successfully")
        print("✓ Control settings menu created successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Menu import test failed: {e}")
        return False

def test_game_state_integration():
    """Test that game states work with new settings"""
    print("\nTesting Game State Integration...")
    
    try:
        from game.game_states import GameStateManager, GameState
        
        # Create game state manager
        game_manager = GameStateManager()
        print("✓ Game state manager with settings created successfully")
        
        # Check that settings manager is available
        assert hasattr(game_manager, 'settings_manager')
        print("✓ Settings manager integrated into game states")
        
        # Check new game states exist
        assert GameState.SETTINGS in GameState
        assert GameState.CONTROL_SETTINGS in GameState
        print("✓ New game states defined correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Game state integration test failed: {e}")
        return False

def main():
    """Run all settings tests"""
    print("AWSKANOID Control Settings Test")
    print("=" * 35)
    
    tests_passed = 0
    total_tests = 3
    
    if test_settings_manager():
        tests_passed += 1
    
    if test_menu_imports():
        tests_passed += 1
    
    if test_game_state_integration():
        tests_passed += 1
    
    print(f"\nTest Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✓ All control settings tests passed!")
        print("\n🎮 New Features Available:")
        print("• Settings menu accessible from main menu")
        print("• Control mode selection (Keyboard/Mouse)")
        print("• Settings persist between game sessions")
        print("• Exclusive control modes (no mixed input)")
        print("\nTo test the new features, run: python3 main.py")
    else:
        print("✗ Some tests failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
