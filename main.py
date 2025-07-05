#!/usr/bin/env python3
"""
AWSKANOID - A Modern Arkanoid/Breakout Clone
Built with Pygame for macOS

A single-player brick-breaking arcade game with 10 pre-designed levels,
modern vector-style graphics, and various power-ups.

Controls:
- Arrow Keys / Mouse: Move paddle
- Spacebar: Release ball / Shoot laser
- ESC: Pause game

Author: Amazon Q
Version: 1.0
"""

import pygame
import sys
import os
from typing import Tuple

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.constants import *
from game.game_states import GameStateManager

class AwskanoidGame:
    def __init__(self):
        """Initialize the game"""
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()
        
        # Set up display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AWSKANOID - A Modern Breakout Experience")
        
        # Set up game icon (create a simple icon using pygame)
        self.create_game_icon()
        
        # Initialize clock for frame rate control
        self.clock = pygame.time.Clock()
        
        # Initialize game state manager
        self.game_state_manager = GameStateManager()
        
        # Game loop control
        self.running = True
        self.show_fps = False  # Set to True for debugging
        
        print("AWSKANOID initialized successfully!")
        print(f"Screen resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print(f"Target FPS: {FPS}")
    
    def create_game_icon(self):
        """Create a simple game icon"""
        icon_size = 32
        icon_surface = pygame.Surface((icon_size, icon_size))
        icon_surface.fill(BACKGROUND)
        
        # Draw a simple paddle and ball icon
        paddle_rect = pygame.Rect(4, 24, 24, 4)
        pygame.draw.rect(icon_surface, PADDLE_COLOR, paddle_rect)
        
        ball_center = (16, 12)
        pygame.draw.circle(icon_surface, BALL_COLOR, ball_center, 4)
        
        # Draw some bricks
        for i in range(3):
            brick_rect = pygame.Rect(2 + i * 9, 2, 8, 4)
            colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
            pygame.draw.rect(icon_surface, colors[i], brick_rect)
        
        pygame.display.set_icon(icon_surface)
    
    def handle_events(self) -> bool:
        """Handle pygame events"""
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        # Check for quit events
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.show_fps = not self.show_fps
        
        # Handle game state events
        result = self.game_state_manager.handle_events(events, keys, mouse_pos, mouse_clicked)
        if result == "quit":
            return False
        
        return True
    
    def update(self, dt: float):
        """Update game logic"""
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        self.game_state_manager.update(dt, keys, mouse_pos)
    
    def draw(self):
        """Draw everything to the screen"""
        # Clear screen
        self.screen.fill(BACKGROUND)
        
        # Draw current game state
        self.game_state_manager.draw(self.screen)
        
        # Draw FPS counter if enabled
        if self.show_fps:
            fps = self.clock.get_fps()
            self.game_state_manager.hud.draw_fps(self.screen, fps)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("Starting AWSKANOID...")
        print("Press F1 to toggle FPS counter")
        print("Have fun!")
        
        while self.running:
            # Calculate delta time
            dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds
            
            # Handle events
            if not self.handle_events():
                self.running = False
                break
            
            # Update game logic
            self.update(dt)
            
            # Draw everything
            self.draw()
        
        self.quit()
    
    def quit(self):
        """Clean up and quit the game"""
        print("Thanks for playing AWSKANOID!")
        pygame.quit()
        sys.exit()

def main():
    """Main entry point"""
    try:
        # Check if numpy is available for sound generation
        try:
            import numpy as np
            print("NumPy found - Sound effects enabled")
        except ImportError:
            print("Warning: NumPy not found - Sound effects may not work properly")
            print("Install NumPy with: pip install numpy")
        
        # Create and run the game
        game = AwskanoidGame()
        game.run()
        
    except Exception as e:
        print(f"Error starting game: {e}")
        print("Make sure Pygame is installed: pip install pygame")
        sys.exit(1)

if __name__ == "__main__":
    main()
