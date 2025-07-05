# Game constants and configuration
import pygame

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors (RGB tuples)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Game area colors
BACKGROUND = (20, 25, 40)
BORDER_COLOR = (100, 120, 150)

# Paddle colors
PADDLE_COLOR = (70, 130, 180)
PADDLE_HIGHLIGHT = (100, 160, 220)

# Ball colors
BALL_COLOR = (255, 255, 255)
BALL_TRAIL = (200, 200, 255)

# Brick colors by type
BRICK_COLORS = {
    'normal': [(255, 100, 100), (255, 130, 130)],      # Red gradient
    'medium': [(100, 255, 100), (130, 255, 130)],      # Green gradient
    'hard': [(100, 100, 255), (130, 130, 255)],        # Blue gradient
    'unbreakable': [(128, 128, 128), (160, 160, 160)]  # Gray gradient
}

# Power-up colors
POWERUP_COLORS = {
    'multi_ball': (255, 215, 0),      # Gold
    'laser': (255, 69, 0),            # Red-orange
    'sticky': (50, 205, 50),          # Lime green
    'expand': (0, 191, 255),          # Deep sky blue
    'shrink': (255, 20, 147),         # Deep pink
    'slow': (138, 43, 226)            # Blue violet
}

# Game mechanics
PADDLE_SPEED = 8
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 15
PADDLE_Y_OFFSET = 50  # Distance from bottom of screen

BALL_RADIUS = 8
BALL_SPEED = 6
BALL_SPEED_INCREMENT = 0.3  # Speed increase per level

BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_PADDING = 2
BRICK_ROWS = 8
BRICK_COLS = 14

# Power-up settings
POWERUP_DROP_CHANCE = 0.15  # 15% chance
POWERUP_FALL_SPEED = 3
POWERUP_SIZE = 20
POWERUP_DURATION = {
    'laser': 15000,    # 15 seconds in milliseconds
    'sticky': 20000,   # 20 seconds
    'expand': 20000,   # 20 seconds
    'shrink': 20000,   # 20 seconds
    'slow': 15000      # 15 seconds
}

# Scoring
SCORE_NORMAL = 10
SCORE_MEDIUM = 20
SCORE_HARD = 30
SCORE_POWERUP = 50

# Lives
STARTING_LIVES = 3

# UI settings
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24

# Menu colors
MENU_BG = (30, 35, 50)
MENU_BUTTON = (70, 80, 120)
MENU_BUTTON_HOVER = (100, 110, 150)
MENU_TEXT = (255, 255, 255)

# Game area boundaries
GAME_AREA_TOP = 100
GAME_AREA_BOTTOM = SCREEN_HEIGHT - 50
GAME_AREA_LEFT = 50
GAME_AREA_RIGHT = SCREEN_WIDTH - 50

# Level progression
TOTAL_LEVELS = 10
