import json
import os
from datetime import datetime
from typing import List, Dict, Tuple

class ScoreManager:
    def __init__(self):
        self.high_scores_file = "high_scores.json"
        self.high_scores = self.load_high_scores()
    
    def load_high_scores(self) -> List[Dict]:
        """Load high scores from file"""
        if os.path.exists(self.high_scores_file):
            try:
                with open(self.high_scores_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Return default empty high scores
        return []
    
    def save_high_scores(self):
        """Save high scores to file"""
        try:
            with open(self.high_scores_file, 'w') as f:
                json.dump(self.high_scores, f, indent=2)
        except Exception as e:
            print(f"Error saving high scores: {e}")
    
    def add_score(self, player_name: str, score: int, level_reached: int) -> bool:
        """Add a new score and return True if it's a high score"""
        new_score = {
            'name': player_name.upper()[:3],  # Limit to 3 characters, uppercase
            'score': score,
            'level': level_reached,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        self.high_scores.append(new_score)
        
        # Sort by score (descending) and keep top 10
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        is_high_score = len(self.high_scores) <= 10 or new_score in self.high_scores[:10]
        self.high_scores = self.high_scores[:10]
        
        self.save_high_scores()
        return is_high_score
    
    def get_high_scores(self) -> List[Dict]:
        """Get the current high scores list"""
        return self.high_scores.copy()
    
    def is_high_score(self, score: int) -> bool:
        """Check if a score qualifies as a high score"""
        if len(self.high_scores) < 10:
            return True
        return score > self.high_scores[-1]['score']
    
    def get_rank(self, score: int) -> int:
        """Get the rank a score would have (1-based)"""
        rank = 1
        for high_score in self.high_scores:
            if score > high_score['score']:
                break
            rank += 1
        return min(rank, 11)  # Cap at 11 (not in top 10)

class GameScore:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.multiplier = 1
    
    def add_points(self, points: int):
        """Add points to the current score"""
        self.score += points * self.multiplier
    
    def lose_life(self):
        """Lose a life"""
        self.lives = max(0, self.lives - 1)
    
    def gain_life(self):
        """Gain an extra life (bonus for high scores)"""
        self.lives += 1
    
    def next_level(self):
        """Advance to the next level"""
        self.level += 1
        # Bonus points for completing a level
        self.add_points(1000)
    
    def reset(self):
        """Reset score for new game"""
        self.score = 0
        self.lives = 3
        self.level = 1
        self.multiplier = 1
    
    def is_game_over(self) -> bool:
        """Check if the game is over"""
        return self.lives <= 0
