import pygame
import math
import random
from typing import Tuple, List
from utils.constants import *

class Ball:
    def __init__(self, x: float, y: float, speed: float = BALL_SPEED):
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS
        self.speed = speed
        self.dx = random.choice([-1, 1]) * 0.7  # Initial horizontal direction
        self.dy = -1  # Always start going up
        self.normalize_velocity()
        self.stuck_to_paddle = False
        self.paddle_offset = 0
    
    def normalize_velocity(self):
        """Normalize velocity to maintain consistent speed"""
        magnitude = math.sqrt(self.dx**2 + self.dy**2)
        if magnitude > 0:
            self.dx = (self.dx / magnitude) * self.speed
            self.dy = (self.dy / magnitude) * self.speed
    
    def update(self, dt: float, paddle=None):
        """Update ball position"""
        if self.stuck_to_paddle and paddle:
            self.x = paddle.x + paddle.width // 2 + self.paddle_offset
            self.y = paddle.y - self.radius
        else:
            self.x += self.dx * dt * 60  # Frame-independent movement
            self.y += self.dy * dt * 60
    
    def bounce_horizontal(self):
        """Bounce off horizontal surfaces"""
        self.dx = -self.dx
    
    def bounce_vertical(self):
        """Bounce off vertical surfaces"""
        self.dy = -self.dy
    
    def bounce_paddle(self, paddle, hit_position: float):
        """Bounce off paddle with angle based on hit position"""
        # hit_position ranges from -1 (left edge) to 1 (right edge)
        max_angle = math.pi / 3  # 60 degrees maximum
        angle = hit_position * max_angle
        
        # Calculate new velocity
        speed = self.speed
        self.dx = math.sin(angle) * speed
        self.dy = -abs(math.cos(angle)) * speed  # Always go up
        
        # Ensure minimum upward velocity
        if abs(self.dy) < speed * 0.3:
            self.dy = -speed * 0.3 if self.dy < 0 else speed * 0.3
    
    def stick_to_paddle(self, paddle):
        """Stick ball to paddle"""
        self.stuck_to_paddle = True
        self.paddle_offset = self.x - (paddle.x + paddle.width // 2)
        self.dx = 0
        self.dy = 0
    
    def release_from_paddle(self):
        """Release ball from paddle"""
        if self.stuck_to_paddle:
            self.stuck_to_paddle = False
            self.dx = random.uniform(-0.5, 0.5) * self.speed
            self.dy = -self.speed
            self.normalize_velocity()
    
    def get_rect(self) -> pygame.Rect:
        """Get ball's bounding rectangle"""
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
    
    def draw(self, screen):
        """Draw the ball with gradient effect"""
        # Main ball
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), self.radius)
        
        # Highlight for 3D effect
        highlight_offset = self.radius // 3
        pygame.draw.circle(screen, (255, 255, 255), 
                          (int(self.x - highlight_offset), int(self.y - highlight_offset)), 
                          self.radius // 3)

class Paddle:
    def __init__(self, x: float, y: float):
        self.base_width = PADDLE_WIDTH
        self.width = self.base_width
        self.height = PADDLE_HEIGHT
        self.x = x - self.width // 2
        self.y = y
        self.speed = PADDLE_SPEED
        self.can_shoot = False
        self.is_sticky = False
        self.lasers = []
    
    def update(self, dt: float, keys, mouse_pos=None, control_mode="keyboard"):
        """Update paddle position based on input and control mode"""
        old_x = self.x
        
        if control_mode == "keyboard":
            # Keyboard controls only
            if keys[pygame.K_LEFT]:
                self.x -= self.speed * dt * 60
            if keys[pygame.K_RIGHT]:
                self.x += self.speed * dt * 60
        
        elif control_mode == "mouse" and mouse_pos:
            # Mouse controls only
            target_x = mouse_pos[0] - self.width // 2
            # Smooth mouse movement
            diff = target_x - self.x
            if abs(diff) > 2:  # Dead zone to prevent jitter
                self.x += diff * 0.1
        
        # Keep paddle within bounds
        self.x = max(GAME_AREA_LEFT, min(self.x, GAME_AREA_RIGHT - self.width))
        
        # Update lasers
        self.lasers = [laser for laser in self.lasers if laser.update(dt)]
    
    def shoot_laser(self):
        """Shoot a laser if laser power-up is active"""
        if self.can_shoot:
            laser_x = self.x + self.width // 2
            laser_y = self.y
            self.lasers.append(Laser(laser_x, laser_y))
    
    def expand(self):
        """Expand paddle width"""
        old_center = self.x + self.width // 2
        self.width = int(self.base_width * 1.5)
        self.x = old_center - self.width // 2
    
    def shrink(self):
        """Shrink paddle width"""
        old_center = self.x + self.width // 2
        self.width = int(self.base_width * 0.5)
        self.x = old_center - self.width // 2
    
    def reset_size(self):
        """Reset paddle to normal size"""
        old_center = self.x + self.width // 2
        self.width = self.base_width
        self.x = old_center - self.width // 2
    
    def get_rect(self) -> pygame.Rect:
        """Get paddle's bounding rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_hit_position(self, ball_x: float) -> float:
        """Get normalized hit position (-1 to 1) based on ball contact"""
        paddle_center = self.x + self.width // 2
        relative_pos = ball_x - paddle_center
        return max(-1, min(1, relative_pos / (self.width // 2)))
    
    def draw(self, screen):
        """Draw the paddle with gradient effect"""
        rect = self.get_rect()
        
        # Draw main paddle with gradient
        for i in range(self.height):
            color_ratio = i / self.height
            color = [
                int(PADDLE_COLOR[j] + (PADDLE_HIGHLIGHT[j] - PADDLE_COLOR[j]) * (1 - color_ratio))
                for j in range(3)
            ]
            pygame.draw.rect(screen, color, 
                           (rect.x, rect.y + i, rect.width, 1))
        
        # Draw border
        pygame.draw.rect(screen, WHITE, rect, 2)
        
        # Draw lasers
        for laser in self.lasers:
            laser.draw(screen)

class Laser:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.width = 3
        self.height = 10
        self.speed = 12
    
    def update(self, dt: float) -> bool:
        """Update laser position, return False if should be removed"""
        self.y -= self.speed * dt * 60
        return self.y > -self.height
    
    def get_rect(self) -> pygame.Rect:
        """Get laser's bounding rectangle"""
        return pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)
    
    def draw(self, screen):
        """Draw the laser"""
        rect = self.get_rect()
        pygame.draw.rect(screen, (255, 255, 0), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 1)

