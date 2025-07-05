import pygame
import math
from typing import Tuple, Optional, List
from utils.constants import *

class CollisionDetector:
    @staticmethod
    def ball_paddle_collision(ball, paddle) -> Optional[float]:
        """
        Check collision between ball and paddle.
        Returns hit position (-1 to 1) if collision occurs, None otherwise.
        """
        ball_rect = ball.get_rect()
        paddle_rect = paddle.get_rect()
        
        if ball_rect.colliderect(paddle_rect):
            # Calculate hit position relative to paddle center
            paddle_center = paddle.x + paddle.width // 2
            hit_position = (ball.x - paddle_center) / (paddle.width // 2)
            return max(-1, min(1, hit_position))
        
        return None
    
    @staticmethod
    def ball_brick_collision(ball, brick) -> Optional[str]:
        """
        Check collision between ball and brick.
        Returns collision side ('top', 'bottom', 'left', 'right') if collision occurs.
        """
        if brick.destroyed:
            return None
        
        ball_rect = ball.get_rect()
        brick_rect = brick.get_rect()
        
        if not ball_rect.colliderect(brick_rect):
            return None
        
        # Determine collision side based on ball position and movement
        ball_center_x = ball.x
        ball_center_y = ball.y
        brick_center_x = brick.x + brick.width // 2
        brick_center_y = brick.y + brick.height // 2
        
        # Calculate overlap on each axis
        overlap_x = min(ball_rect.right, brick_rect.right) - max(ball_rect.left, brick_rect.left)
        overlap_y = min(ball_rect.bottom, brick_rect.bottom) - max(ball_rect.top, brick_rect.top)
        
        # Determine collision side based on smallest overlap
        if overlap_x < overlap_y:
            # Horizontal collision
            if ball_center_x < brick_center_x:
                return 'left'
            else:
                return 'right'
        else:
            # Vertical collision
            if ball_center_y < brick_center_y:
                return 'top'
            else:
                return 'bottom'
    
    @staticmethod
    def ball_wall_collision(ball) -> List[str]:
        """
        Check collision between ball and game area walls.
        Returns list of walls hit ('left', 'right', 'top').
        """
        collisions = []
        
        # Left wall
        if ball.x - ball.radius <= GAME_AREA_LEFT:
            collisions.append('left')
        
        # Right wall
        if ball.x + ball.radius >= GAME_AREA_RIGHT:
            collisions.append('right')
        
        # Top wall
        if ball.y - ball.radius <= GAME_AREA_TOP:
            collisions.append('top')
        
        return collisions
    
    @staticmethod
    def laser_brick_collision(laser, brick) -> bool:
        """Check collision between laser and brick"""
        if brick.destroyed:
            return False
        
        laser_rect = laser.get_rect()
        brick_rect = brick.get_rect()
        
        return laser_rect.colliderect(brick_rect)
    
    @staticmethod
    def resolve_ball_brick_collision(ball, brick, collision_side: str):
        """Resolve ball-brick collision by adjusting ball position and velocity"""
        brick_rect = brick.get_rect()
        
        if collision_side in ['left', 'right']:
            # Horizontal collision
            if collision_side == 'left':
                ball.x = brick_rect.left - ball.radius
            else:  # right
                ball.x = brick_rect.right + ball.radius
            ball.bounce_horizontal()
        
        else:  # top or bottom
            # Vertical collision
            if collision_side == 'top':
                ball.y = brick_rect.top - ball.radius
            else:  # bottom
                ball.y = brick_rect.bottom + ball.radius
            ball.bounce_vertical()
    
    @staticmethod
    def resolve_ball_wall_collision(ball, walls: List[str]):
        """Resolve ball-wall collisions"""
        for wall in walls:
            if wall == 'left':
                ball.x = GAME_AREA_LEFT + ball.radius
                ball.bounce_horizontal()
            elif wall == 'right':
                ball.x = GAME_AREA_RIGHT - ball.radius
                ball.bounce_horizontal()
            elif wall == 'top':
                ball.y = GAME_AREA_TOP + ball.radius
                ball.bounce_vertical()
    
    @staticmethod
    def is_ball_below_paddle(ball, paddle) -> bool:
        """Check if ball has fallen below the paddle (life lost)"""
        return ball.y - ball.radius > paddle.y + paddle.height + 10
    
    @staticmethod
    def circle_rect_collision(circle_x: float, circle_y: float, radius: float, 
                            rect: pygame.Rect) -> bool:
        """
        Check collision between a circle and rectangle.
        More accurate than simple rect collision for circular objects.
        """
        # Find the closest point on the rectangle to the circle center
        closest_x = max(rect.left, min(circle_x, rect.right))
        closest_y = max(rect.top, min(circle_y, rect.bottom))
        
        # Calculate distance between circle center and closest point
        distance_x = circle_x - closest_x
        distance_y = circle_y - closest_y
        distance_squared = distance_x * distance_x + distance_y * distance_y
        
        return distance_squared <= radius * radius
    
    @staticmethod
    def get_collision_normal(ball, brick, collision_side: str) -> Tuple[float, float]:
        """Get the normal vector for a collision"""
        if collision_side == 'left':
            return (-1, 0)
        elif collision_side == 'right':
            return (1, 0)
        elif collision_side == 'top':
            return (0, -1)
        elif collision_side == 'bottom':
            return (0, 1)
        else:
            return (0, 0)
    
    @staticmethod
    def reflect_velocity(velocity: Tuple[float, float], normal: Tuple[float, float]) -> Tuple[float, float]:
        """Reflect velocity vector off a surface normal"""
        vx, vy = velocity
        nx, ny = normal
        
        # Reflection formula: v' = v - 2(v·n)n
        dot_product = vx * nx + vy * ny
        reflected_vx = vx - 2 * dot_product * nx
        reflected_vy = vy - 2 * dot_product * ny
        
        return (reflected_vx, reflected_vy)
