import json
import os
from utils.constants import *

class SettingsManager:
    def __init__(self):
        self.settings_file = "game_settings.json"
        self.settings = self.load_settings()
    
    def load_settings(self) -> dict:
        """Load settings from file"""
        default_settings = {
            'control_mode': DEFAULT_CONTROL_MODE,
            'sound_enabled': True,
            'show_fps': False
        }
        
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_settings.update(loaded_settings)
                    return default_settings
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        return default_settings
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get_control_mode(self) -> str:
        """Get current control mode"""
        return self.settings.get('control_mode', DEFAULT_CONTROL_MODE)
    
    def set_control_mode(self, mode: str):
        """Set control mode"""
        if mode in [CONTROL_MODE_KEYBOARD, CONTROL_MODE_MOUSE]:
            self.settings['control_mode'] = mode
            self.save_settings()
    
    def is_keyboard_mode(self) -> bool:
        """Check if keyboard mode is active"""
        return self.get_control_mode() == CONTROL_MODE_KEYBOARD
    
    def is_mouse_mode(self) -> bool:
        """Check if mouse mode is active"""
        return self.get_control_mode() == CONTROL_MODE_MOUSE
    
    def toggle_control_mode(self):
        """Toggle between keyboard and mouse control"""
        current_mode = self.get_control_mode()
        new_mode = CONTROL_MODE_MOUSE if current_mode == CONTROL_MODE_KEYBOARD else CONTROL_MODE_KEYBOARD
        self.set_control_mode(new_mode)
    
    def get_setting(self, key: str, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()