class Brick:
    def __init__(self, x: float, y: float, brick_type: str = 'normal'):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.type = brick_type
        self.max_hits = self.get_max_hits()
        self.hits = 0
        self.destroyed = False
        self.flash_timer = 0
        self.points = self.get_points()
    
    def get_max_hits(self) -> int:
        """Get maximum hits for brick type"""
        hit_map = {
            'normal': 1,
            'medium': 2,
            'hard': 3,
            'unbreakable': float('inf')
        }
        return hit_map.get(self.type, 1)
    
    def get_points(self) -> int:
        """Get points for destroying this brick"""
        point_map = {
            'normal': SCORE_NORMAL,
            'medium': SCORE_MEDIUM,
            'hard': SCORE_HARD,
            'unbreakable': 0
        }
        return point_map.get(self.type, SCORE_NORMAL)
    
    def hit(self) -> bool:
        """Hit the brick, return True if destroyed"""
        if self.type == 'unbreakable':
            self.flash_timer = 200  # Flash for visual feedback
            return False
        
        self.hits += 1
        self.flash_timer = 200
        
        if self.hits >= self.max_hits:
            self.destroyed = True
            return True
        
        return False
    
    def update(self, dt: float):
        """Update brick state"""
        if self.flash_timer > 0:
            self.flash_timer -= dt * 1000
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get current brick color based on type and damage"""
        base_colors = BRICK_COLORS[self.type]
        
        if self.type == 'medium':
            if self.hits >= 1:
                # Darker when damaged
                return tuple(max(0, c - 50) for c in base_colors[0])
        elif self.type == 'hard':
            if self.hits >= 2:
                # Much darker when heavily damaged
                return tuple(max(0, c - 100) for c in base_colors[0])
            elif self.hits >= 1:
                # Slightly darker when damaged
                return tuple(max(0, c - 50) for c in base_colors[0])
        
        return base_colors[0]
    
    def get_rect(self) -> pygame.Rect:
        """Get brick's bounding rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        """Draw the brick with gradient and damage effects"""
        if self.destroyed:
            return
        
        rect = self.get_rect()
        base_color = self.get_color()
        highlight_color = BRICK_COLORS[self.type][1]
        
        # Flash effect when hit
        if self.flash_timer > 0:
            flash_intensity = self.flash_timer / 200
            base_color = tuple(min(255, int(c + (255 - c) * flash_intensity)) for c in base_color)
            highlight_color = tuple(min(255, int(c + (255 - c) * flash_intensity)) for c in highlight_color)
        
        # Draw gradient
        for i in range(self.height):
            color_ratio = i / self.height
            color = [
                int(highlight_color[j] + (base_color[j] - highlight_color[j]) * color_ratio)
                for j in range(3)
            ]
            pygame.draw.rect(screen, color, 
                           (rect.x, rect.y + i, rect.width, 1))
        
        # Draw border
        border_color = WHITE if self.type != 'unbreakable' else DARK_GRAY
        pygame.draw.rect(screen, border_color, rect, 1)
