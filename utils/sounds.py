import pygame
import numpy as np
import math

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.generate_sounds()
    
    def generate_tone(self, frequency, duration, volume=0.5, fade_out=True):
        """Generate a simple tone"""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            time = float(i) / sample_rate
            wave = volume * math.sin(2 * math.pi * frequency * time)
            
            # Apply fade out to prevent clicking
            if fade_out and i > frames * 0.8:
                fade_factor = 1.0 - (i - frames * 0.8) / (frames * 0.2)
                wave *= fade_factor
            
            arr[i][0] = wave  # Left channel
            arr[i][1] = wave  # Right channel
        
        # Convert to 16-bit integers
        arr = (arr * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def generate_noise(self, duration, volume=0.3):
        """Generate white noise for destruction sounds"""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.random.uniform(-volume, volume, (frames, 2))
        
        # Apply envelope
        for i in range(frames):
            fade_factor = 1.0 - (i / frames)
            arr[i] *= fade_factor
        
        arr = (arr * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def generate_sounds(self):
        """Generate all game sounds"""
        # Paddle hit sounds (different pitches based on hit location)
        self.sounds['paddle_left'] = self.generate_tone(220, 0.1)    # A3
        self.sounds['paddle_center'] = self.generate_tone(330, 0.1)  # E4
        self.sounds['paddle_right'] = self.generate_tone(440, 0.1)   # A4
        
        # Brick destruction sounds
        self.sounds['brick_normal'] = self.generate_tone(523, 0.15)   # C5
        self.sounds['brick_medium'] = self.generate_tone(659, 0.15)   # E5
        self.sounds['brick_hard'] = self.generate_tone(784, 0.15)     # G5
        self.sounds['brick_unbreakable'] = self.generate_noise(0.1, 0.2)
        
        # Power-up sounds
        self.sounds['powerup_collect'] = self.generate_tone(880, 0.2) # A5
        
        # Game event sounds
        self.sounds['life_lost'] = self.generate_tone(147, 0.5)       # D3 (low, sad)
        self.sounds['game_over'] = self.generate_tone(110, 1.0)       # A2 (very low)
        
        # Level complete fanfare (simple ascending notes)
        self.sounds['level_complete'] = self.generate_fanfare()
    
    def generate_fanfare(self):
        """Generate a simple fanfare for level completion"""
        notes = [523, 659, 784, 1047]  # C5, E5, G5, C6
        sample_rate = 22050
        total_duration = 1.0
        note_duration = total_duration / len(notes)
        frames_per_note = int(note_duration * sample_rate)
        total_frames = frames_per_note * len(notes)
        
        arr = np.zeros((total_frames, 2))
        
        for note_idx, frequency in enumerate(notes):
            start_frame = note_idx * frames_per_note
            for i in range(frames_per_note):
                time = float(i) / sample_rate
                wave = 0.4 * math.sin(2 * math.pi * frequency * time)
                
                # Fade in/out each note
                if i < frames_per_note * 0.1:
                    wave *= i / (frames_per_note * 0.1)
                elif i > frames_per_note * 0.9:
                    fade_factor = 1.0 - (i - frames_per_note * 0.9) / (frames_per_note * 0.1)
                    wave *= fade_factor
                
                arr[start_frame + i][0] = wave
                arr[start_frame + i][1] = wave
        
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def play_sound(self, sound_name, volume=1.0):
        """Play a sound by name"""
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            sound.set_volume(volume)
            sound.play()
    
    def play_paddle_hit(self, hit_position):
        """Play paddle hit sound based on hit position (-1 to 1)"""
        if hit_position < -0.3:
            self.play_sound('paddle_left')
        elif hit_position > 0.3:
            self.play_sound('paddle_right')
        else:
            self.play_sound('paddle_center')
    
    def play_brick_hit(self, brick_type):
        """Play appropriate sound for brick type"""
        sound_map = {
            'normal': 'brick_normal',
            'medium': 'brick_medium',
            'hard': 'brick_hard',
            'unbreakable': 'brick_unbreakable'
        }
        self.play_sound(sound_map.get(brick_type, 'brick_normal'))
