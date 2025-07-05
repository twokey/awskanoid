import pygame
import random
import math
from typing import List, Tuple
from utils.constants import *

class PowerUp:
    def __init__(self, x: float, y: float, powerup_type: str):
        self.x = x
        self.y = y
        self.type = powerup_type
        self.size = POWERUP_SIZE
        self.speed = POWERUP_FALL_SPEED
        self.collected = False
        self.rotation = 0
    
    def update(self, dt: float) -> bool:
        """Update power-up position, return False if should be removed"""
        self.y += self.speed * dt * 60
        self.rotation += dt * 180  # Rotate for visual effect
        
        # Remove if fallen off screen
        return self.y < SCREEN_HEIGHT + self.size
    
    def get_rect(self) -> pygame.Rect:
        """Get power-up's bounding rectangle"""
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, 
                          self.size, self.size)
    
    def draw(self, screen):
        """Draw the power-up with rotation and glow effect"""
        if self.collected:
            return
        
        center = (int(self.x), int(self.y))
        color = POWERUP_COLORS[self.type]
        
        # Draw glow effect
        glow_size = self.size + 4
        glow_color = tuple(min(255, c + 50) for c in color)
        pygame.draw.circle(screen, glow_color, center, glow_size // 2, 2)
        
        # Draw rotating diamond shape
        points = []
        for i in range(4):
            angle = math.radians(self.rotation + i * 90)
            px = center[0] + math.cos(angle) * (self.size // 2)
            py = center[1] + math.sin(angle) * (self.size // 2)
            points.append((px, py))
        
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, WHITE, points, 2)
        
        # Draw power-up symbol
        self.draw_symbol(screen, center, color)
    
    def draw_symbol(self, screen, center: Tuple[int, int], color: Tuple[int, int, int]):
        """Draw symbol indicating power-up type"""
        symbol_size = self.size // 3
        x, y = center
        
        if self.type == 'multi_ball':
            # Three small circles
            pygame.draw.circle(screen, WHITE, (x - 4, y), 2)
            pygame.draw.circle(screen, WHITE, (x + 4, y), 2)
            pygame.draw.circle(screen, WHITE, (x, y - 4), 2)
        
        elif self.type == 'laser':
            # Laser beam lines
            pygame.draw.line(screen, WHITE, (x, y - 6), (x, y + 6), 2)
            pygame.draw.line(screen, WHITE, (x - 3, y - 3), (x + 3, y + 3), 1)
            pygame.draw.line(screen, WHITE, (x + 3, y - 3), (x - 3, y + 3), 1)
        
        elif self.type == 'sticky':
            # Sticky drops
            for i in range(3):
                drop_x = x - 4 + i * 4
                pygame.draw.circle(screen, WHITE, (drop_x, y), 1)
        
        elif self.type == 'expand':
            # Expanding arrows
            pygame.draw.line(screen, WHITE, (x - 6, y), (x - 2, y), 2)
            pygame.draw.line(screen, WHITE, (x + 2, y), (x + 6, y), 2)
            pygame.draw.polygon(screen, WHITE, [(x - 2, y - 2), (x - 6, y), (x - 2, y + 2)])
            pygame.draw.polygon(screen, WHITE, [(x + 2, y - 2), (x + 6, y), (x + 2, y + 2)])
        
        elif self.type == 'shrink':
            # Contracting arrows
            pygame.draw.line(screen, WHITE, (x - 2, y), (x - 6, y), 2)
            pygame.draw.line(screen, WHITE, (x + 6, y), (x + 2, y), 2)
            pygame.draw.polygon(screen, WHITE, [(x - 6, y - 2), (x - 2, y), (x - 6, y + 2)])
            pygame.draw.polygon(screen, WHITE, [(x + 6, y - 2), (x + 2, y), (x + 6, y + 2)])
        
        elif self.type == 'slow':
            # Clock or slow symbol
            pygame.draw.circle(screen, WHITE, center, 4, 1)
            pygame.draw.line(screen, WHITE, center, (x, y - 3), 1)
            pygame.draw.line(screen, WHITE, center, (x + 2, y), 1)

class PowerUpManager:
    def __init__(self):
        self.active_powerups = []
        self.falling_powerups = []
        self.powerup_timers = {}
        self.multi_ball_requested = False
    
    def create_powerup(self, x: float, y: float) -> bool:
        """Create a random power-up at the given position"""
        if random.random() < POWERUP_DROP_CHANCE:
            powerup_types = ['multi_ball', 'laser', 'sticky', 'expand', 'shrink', 'slow']
            powerup_type = random.choice(powerup_types)
            self.falling_powerups.append(PowerUp(x, y, powerup_type))
            return True
        return False
    
    def update(self, dt: float, paddle):
        """Update all power-ups and check for collection"""
        # Update falling power-ups
        self.falling_powerups = [
            powerup for powerup in self.falling_powerups 
            if powerup.update(dt) and not self.check_collection(powerup, paddle)
        ]
        
        # Update active power-up timers
        expired_powerups = []
        for powerup_type, timer in self.powerup_timers.items():
            self.powerup_timers[powerup_type] = timer - dt * 1000
            if self.powerup_timers[powerup_type] <= 0:
                expired_powerups.append(powerup_type)
        
        # Remove expired power-ups
        for powerup_type in expired_powerups:
            self.deactivate_powerup(powerup_type, paddle)
    
    def check_collection(self, powerup: PowerUp, paddle) -> bool:
        """Check if power-up is collected by paddle"""
        paddle_rect = paddle.get_rect()
        powerup_rect = powerup.get_rect()
        
        if paddle_rect.colliderect(powerup_rect):
            self.activate_powerup(powerup.type, paddle)
            # Play collection sound (will be handled by game state)
            return True
        return False
    
    def activate_powerup(self, powerup_type: str, paddle):
        """Activate a power-up effect"""
        if powerup_type == 'multi_ball':
            # Multi-ball is handled immediately by the game state
            # Signal that multi-ball should be activated
            self.multi_ball_requested = True
        
        elif powerup_type == 'laser':
            paddle.can_shoot = True
            self.powerup_timers['laser'] = POWERUP_DURATION['laser']
        
        elif powerup_type == 'sticky':
            paddle.is_sticky = True
            self.powerup_timers['sticky'] = POWERUP_DURATION['sticky']
        
        elif powerup_type == 'expand':
            if 'shrink' in self.powerup_timers:
                del self.powerup_timers['shrink']
                paddle.reset_size()
            paddle.expand()
            self.powerup_timers['expand'] = POWERUP_DURATION['expand']
        
        elif powerup_type == 'shrink':
            if 'expand' in self.powerup_timers:
                del self.powerup_timers['expand']
                paddle.reset_size()
            paddle.shrink()
            self.powerup_timers['shrink'] = POWERUP_DURATION['shrink']
        
        elif powerup_type == 'slow':
            # Slow ball is handled by the game state
            self.powerup_timers['slow'] = POWERUP_DURATION['slow']
        
        # Add to active power-ups list
        if powerup_type not in [p['type'] for p in self.active_powerups]:
            self.active_powerups.append({
                'type': powerup_type,
                'timer': self.powerup_timers.get(powerup_type, 0)
            })
    
    def deactivate_powerup(self, powerup_type: str, paddle):
        """Deactivate a power-up effect"""
        if powerup_type == 'laser':
            paddle.can_shoot = False
        
        elif powerup_type == 'sticky':
            paddle.is_sticky = False
        
        elif powerup_type in ['expand', 'shrink']:
            paddle.reset_size()
        
        # Remove from timers and active list
        if powerup_type in self.powerup_timers:
            del self.powerup_timers[powerup_type]
        
        self.active_powerups = [
            p for p in self.active_powerups if p['type'] != powerup_type
        ]
    
    def is_active(self, powerup_type: str) -> bool:
        """Check if a power-up is currently active"""
        return powerup_type in self.powerup_timers
    
    def get_remaining_time(self, powerup_type: str) -> float:
        """Get remaining time for a power-up in seconds"""
        if powerup_type in self.powerup_timers:
            return max(0, self.powerup_timers[powerup_type] / 1000)
        return 0
    
    def clear_all(self, paddle):
        """Clear all active power-ups"""
        for powerup_type in list(self.powerup_timers.keys()):
            self.deactivate_powerup(powerup_type, paddle)
        self.falling_powerups.clear()
        self.active_powerups.clear()
    
    def check_multiball_request(self) -> bool:
        """Check if multi-ball was requested and reset the flag"""
        if self.multi_ball_requested:
            self.multi_ball_requested = False
            return True
        return False
    
    def draw(self, screen):
        """Draw all falling power-ups"""
        for powerup in self.falling_powerups:
            powerup.draw(screen)
