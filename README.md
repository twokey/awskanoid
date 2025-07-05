# AWSKANOID - A Modern Arkanoid/Breakout Clone

A single-player brick-breaking arcade game built with Pygame, featuring 10 pre-designed levels, modern vector-style graphics, and various power-ups.

## Features

### Core Gameplay
- **10 Pre-designed Levels**: Each with unique brick patterns and increasing difficulty
- **Modern Vector Graphics**: Clean shapes and gradients, no pixel art
- **Smooth 60 FPS Gameplay**: Frame-independent movement for consistent experience
- **1280x720 Resolution**: 16:9 aspect ratio, perfect for modern displays

### Game Mechanics
- **Realistic Ball Physics**: Angle reflection based on paddle hit location
- **Multiple Brick Types**:
  - Normal bricks (1 hit, 10 points)
  - Medium bricks (2 hits, 20 points, change color when damaged)
  - Hard bricks (3 hits, 30 points, change color with each hit)
  - Unbreakable bricks (metallic appearance, no points)

### Power-up System
- **Multi-ball**: Splits current ball into 3 balls
- **Laser Paddle**: Shoot lasers for 15 seconds (spacebar to fire)
- **Sticky Paddle**: Ball sticks to paddle on contact
- **Expand Paddle**: Increases paddle width by 50% for 20 seconds
- **Shrink Paddle**: Decreases paddle width by 50% for 20 seconds (negative power-up)
- **Slow Ball**: Reduces ball speed by 50% for 15 seconds

### Audio
- Dynamic sound effects generated using Pygame
- Different sounds for different brick types
- Paddle hit sounds vary based on hit location
- Power-up collection and game event sounds

## Controls

- **Arrow Keys / Mouse**: Move paddle
- **Spacebar**: Release ball from paddle / Shoot laser (when laser power-up is active)
- **ESC**: Pause game / Access pause menu
- **F1**: Toggle FPS counter (debug feature)

## Installation

1. **Install Python 3.7+** (if not already installed)

2. **Install required dependencies**:
   ```bash
   pip install pygame numpy
   ```
   
   Or using the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

## Game Structure

```
arkanoid_game/
├── main.py              # Entry point and game loop
├── game/
│   ├── game_states.py   # Menu, gameplay, pause, game over states
│   ├── entities.py      # Ball, Paddle, Brick classes
│   ├── powerups.py      # Power-up system and types
│   ├── levels.py        # Level definitions and loader
│   └── collision.py     # Collision detection logic
├── ui/
│   ├── menu.py          # Menu systems
│   └── hud.py           # In-game UI elements
├── utils/
│   ├── constants.py     # Game constants (screen size, colors, speeds)
│   ├── sounds.py        # Sound effect generation and management
│   └── score.py         # Score and high score management
└── assets/
    └── levels/          # Level definition files
```

## Gameplay Tips

1. **Paddle Control**: The ball's angle changes based on where it hits the paddle:
   - Left edge = sharp left angle
   - Center = straight up
   - Right edge = sharp right angle

2. **Power-up Strategy**: 
   - Collect power-ups by moving the paddle to catch falling items
   - Some power-ups stack (like laser + expand paddle)
   - Watch out for the shrink power-up (it's bad!)

3. **Level Progression**:
   - Ball speed increases with each level
   - Later levels have more unbreakable bricks as obstacles
   - Complete a level by destroying all breakable bricks

4. **Scoring**:
   - Normal bricks: 10 points
   - Medium bricks: 20 points  
   - Hard bricks: 30 points
   - Level completion bonus: 1000 points
   - Power-up collection: 50 points

## High Scores

- Top 10 scores are saved automatically
- Enter your 3-letter name for high scores (classic arcade style)
- Scores include points, level reached, and date

## System Requirements

- **Operating System**: macOS (optimized for), Windows, Linux
- **Python**: 3.7 or higher
- **RAM**: 256 MB minimum
- **Display**: 1280x720 or higher resolution recommended

## Development Notes

- Built using object-oriented design principles
- State machine pattern for game states
- Modular code structure for easy expansion
- Frame-independent movement using delta time
- Clean collision detection system

## Future Enhancements (Not in v1)

- Level editor
- Save game functionality
- Particle effects
- Additional power-ups
- Multiplayer support
- Custom soundtracks

## Troubleshooting

**Game won't start:**
- Make sure Pygame is installed: `pip install pygame`
- Check Python version: `python --version` (should be 3.7+)

**No sound effects:**
- Install NumPy: `pip install numpy`
- Check system audio settings

**Performance issues:**
- Close other applications
- Try running in windowed mode
- Check if your system meets minimum requirements

## License

This game is created as a demonstration project. Feel free to use and modify for educational purposes.

## Credits

- Built with Pygame
- Sound generation using NumPy
- Inspired by classic Arkanoid and Breakout games
- Created by Amazon Q

---

**Have fun breaking bricks!** 🧱⚡
