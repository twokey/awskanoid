#!/usr/bin/env python3
"""
Test script to verify keyboard navigation in menus
"""

import sys
import os
import pygame

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_menu_keyboard_navigation():
    """Test keyboard navigation functionality"""
    print("Testing Menu Keyboard Navigation...")
    
    try:
        from ui.menu import MainMenu, SettingsMenu, ControlSettingsMenu
        from utils.settings import SettingsManager
        
        # Initialize pygame for event testing
        pygame.init()
        
        # Test MainMenu keyboard navigation
        main_menu = MainMenu()
        print("✓ MainMenu created with keyboard navigation")
        
        # Check initial selection
        assert main_menu.selected_index == 0
        assert main_menu.buttons[0].selected == True
        print("✓ Initial selection set correctly")
        
        # Test selection update
        main_menu.selected_index = 2
        main_menu.update_selection()
        assert main_menu.buttons[2].selected == True
        assert main_menu.buttons[0].selected == False
        print("✓ Selection update works correctly")
        
        # Test SettingsMenu
        settings_manager = SettingsManager()
        settings_menu = SettingsMenu(settings_manager)
        print("✓ SettingsMenu created with keyboard navigation")
        
        # Test ControlSettingsMenu
        control_menu = ControlSettingsMenu(settings_manager)
        print("✓ ControlSettingsMenu created with keyboard navigation")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"✗ Menu keyboard navigation test failed: {e}")
        return False

def test_button_selection_states():
    """Test button selection state functionality"""
    print("\nTesting Button Selection States...")
    
    try:
        from ui.menu import Button
        import pygame
        
        pygame.init()
        font = pygame.font.Font(None, 32)
        
        # Create test button
        button = Button(100, 100, 200, 50, "Test Button", font)
        
        # Test initial state
        assert button.selected == False
        print("✓ Button initial selection state correct")
        
        # Test setting selection
        button.set_selected(True)
        assert button.selected == True
        print("✓ Button selection setting works")
        
        button.set_selected(False)
        assert button.selected == False
        print("✓ Button deselection works")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"✗ Button selection test failed: {e}")
        return False

def test_keyboard_event_simulation():
    """Test keyboard event handling simulation"""
    print("\nTesting Keyboard Event Handling...")
    
    try:
        from ui.menu import MainMenu
        import pygame
        
        pygame.init()
        
        # Create main menu
        main_menu = MainMenu()
        initial_selection = main_menu.selected_index
        
        # Simulate DOWN key event
        down_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        events = [down_event]
        
        # Handle keyboard input
        result = main_menu.handle_keyboard_input(events)
        
        # Check that selection moved down
        expected_selection = (initial_selection + 1) % len(main_menu.buttons)
        assert main_menu.selected_index == expected_selection
        print("✓ DOWN key navigation works")
        
        # Simulate UP key event
        up_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
        events = [up_event]
        
        current_selection = main_menu.selected_index
        main_menu.handle_keyboard_input(events)
        
        expected_selection = (current_selection - 1) % len(main_menu.buttons)
        assert main_menu.selected_index == expected_selection
        print("✓ UP key navigation works")
        
        # Simulate ENTER key event
        enter_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        events = [enter_event]
        
        result = main_menu.handle_keyboard_input(events)
        assert result is not None  # Should return an action
        print("✓ ENTER key activation works")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"✗ Keyboard event handling test failed: {e}")
        return False

def main():
    """Run all keyboard navigation tests"""
    print("AWSKANOID Keyboard Navigation Test")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 3
    
    if test_menu_keyboard_navigation():
        tests_passed += 1
    
    if test_button_selection_states():
        tests_passed += 1
    
    if test_keyboard_event_simulation():
        tests_passed += 1
    
    print(f"\nTest Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✓ All keyboard navigation tests passed!")
        print("\n⌨️  New Keyboard Features:")
        print("• UP/DOWN arrows navigate menu buttons")
        print("• ENTER activates selected button")
        print("• ESC goes back in menus")
        print("• Mouse and keyboard work together")
        print("• Visual feedback with yellow selection border")
        print("• Navigation hints displayed in menus")
        print("\nTo test keyboard navigation, run: python3 main.py")
        print("Then use arrow keys and ENTER to navigate!")
    else:
        print("✗ Some tests failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
