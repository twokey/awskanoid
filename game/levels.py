from typing import List, Dict, Tuple
from game.entities import Brick
from utils.constants import *

class LevelManager:
    def __init__(self):
        self.levels = self.create_levels()
        self.current_level = 1
    
    def create_levels(self) -> Dict[int, Dict]:
        """Create all 10 levels with increasing difficulty"""
        levels = {}
        
        # Level 1: Simple pattern, mostly normal bricks
        levels[1] = {
            'name': 'Getting Started',
            'pattern': [
                'NNNNNNNNNNNNNN',
                'NNNNNNNNNNNNNN',
                'NNNNNNNNNNNNNN',
                '              ',
                '              ',
                '              ',
                '              ',
                '              '
            ],
            'ball_speed_multiplier': 1.0
        }
        
        # Level 2: Introduce medium bricks
        levels[2] = {
            'name': 'Stepping Up',
            'pattern': [
                'NNNNNNNNNNNNNN',
                'MMMMMMMMMMMMMM',
                'NNNNNNNNNNNNNN',
                'MMMMMMMMMMMMMM',
                '              ',
                '              ',
                '              ',
                '              '
            ],
            'ball_speed_multiplier': 1.1
        }
        
        # Level 3: Add hard bricks
        levels[3] = {
            'name': 'Getting Harder',
            'pattern': [
                'HHHHHHHHHHHHHH',
                'MMMMMMMMMMMMMM',
                'NNNNNNNNNNNNNN',
                'MMMMMMMMMMMMMM',
                'HHHHHHHHHHHHHH',
                '              ',
                '              ',
                '              '
            ],
            'ball_speed_multiplier': 1.2
        }
        
        # Level 4: Introduce unbreakable bricks
        levels[4] = {
            'name': 'Obstacles',
            'pattern': [
                'NNNNNNNNNNNNNN',
                'NUUUUUUUUUUUUN',
                'NMMMMMMMMMMMNN',
                'NUUUUUUUUUUUUN',
                'NNNNNNNNNNNNNN',
                '              ',
                '              ',
                '              '
            ],
            'ball_speed_multiplier': 1.3
        }
        
        # Level 5: Complex pattern
        levels[5] = {
            'name': 'Maze Runner',
            'pattern': [
                'HUHUHUHUHUHUH ',
                'UMUMUMUMUMUMUM',
                'HUHUHUHUHUHUH ',
                'UMUMUMUMUMUMUM',
                'HUHUHUHUHUHUH ',
                'NNNNNNNNNNNNNN',
                '              ',
                '              '
            ],
            'ball_speed_multiplier': 1.4
        }
        
        # Level 6: Diamond pattern
        levels[6] = {
            'name': 'Diamond Formation',
            'pattern': [
                '      HH      ',
                '     HMMH     ',
                '    HMNNMH    ',
                '   HMNNNNMH   ',
                '    HMNNMH    ',
                '     HMMH     ',
                '      HH      ',
                '              '
            ],
            'ball_speed_multiplier': 1.5
        }
        
        # Level 7: Fortress
        levels[7] = {
            'name': 'The Fortress',
            'pattern': [
                'UUUUUUUUUUUUUU',
                'UHHHHHHHHHHHHU',
                'UHMMMMMMMMMMHU',
                'UHMNNNNNNNMHHU',
                'UHMMMMMMMMMMHU',
                'UHHHHHHHHHHHHU',
                'UUUUUUUUUUUUUU',
                '              '
            ],
            'ball_speed_multiplier': 1.6
        }
        
        # Level 8: Checkerboard
        levels[8] = {
            'name': 'Checkerboard',
            'pattern': [
                'HUHUHUHUHUHUH ',
                'UHUHUHUHUHUHUH',
                'HUHUHUHUHUHUH ',
                'UHUHUHUHUHUHUH',
                'HUHUHUHUHUHUH ',
                'UHUHUHUHUHUHUH',
                'HUHUHUHUHUHUH ',
                '              '
            ],
            'ball_speed_multiplier': 1.7
        }
        
        # Level 9: The Gauntlet
        levels[9] = {
            'name': 'The Gauntlet',
            'pattern': [
                'UUUUUUUUUUUUUU',
                'UHHHHHHHHHHHU ',
                'UHMMMMMMMMHHU ',
                'UHMNNNNNMHHUU ',
                'UHMMMMMMHHUUU ',
                'UHHHHHHHHUUUU ',
                'UUUUUUUUUUUUU ',
                'NNNNNNNNNNNNNN'
            ],
            'ball_speed_multiplier': 1.8
        }
        
        # Level 10: Final Boss
        levels[10] = {
            'name': 'Final Challenge',
            'pattern': [
                'UUUUUUUUUUUUUU',
                'UHHHHHHHHHHHU ',
                'UHMMMMMMMMHHU ',
                'UHMNNNNNMHHUU ',
                'UHMNUUUNMHHUU ',
                'UHMNNNNNMHHUU ',
                'UHMMMMMMMMHHU ',
                'UHHHHHHHHHHHU '
            ],
            'ball_speed_multiplier': 2.0
        }
        
        return levels
    
    def get_level(self, level_num: int) -> Dict:
        """Get level data for specified level number"""
        return self.levels.get(level_num, self.levels[1])
    
    def create_bricks_for_level(self, level_num: int) -> List[Brick]:
        """Create brick objects for the specified level"""
        level_data = self.get_level(level_num)
        pattern = level_data['pattern']
        bricks = []
        
        # Calculate starting position to center the brick field
        total_width = BRICK_COLS * (BRICK_WIDTH + BRICK_PADDING) - BRICK_PADDING
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = GAME_AREA_TOP + 50
        
        brick_type_map = {
            'N': 'normal',
            'M': 'medium', 
            'H': 'hard',
            'U': 'unbreakable',
            ' ': None
        }
        
        for row_idx, row in enumerate(pattern):
            for col_idx, brick_char in enumerate(row):
                if col_idx >= BRICK_COLS:
                    break
                
                brick_type = brick_type_map.get(brick_char)
                if brick_type:
                    x = start_x + col_idx * (BRICK_WIDTH + BRICK_PADDING)
                    y = start_y + row_idx * (BRICK_HEIGHT + BRICK_PADDING)
                    bricks.append(Brick(x, y, brick_type))
        
        return bricks
    
    def get_level_name(self, level_num: int) -> str:
        """Get the name of the specified level"""
        level_data = self.get_level(level_num)
        return level_data.get('name', f'Level {level_num}')
    
    def get_ball_speed_multiplier(self, level_num: int) -> float:
        """Get the ball speed multiplier for the specified level"""
        level_data = self.get_level(level_num)
        return level_data.get('ball_speed_multiplier', 1.0)
    
    def is_level_complete(self, bricks: List[Brick]) -> bool:
        """Check if the current level is complete (all breakable bricks destroyed)"""
        for brick in bricks:
            if not brick.destroyed and brick.type != 'unbreakable':
                return False
        return True
    
    def get_total_breakable_bricks(self, level_num: int) -> int:
        """Get the total number of breakable bricks in a level"""
        bricks = self.create_bricks_for_level(level_num)
        return sum(1 for brick in bricks if brick.type != 'unbreakable')
    
    def get_max_score_for_level(self, level_num: int) -> int:
        """Calculate the maximum possible score for a level"""
        bricks = self.create_bricks_for_level(level_num)
        total_score = 0
        
        for brick in bricks:
            if brick.type != 'unbreakable':
                total_score += brick.points
        
        # Add level completion bonus
        total_score += 1000
        
        return total_score
    
    def get_level_stats(self, level_num: int) -> Dict:
        """Get statistics about a level"""
        bricks = self.create_bricks_for_level(level_num)
        stats = {
            'total_bricks': len(bricks),
            'breakable_bricks': 0,
            'normal_bricks': 0,
            'medium_bricks': 0,
            'hard_bricks': 0,
            'unbreakable_bricks': 0,
            'max_score': 0
        }
        
        for brick in bricks:
            if brick.type == 'normal':
                stats['normal_bricks'] += 1
                stats['breakable_bricks'] += 1
                stats['max_score'] += brick.points
            elif brick.type == 'medium':
                stats['medium_bricks'] += 1
                stats['breakable_bricks'] += 1
                stats['max_score'] += brick.points
            elif brick.type == 'hard':
                stats['hard_bricks'] += 1
                stats['breakable_bricks'] += 1
                stats['max_score'] += brick.points
            elif brick.type == 'unbreakable':
                stats['unbreakable_bricks'] += 1
        
        # Add level completion bonus
        stats['max_score'] += 1000
        
        return stats
