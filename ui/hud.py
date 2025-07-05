import pygame
from typing import List, Dict
from utils.constants import *

class HUD:
    def __init__(self):
        pygame.font.init()
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
    
    def draw_score(self, screen, score: int):
        """Draw the current score in the top left"""
        score_text = self.font_medium.render(f"Score: {score:,}", True, WHITE)
        screen.blit(score_text, (20, 20))
    
    def draw_lives(self, screen, lives: int):
        """Draw remaining lives as paddle icons in the top right"""
        lives_text = self.font_medium.render("Lives:", True, WHITE)
        text_rect = lives_text.get_rect()
        screen.blit(lives_text, (SCREEN_WIDTH - 150, 20))
        
        # Draw paddle icons for each life
        paddle_width = 30
        paddle_height = 6
        start_x = SCREEN_WIDTH - 150 + text_rect.width + 10
        
        for i in range(lives):
            x = start_x + i * (paddle_width + 5)
            y = 25
            
            # Draw mini paddle
            pygame.draw.rect(screen, PADDLE_COLOR, 
                           (x, y, paddle_width, paddle_height))
            pygame.draw.rect(screen, WHITE, 
                           (x, y, paddle_width, paddle_height), 1)
    
    def draw_level(self, screen, level: int, level_name: str = ""):
        """Draw the current level in the top center"""
        level_text = f"Level {level}"
        if level_name:
            level_text += f": {level_name}"
        
        text_surface = self.font_medium.render(level_text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = SCREEN_WIDTH // 2
        text_rect.y = 20
        screen.blit(text_surface, text_rect)
    
    def draw_powerup_timers(self, screen, powerup_manager):
        """Draw active power-up timers"""
        y_offset = 80
        
        for i, powerup in enumerate(powerup_manager.active_powerups):
            powerup_type = powerup['type']
            remaining_time = powerup_manager.get_remaining_time(powerup_type)
            
            if remaining_time > 0:
                # Format power-up name
                display_name = powerup_type.replace('_', ' ').title()
                time_text = f"{display_name}: {remaining_time:.1f}s"
                
                # Choose color based on power-up type
                color = POWERUP_COLORS.get(powerup_type, WHITE)
                
                text_surface = self.font_small.render(time_text, True, color)
                screen.blit(text_surface, (20, y_offset + i * 25))
    
    def draw_game_over(self, screen, final_score: int, is_high_score: bool = False):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font_medium.render(f"Final Score: {final_score:,}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        screen.blit(score_text, score_rect)
        
        # High score notification
        if is_high_score:
            high_score_text = self.font_medium.render("NEW HIGH SCORE!", True, (255, 215, 0))
            high_score_rect = high_score_text.get_rect()
            high_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(high_score_text, high_score_rect)
        
        # Instructions
        restart_text = self.font_small.render("Press R to restart or ESC for main menu", True, WHITE)
        restart_rect = restart_text.get_rect()
        restart_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        screen.blit(restart_text, restart_rect)
    
    def draw_level_complete(self, screen, level: int, score: int):
        """Draw level complete screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Level Complete text
        complete_text = self.font_large.render(f"LEVEL {level} COMPLETE!", True, (0, 255, 0))
        complete_rect = complete_text.get_rect()
        complete_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        screen.blit(complete_text, complete_rect)
        
        # Score
        score_text = self.font_medium.render(f"Score: {score:,}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(score_text, score_rect)
        
        # Instructions
        continue_text = self.font_small.render("Press SPACE to continue", True, WHITE)
        continue_rect = continue_text.get_rect()
        continue_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        screen.blit(continue_text, continue_rect)
    
    def draw_pause_overlay(self, screen):
        """Draw pause screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Paused text
        paused_text = self.font_large.render("PAUSED", True, WHITE)
        paused_rect = paused_text.get_rect()
        paused_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        screen.blit(paused_text, paused_rect)
        
        # Instructions
        instructions = [
            "ESC - Resume Game",
            "R - Restart Level", 
            "M - Main Menu"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font_small.render(instruction, True, WHITE)
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 30)
            screen.blit(text, text_rect)
    
    def draw_controls_help(self, screen):
        """Draw controls help overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Title
        title_text = self.font_large.render("CONTROLS", True, WHITE)
        title_rect = title_text.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2, 100)
        screen.blit(title_text, title_rect)
        
        # Controls list
        controls = [
            "Arrow Keys / Mouse - Move Paddle",
            "Spacebar - Release Ball / Shoot Laser",
            "ESC - Pause Game",
            "",
            "POWER-UPS:",
            "Multi-Ball - Split ball into 3",
            "Laser - Shoot lasers for 15 seconds",
            "Sticky - Ball sticks to paddle",
            "Expand - Increase paddle size",
            "Shrink - Decrease paddle size (bad!)",
            "Slow - Reduce ball speed",
            "",
            "Press any key to continue..."
        ]
        
        start_y = 200
        for i, control in enumerate(controls):
            if control == "":
                continue
            
            color = WHITE
            if control.startswith("POWER-UPS:"):
                color = (255, 215, 0)
            elif "bad!" in control:
                color = (255, 100, 100)
            
            text = self.font_small.render(control, True, color)
            text_rect = text.get_rect()
            text_rect.centerx = SCREEN_WIDTH // 2
            text_rect.y = start_y + i * 25
            screen.blit(text, text_rect)
    
    def draw_fps(self, screen, fps: float):
        """Draw FPS counter (for debugging)"""
        fps_text = self.font_small.render(f"FPS: {fps:.1f}", True, WHITE)
        screen.blit(fps_text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30))
