# AWSKANOID - Project Overview

## Project Structure

```
arkanoid_game/
├── main.py                 # Main entry point and game loop
├── launch_game.sh          # Launcher script for easy execution
├── test_game.py           # Component testing script
├── requirements.txt       # Python dependencies
├── README.md             # User documentation
├── PROJECT_OVERVIEW.md   # This file
│
├── game/                 # Core game logic
│   ├── __init__.py
│   ├── game_states.py    # State machine (menu, playing, paused, etc.)
│   ├── entities.py       # Game objects (Ball, Paddle, Brick, Laser)
│   ├── powerups.py       # Power-up system and management
│   ├── levels.py         # Level definitions and loading
│   └── collision.py      # Collision detection algorithms
│
├── ui/                   # User interface components
│   ├── __init__.py
│   ├── menu.py           # Menu systems (main, high scores, name entry)
│   └── hud.py            # In-game UI (score, lives, timers)
│
├── utils/                # Utility modules
│   ├── __init__.py
│   ├── constants.py      # Game constants and configuration
│   ├── sounds.py         # Sound generation and management
│   └── score.py          # Score tracking and high score system
│
└── assets/               # Game assets (currently unused)
    └── levels/           # Level definition files (for future expansion)
```

## Key Features Implemented

### ✅ Core Game Requirements
- [x] Single-player brick-breaking arcade game
- [x] 10 pre-designed levels with unique patterns
- [x] 1280x720 windowed mode (16:9 aspect ratio)
- [x] 60 FPS smooth gameplay
- [x] Modern vector-style graphics with gradients

### ✅ Game Mechanics
- [x] Realistic ball physics with angle reflection
- [x] Ball angle changes based on paddle hit location
- [x] Ball speed increases with level progression
- [x] Keyboard (arrow keys) and mouse paddle controls
- [x] Paddle boundary constraints

### ✅ Brick System
- [x] Normal bricks (1 hit, 10 points)
- [x] Medium bricks (2 hits, 20 points, color change when damaged)
- [x] Hard bricks (3 hits, 30 points, color change with each hit)
- [x] Unbreakable bricks (metallic appearance, no points)
- [x] Visual feedback when bricks are hit (flash effect)

### ✅ Power-up System
- [x] Multi-ball: Splits current ball into 3 balls
- [x] Laser paddle: Shoot lasers for 15 seconds (spacebar to fire)
- [x] Sticky paddle: Ball sticks to paddle on contact
- [x] Expand paddle: Increases paddle width by 50% for 20 seconds
- [x] Shrink paddle: Decreases paddle width by 50% for 20 seconds
- [x] Slow ball: Reduces ball speed by 50% for 15 seconds
- [x] Power-ups fall slowly and are collected by paddle contact
- [x] 15% drop chance from destroyed bricks

### ✅ Lives System
- [x] Player starts with 3 lives
- [x] Lose life when ball falls below paddle
- [x] Game over when all lives are lost
- [x] Option to restart from level 1 or quit to main menu

### ✅ User Interface
- [x] Main menu with "AWSKANOID" title
- [x] Start Game, High Scores, Controls, Quit options
- [x] Modern UI with hover effects on buttons
- [x] Pause menu (ESC key) with Resume, Restart, Main Menu
- [x] Semi-transparent overlays
- [x] High score screen with top 10 scores
- [x] 3-letter player name input (classic arcade style)
- [x] HUD with score, lives (paddle icons), level number
- [x] Active power-up timers display

### ✅ Audio System
- [x] Procedurally generated sound effects using NumPy
- [x] Ball paddle hit sounds (different pitch based on hit location)
- [x] Brick destruction sounds (different for each brick type)
- [x] Power-up collection sound
- [x] Life lost sound
- [x] Level complete fanfare
- [x] Game over sound

### ✅ Code Organization
- [x] Clean modular structure following best practices
- [x] Object-oriented design with clear separation of concerns
- [x] State machine pattern for game states
- [x] Frame-independent movement using delta time
- [x] Comprehensive collision detection system

### ✅ Level Design
- [x] 10 pre-designed levels with increasing difficulty
- [x] Unique brick patterns for each level
- [x] Progressive introduction of different brick types
- [x] Later levels include more unbreakable bricks as obstacles
- [x] Level complete when all breakable bricks are destroyed

### ✅ Technical Specifications
- [x] Latest stable Pygame version support
- [x] Vector math for ball physics calculations
- [x] Clean collision detection between ball/paddle/bricks
- [x] Smooth gameplay at 60 FPS
- [x] All graphics drawn using Pygame's drawing functions
- [x] Proper game window title and icon
- [x] Update and render separation in game loop

## Game Controls

| Input | Action |
|-------|--------|
| Arrow Keys / Mouse | Move paddle |
| Spacebar | Release ball from paddle / Shoot laser |
| ESC | Pause game / Access pause menu |
| F1 | Toggle FPS counter (debug) |
| R | Restart level (when paused/game over) |
| M | Return to main menu (when paused) |

## Power-up Effects

| Power-up | Effect | Duration | Visual |
|----------|--------|----------|--------|
| Multi-ball | Splits ball into 3 | Instant | Gold diamond |
| Laser | Paddle shoots lasers | 15 seconds | Red-orange diamond |
| Sticky | Ball sticks to paddle | 20 seconds | Green diamond |
| Expand | Paddle width +50% | 20 seconds | Blue diamond |
| Shrink | Paddle width -50% | 20 seconds | Pink diamond |
| Slow | Ball speed -50% | 15 seconds | Purple diamond |

## Level Progression

1. **Getting Started** - Simple pattern, normal bricks only
2. **Stepping Up** - Introduces medium bricks
3. **Getting Harder** - Adds hard bricks
4. **Obstacles** - First unbreakable bricks
5. **Maze Runner** - Complex alternating pattern
6. **Diamond Formation** - Diamond-shaped brick layout
7. **The Fortress** - Fortress-like defensive pattern
8. **Checkerboard** - Alternating brick pattern
9. **The Gauntlet** - Dense defensive layout
10. **Final Challenge** - Ultimate test with all brick types

## Performance Notes

- Optimized for 60 FPS gameplay
- Frame-independent movement ensures consistent speed across different hardware
- Efficient collision detection using bounding rectangles
- Sound generation cached for performance
- Minimal memory allocation during gameplay

## Future Enhancement Possibilities

- Level editor for custom levels
- Save game functionality
- Particle effects for brick destruction
- Additional power-ups
- Multiplayer support
- Custom soundtracks
- Achievements system
- Different paddle types
- Boss levels

## Testing

Run `python3 test_game.py` to verify all components work correctly before playing.

## Installation & Running

1. Install dependencies: `pip3 install pygame numpy`
2. Run game: `python3 main.py`
3. Or use launcher: `./launch_game.sh`

The game has been tested and verified to work on macOS with Python 3.9+ and the specified dependencies.
