import pygame
import random
from typing import List, Optional
from enum import Enum

from utils.constants import *
from utils.sounds import SoundManager
from utils.score import ScoreManager, GameScore
from game.entities import Ball, Paddle, Brick
from game.powerups import PowerUpManager
from game.collision import CollisionDetector
from game.levels import LevelManager
from ui.hud import HUD
from ui.menu import MainMenu, HighScoreMenu, NameEntryMenu

class GameState(Enum):
    MAIN_MENU = "main_menu"
    PLAYING = "playing"
    PAUSED = "paused"
    LEVEL_COMPLETE = "level_complete"
    GAME_OVER = "game_over"
    HIGH_SCORES = "high_scores"
    CONTROLS = "controls"
    NAME_ENTRY = "name_entry"

class GameStateManager:
    def __init__(self):
        # Initialize managers
        self.sound_manager = SoundManager()
        self.score_manager = ScoreManager()
        self.level_manager = LevelManager()
        self.powerup_manager = PowerUpManager()
        self.collision_detector = CollisionDetector()
        self.hud = HUD()
        
        # Initialize UI
        self.main_menu = MainMenu()
        self.high_score_menu = HighScoreMenu(self.score_manager)
        self.name_entry_menu = None
        
        # Game state
        self.current_state = GameState.MAIN_MENU
        self.game_score = GameScore()
        
        # Game objects
        self.paddle = None
        self.balls = []
        self.bricks = []
        
        # Timing
        self.level_complete_timer = 0
        self.show_controls = False
        
        # Initialize game
        self.reset_game()
    
    def reset_game(self):
        """Reset game to initial state"""
        self.game_score.reset()
        self.powerup_manager.clear_all(self.paddle if self.paddle else None)
        self.setup_level(1)
    
    def setup_level(self, level_num: int):
        """Setup a specific level"""
        self.game_score.level = level_num
        
        # Create paddle
        paddle_x = SCREEN_WIDTH // 2
        paddle_y = SCREEN_HEIGHT - PADDLE_Y_OFFSET
        self.paddle = Paddle(paddle_x, paddle_y)
        
        # Create ball
        ball_speed = BALL_SPEED + (level_num - 1) * BALL_SPEED_INCREMENT
        ball_speed *= self.level_manager.get_ball_speed_multiplier(level_num)
        
        ball_x = paddle_x
        ball_y = paddle_y - BALL_RADIUS - 10
        ball = Ball(ball_x, ball_y, ball_speed)
        ball.stick_to_paddle(self.paddle)
        self.balls = [ball]
        
        # Create bricks
        self.bricks = self.level_manager.create_bricks_for_level(level_num)
        
        # Clear power-ups
        self.powerup_manager.clear_all(self.paddle)
    
    def handle_events(self, events: List[pygame.event.Event], keys, mouse_pos, mouse_clicked):
        """Handle events based on current state"""
        if self.current_state == GameState.MAIN_MENU:
            action = self.main_menu.update(mouse_pos, mouse_clicked)
            if action == "start_game":
                self.current_state = GameState.PLAYING
                self.reset_game()
            elif action == "high_scores":
                self.current_state = GameState.HIGH_SCORES
            elif action == "controls":
                self.show_controls = True
                self.current_state = GameState.CONTROLS
            elif action == "quit":
                return "quit"
        
        elif self.current_state == GameState.HIGH_SCORES:
            action = self.high_score_menu.update(mouse_pos, mouse_clicked)
            if action == "main_menu":
                self.current_state = GameState.MAIN_MENU
        
        elif self.current_state == GameState.CONTROLS:
            # Any key returns to main menu
            for event in events:
                if event.type == pygame.KEYDOWN:
                    self.show_controls = False
                    self.current_state = GameState.MAIN_MENU
        
        elif self.current_state == GameState.PLAYING:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.current_state = GameState.PAUSED
                    elif event.key == pygame.K_SPACE:
                        # Release stuck balls or shoot laser
                        for ball in self.balls:
                            if ball.stuck_to_paddle:
                                ball.release_from_paddle()
                        if self.paddle.can_shoot:
                            self.paddle.shoot_laser()
        
        elif self.current_state == GameState.PAUSED:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.current_state = GameState.PLAYING
                    elif event.key == pygame.K_r:
                        self.setup_level(self.game_score.level)
                        self.current_state = GameState.PLAYING
                    elif event.key == pygame.K_m:
                        self.current_state = GameState.MAIN_MENU
        
        elif self.current_state == GameState.LEVEL_COMPLETE:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_score.level >= TOTAL_LEVELS:
                            # Game completed!
                            self.check_high_score()
                        else:
                            self.game_score.next_level()
                            self.setup_level(self.game_score.level)
                            self.current_state = GameState.PLAYING
        
        elif self.current_state == GameState.GAME_OVER:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.current_state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.current_state = GameState.MAIN_MENU
        
        elif self.current_state == GameState.NAME_ENTRY:
            if self.name_entry_menu:
                result = self.name_entry_menu.update(1/60, events)  # Assuming 60 FPS
                if result:
                    # Save high score
                    self.score_manager.add_score(result, self.game_score.score, self.game_score.level)
                    self.current_state = GameState.HIGH_SCORES
        
        return None
    
    def update(self, dt: float, keys, mouse_pos):
        """Update game state"""
        if self.current_state == GameState.PLAYING:
            self.update_gameplay(dt, keys, mouse_pos)
        elif self.current_state == GameState.LEVEL_COMPLETE:
            self.level_complete_timer += dt * 1000
    
    def update_gameplay(self, dt: float, keys, mouse_pos):
        """Update gameplay logic"""
        # Update paddle
        self.paddle.update(dt, keys, mouse_pos)
        
        # Update power-ups
        old_falling_count = len(self.powerup_manager.falling_powerups)
        self.powerup_manager.update(dt, self.paddle)
        new_falling_count = len(self.powerup_manager.falling_powerups)
        
        # Play sound if power-up was collected
        if old_falling_count > new_falling_count:
            self.sound_manager.play_sound('powerup_collect')
        
        # Update balls
        balls_to_remove = []
        for ball in self.balls:
            # Apply slow power-up effect
            ball_speed = ball.speed
            if self.powerup_manager.is_active('slow'):
                ball_speed *= 0.5
            
            old_speed = ball.speed
            ball.speed = ball_speed
            ball.update(dt, self.paddle)
            ball.speed = old_speed
            
            # Check wall collisions
            wall_collisions = self.collision_detector.ball_wall_collision(ball)
            if wall_collisions:
                self.collision_detector.resolve_ball_wall_collision(ball, wall_collisions)
                for wall in wall_collisions:
                    if wall in ['left', 'right', 'top']:
                        self.sound_manager.play_sound('paddle_center', 0.3)
            
            # Check paddle collision
            if not ball.stuck_to_paddle:
                hit_position = self.collision_detector.ball_paddle_collision(ball, self.paddle)
                if hit_position is not None:
                    if self.paddle.is_sticky:
                        ball.stick_to_paddle(self.paddle)
                    else:
                        ball.bounce_paddle(self.paddle, hit_position)
                    self.sound_manager.play_paddle_hit(hit_position)
            
            # Check brick collisions
            for brick in self.bricks:
                if not brick.destroyed:
                    collision_side = self.collision_detector.ball_brick_collision(ball, brick)
                    if collision_side:
                        self.collision_detector.resolve_ball_brick_collision(ball, brick, collision_side)
                        
                        # Hit the brick
                        if brick.hit():
                            # Brick destroyed
                            self.game_score.add_points(brick.points)
                            self.powerup_manager.create_powerup(
                                brick.x + brick.width // 2,
                                brick.y + brick.height // 2
                            )
                        
                        self.sound_manager.play_brick_hit(brick.type)
                        break
            
            # Check laser collisions
            for laser in self.paddle.lasers[:]:
                for brick in self.bricks:
                    if not brick.destroyed and self.collision_detector.laser_brick_collision(laser, brick):
                        if brick.hit():
                            self.game_score.add_points(brick.points)
                            self.powerup_manager.create_powerup(
                                brick.x + brick.width // 2,
                                brick.y + brick.height // 2
                            )
                        self.sound_manager.play_brick_hit(brick.type)
                        self.paddle.lasers.remove(laser)
                        break
            
            # Check if ball fell below paddle
            if self.collision_detector.is_ball_below_paddle(ball, self.paddle):
                balls_to_remove.append(ball)
        
        # Remove fallen balls
        for ball in balls_to_remove:
            self.balls.remove(ball)
        
        # Check if all balls are lost
        if not self.balls:
            self.game_score.lose_life()
            if self.game_score.is_game_over():
                self.sound_manager.play_sound('game_over')
                self.check_high_score()
            else:
                self.sound_manager.play_sound('life_lost')
                # Respawn ball
                ball_x = self.paddle.x + self.paddle.width // 2
                ball_y = self.paddle.y - BALL_RADIUS - 10
                ball_speed = BALL_SPEED + (self.game_score.level - 1) * BALL_SPEED_INCREMENT
                ball_speed *= self.level_manager.get_ball_speed_multiplier(self.game_score.level)
                
                ball = Ball(ball_x, ball_y, ball_speed)
                ball.stick_to_paddle(self.paddle)
                self.balls = [ball]
        
        # Handle multi-ball power-up activation
        if self.powerup_manager.check_multiball_request():
            self.activate_multiball()
        
        # Check level completion
        if self.level_manager.is_level_complete(self.bricks):
            self.sound_manager.play_sound('level_complete')
            self.current_state = GameState.LEVEL_COMPLETE
            self.level_complete_timer = 0
        
        # Update bricks
        for brick in self.bricks:
            brick.update(dt)
    
    def activate_multiball(self):
        """Activate multi-ball power-up"""
        if len(self.balls) == 1:
            original_ball = self.balls[0]
            if not original_ball.stuck_to_paddle:
                # Create two additional balls
                for i in range(2):
                    new_ball = Ball(original_ball.x, original_ball.y, original_ball.speed)
                    angle_offset = (i + 1) * 0.5  # Different angles
                    new_ball.dx = original_ball.dx + angle_offset
                    new_ball.dy = original_ball.dy
                    new_ball.normalize_velocity()
                    self.balls.append(new_ball)
    
    def check_high_score(self):
        """Check if current score is a high score"""
        if self.score_manager.is_high_score(self.game_score.score):
            self.name_entry_menu = NameEntryMenu(self.game_score.score)
            self.current_state = GameState.NAME_ENTRY
        else:
            self.current_state = GameState.GAME_OVER
    
    def draw(self, screen):
        """Draw current game state"""
        if self.current_state == GameState.MAIN_MENU:
            self.main_menu.draw(screen)
        
        elif self.current_state == GameState.HIGH_SCORES:
            self.high_score_menu.draw(screen)
        
        elif self.current_state == GameState.CONTROLS:
            screen.fill(BACKGROUND)
            self.hud.draw_controls_help(screen)
        
        elif self.current_state in [GameState.PLAYING, GameState.PAUSED, GameState.LEVEL_COMPLETE]:
            self.draw_gameplay(screen)
            
            if self.current_state == GameState.PAUSED:
                self.hud.draw_pause_overlay(screen)
            elif self.current_state == GameState.LEVEL_COMPLETE:
                level_name = self.level_manager.get_level_name(self.game_score.level)
                self.hud.draw_level_complete(screen, self.game_score.level, self.game_score.score)
        
        elif self.current_state == GameState.GAME_OVER:
            self.draw_gameplay(screen)
            is_high_score = self.score_manager.is_high_score(self.game_score.score)
            self.hud.draw_game_over(screen, self.game_score.score, is_high_score)
        
        elif self.current_state == GameState.NAME_ENTRY:
            self.draw_gameplay(screen)
            if self.name_entry_menu:
                self.name_entry_menu.draw(screen)
    
    def draw_gameplay(self, screen):
        """Draw the main gameplay screen"""
        screen.fill(BACKGROUND)
        
        # Draw game area border
        border_rect = pygame.Rect(GAME_AREA_LEFT - 5, GAME_AREA_TOP - 5, 
                                 GAME_AREA_RIGHT - GAME_AREA_LEFT + 10,
                                 GAME_AREA_BOTTOM - GAME_AREA_TOP + 10)
        pygame.draw.rect(screen, BORDER_COLOR, border_rect, 3)
        
        # Draw game objects
        if self.paddle:
            self.paddle.draw(screen)
        
        for ball in self.balls:
            ball.draw(screen)
        
        for brick in self.bricks:
            if not brick.destroyed:
                brick.draw(screen)
        
        self.powerup_manager.draw(screen)
        
        # Draw HUD
        level_name = self.level_manager.get_level_name(self.game_score.level)
        self.hud.draw_score(screen, self.game_score.score)
        self.hud.draw_lives(screen, self.game_score.lives)
        self.hud.draw_level(screen, self.game_score.level, level_name)
        self.hud.draw_powerup_timers(screen, self.powerup_manager)
