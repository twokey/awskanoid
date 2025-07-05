#!/usr/bin/env python3
"""
Test script to verify AWSKANOID components work correctly
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        import pygame
        print("✓ Pygame imported successfully")
    except ImportError as e:
        print(f"✗ Pygame import failed: {e}")
        return False
    
    try:
        import numpy
        print("✓ NumPy imported successfully")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        import utils.constants
        print("✓ Constants imported successfully")
    except ImportError as e:
        print(f"✗ Constants import failed: {e}")
        return False
    
    try:
        from game.entities import Ball, Paddle, Brick
        print("✓ Game entities imported successfully")
    except ImportError as e:
        print(f"✗ Game entities import failed: {e}")
        return False
    
    try:
        from game.game_states import GameStateManager
        print("✓ Game state manager imported successfully")
    except ImportError as e:
        print(f"✗ Game state manager import failed: {e}")
        return False
    
    try:
        from utils.sounds import SoundManager
        print("✓ Sound manager imported successfully")
    except ImportError as e:
        print(f"✗ Sound manager import failed: {e}")
        return False
    
    return True

def test_game_initialization():
    """Test basic game component initialization"""
    print("\nTesting game initialization...")
    
    try:
        import pygame
        pygame.init()
        
        # Test screen creation
        screen = pygame.display.set_mode((100, 100))
        print("✓ Pygame screen created successfully")
        
        # Test game entities
        from game.entities import Ball, Paddle, Brick
        
        ball = Ball(50, 50)
        print("✓ Ball created successfully")
        
        paddle = Paddle(50, 80)
        print("✓ Paddle created successfully")
        
        brick = Brick(10, 10, 'normal')
        print("✓ Brick created successfully")
        
        # Test sound manager
        from utils.sounds import SoundManager
        sound_manager = SoundManager()
        print("✓ Sound manager created successfully")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"✗ Game initialization failed: {e}")
        return False

def test_level_loading():
    """Test level loading"""
    print("\nTesting level loading...")
    
    try:
        from game.levels import LevelManager
        
        level_manager = LevelManager()
        print("✓ Level manager created successfully")
        
        # Test level 1
        bricks = level_manager.create_bricks_for_level(1)
        print(f"✓ Level 1 loaded with {len(bricks)} bricks")
        
        # Test all levels
        for i in range(1, 11):
            level_data = level_manager.get_level(i)
            level_name = level_manager.get_level_name(i)
            print(f"✓ Level {i}: {level_name}")
        
        return True
        
    except Exception as e:
        print(f"✗ Level loading failed: {e}")
        return False

def main():
    """Run all tests"""
    print("AWSKANOID Component Test")
    print("=" * 30)
    
    tests_passed = 0
    total_tests = 3
    
    if test_imports():
        tests_passed += 1
    
    if test_game_initialization():
        tests_passed += 1
    
    if test_level_loading():
        tests_passed += 1
    
    print(f"\nTest Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✓ All tests passed! The game should work correctly.")
        print("\nTo start the game, run: python3 main.py")
    else:
        print("✗ Some tests failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
