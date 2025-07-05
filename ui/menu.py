import pygame
from typing import List, Tuple, Optional
from utils.constants import *
from utils.score import ScoreManager
from utils.settings import SettingsManager

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False
        self.clicked = False
    
    def update(self, mouse_pos: Tuple[int, int], mouse_clicked: bool):
        """Update button state based on mouse input"""
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.clicked = self.hovered and mouse_clicked
    
    def draw(self, screen):
        """Draw the button"""
        # Choose colors based on state
        bg_color = MENU_BUTTON_HOVER if self.hovered else MENU_BUTTON
        text_color = WHITE
        
        # Draw button background
        pygame.draw.rect(screen, bg_color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Draw button text
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text_surface, text_rect)

class MainMenu:
    def __init__(self):
        pygame.font.init()
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_spacing = 70
        start_y = SCREEN_HEIGHT // 2 - 50
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.buttons = [
            Button(center_x, start_y, button_width, button_height, "Start Game", self.font_medium),
            Button(center_x, start_y + button_spacing, button_width, button_height, "High Scores", self.font_medium),
            Button(center_x, start_y + button_spacing * 2, button_width, button_height, "Settings", self.font_medium),
            Button(center_x, start_y + button_spacing * 3, button_width, button_height, "Quit", self.font_medium)
        ]
    
    def update(self, mouse_pos: Tuple[int, int], mouse_clicked: bool) -> Optional[str]:
        """Update menu and return action if button clicked"""
        for i, button in enumerate(self.buttons):
            button.update(mouse_pos, mouse_clicked)
            if button.clicked:
                if i == 0:
                    return "start_game"
                elif i == 1:
                    return "high_scores"
                elif i == 2:
                    return "settings"
                elif i == 3:
                    return "quit"
        return None
    
    def draw(self, screen):
        """Draw the main menu"""
        screen.fill(MENU_BG)
        
        # Draw title with glow effect
        title_text = "AWSKANOID"
        
        # Glow effect
        for offset in range(5, 0, -1):
            glow_color = tuple(min(255, c + offset * 10) for c in (70, 130, 180))
            glow_surface = self.font_large.render(title_text, True, glow_color)
            glow_rect = glow_surface.get_rect()
            glow_rect.center = (SCREEN_WIDTH // 2 + offset, 150 + offset)
            screen.blit(glow_surface, glow_rect)
        
        # Main title
        title_surface = self.font_large.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2, 150)
        screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = "A Modern Breakout Experience"
        subtitle_surface = self.font_small.render(subtitle_text, True, LIGHT_GRAY)
        subtitle_rect = subtitle_surface.get_rect()
        subtitle_rect.center = (SCREEN_WIDTH // 2, 190)
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)
        
        # Draw version info
        version_text = "v1.0 - Built with Pygame"
        version_surface = self.font_small.render(version_text, True, GRAY)
        screen.blit(version_surface, (10, SCREEN_HEIGHT - 30))

class HighScoreMenu:
    def __init__(self, score_manager: ScoreManager):
        pygame.font.init()
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.score_manager = score_manager
        
        # Back button
        self.back_button = Button(50, SCREEN_HEIGHT - 100, 100, 40, "Back", self.font_small)
    
    def update(self, mouse_pos: Tuple[int, int], mouse_clicked: bool) -> Optional[str]:
        """Update high score menu"""
        self.back_button.update(mouse_pos, mouse_clicked)
        if self.back_button.clicked:
            return "main_menu"
        return None
    
    def draw(self, screen):
        """Draw the high scores menu"""
        screen.fill(MENU_BG)
        
        # Title
        title_text = "HIGH SCORES"
        title_surface = self.font_large.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2, 80)
        screen.blit(title_surface, title_rect)
        
        # Column headers
        headers = ["Rank", "Name", "Score", "Level", "Date"]
        header_positions = [200, 350, 500, 650, 800]
        
        for i, header in enumerate(headers):
            header_surface = self.font_medium.render(header, True, (255, 215, 0))
            screen.blit(header_surface, (header_positions[i], 150))
        
        # Draw line under headers
        pygame.draw.line(screen, WHITE, (150, 180), (SCREEN_WIDTH - 150, 180), 2)
        
        # High scores
        high_scores = self.score_manager.get_high_scores()
        
        if not high_scores:
            no_scores_text = "No high scores yet! Play a game to set the first record."
            no_scores_surface = self.font_medium.render(no_scores_text, True, GRAY)
            no_scores_rect = no_scores_surface.get_rect()
            no_scores_rect.center = (SCREEN_WIDTH // 2, 300)
            screen.blit(no_scores_surface, no_scores_rect)
        else:
            for i, score_entry in enumerate(high_scores[:10]):
                y_pos = 200 + i * 35
                
                # Rank
                rank_text = f"{i + 1}."
                rank_surface = self.font_small.render(rank_text, True, WHITE)
                screen.blit(rank_surface, (header_positions[0], y_pos))
                
                # Name
                name_surface = self.font_small.render(score_entry['name'], True, WHITE)
                screen.blit(name_surface, (header_positions[1], y_pos))
                
                # Score
                score_text = f"{score_entry['score']:,}"
                score_surface = self.font_small.render(score_text, True, WHITE)
                screen.blit(score_surface, (header_positions[2], y_pos))
                
                # Level
                level_text = str(score_entry['level'])
                level_surface = self.font_small.render(level_text, True, WHITE)
                screen.blit(level_surface, (header_positions[3], y_pos))
                
                # Date
                date_surface = self.font_small.render(score_entry['date'], True, WHITE)
                screen.blit(date_surface, (header_positions[4], y_pos))
        
        # Back button
        self.back_button.draw(screen)

class NameEntryMenu:
    def __init__(self, final_score: int):
        pygame.font.init()
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        self.final_score = final_score
        self.player_name = ""
        self.cursor_visible = True
        self.cursor_timer = 0
        self.max_length = 3
    
    def update(self, dt: float, events: List[pygame.event.Event]) -> Optional[str]:
        """Update name entry menu"""
        # Update cursor blink
        self.cursor_timer += dt * 1000
        if self.cursor_timer >= 500:  # Blink every 500ms
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if len(self.player_name) > 0:
                        return self.player_name
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return "AAA"  # Default name if escaped
                else:
                    # Add character if it's a letter and we haven't reached max length
                    if len(self.player_name) < self.max_length and event.unicode.isalpha():
                        self.player_name += event.unicode.upper()
        
        return None
    
    def draw(self, screen):
        """Draw the name entry menu"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Congratulations text
        congrats_text = "NEW HIGH SCORE!"
        congrats_surface = self.font_large.render(congrats_text, True, (255, 215, 0))
        congrats_rect = congrats_surface.get_rect()
        congrats_rect.center = (SCREEN_WIDTH // 2, 200)
        screen.blit(congrats_surface, congrats_rect)
        
        # Score
        score_text = f"Score: {self.final_score:,}"
        score_surface = self.font_medium.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect()
        score_rect.center = (SCREEN_WIDTH // 2, 250)
        screen.blit(score_surface, score_rect)
        
        # Name entry prompt
        prompt_text = "Enter your name (3 letters):"
        prompt_surface = self.font_medium.render(prompt_text, True, WHITE)
        prompt_rect = prompt_surface.get_rect()
        prompt_rect.center = (SCREEN_WIDTH // 2, 320)
        screen.blit(prompt_surface, prompt_rect)
        
        # Name input box
        box_width = 200
        box_height = 50
        box_x = SCREEN_WIDTH // 2 - box_width // 2
        box_y = 360
        
        pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, BLACK, (box_x + 2, box_y + 2, box_width - 4, box_height - 4))
        
        # Display current name
        name_display = self.player_name
        if self.cursor_visible and len(self.player_name) < self.max_length:
            name_display += "_"
        
        name_surface = self.font_large.render(name_display, True, WHITE)
        name_rect = name_surface.get_rect()
        name_rect.center = (SCREEN_WIDTH // 2, box_y + box_height // 2)
        screen.blit(name_surface, name_rect)
        
        # Instructions
        instruction_text = "Press ENTER when done, ESC to skip"
        instruction_surface = self.font_small.render(instruction_text, True, GRAY)
        instruction_rect = instruction_surface.get_rect()
        instruction_rect.center = (SCREEN_WIDTH // 2, 450)
        screen.blit(instruction_surface, instruction_rect)

class ControlSettingsMenu:
    def __init__(self, settings_manager: SettingsManager):
        pygame.font.init()
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.settings_manager = settings_manager
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_spacing = 80
        start_y = SCREEN_HEIGHT // 2 - 50
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.keyboard_button = Button(center_x, start_y, button_width, button_height, "Keyboard", self.font_medium)
        self.mouse_button = Button(center_x, start_y + button_spacing, button_width, button_height, "Mouse", self.font_medium)
        self.back_button = Button(50, SCREEN_HEIGHT - 100, 100, 40, "Back", self.font_small)
    
    def update(self, mouse_pos: Tuple[int, int], mouse_clicked: bool) -> Optional[str]:
        """Update control settings menu"""
        self.keyboard_button.update(mouse_pos, mouse_clicked)
        self.mouse_button.update(mouse_pos, mouse_clicked)
        self.back_button.update(mouse_pos, mouse_clicked)
        
        if self.keyboard_button.clicked:
            self.settings_manager.set_control_mode(CONTROL_MODE_KEYBOARD)
        elif self.mouse_button.clicked:
            self.settings_manager.set_control_mode(CONTROL_MODE_MOUSE)
        elif self.back_button.clicked:
            return "main_menu"
        
        return None
    
    def draw(self, screen):
        """Draw the control settings menu"""
        screen.fill(MENU_BG)
        
        # Title
        title_text = "CONTROL SETTINGS"
        title_surface = self.font_large.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2, 150)
        screen.blit(title_surface, title_rect)
        
        # Instructions
        instruction_text = "Choose your preferred control method:"
        instruction_surface = self.font_medium.render(instruction_text, True, LIGHT_GRAY)
        instruction_rect = instruction_surface.get_rect()
        instruction_rect.center = (SCREEN_WIDTH // 2, 220)
        screen.blit(instruction_surface, instruction_rect)
        
        # Current selection indicator
        current_mode = self.settings_manager.get_control_mode()
        
        # Draw buttons with selection indicator
        self.draw_control_button(screen, self.keyboard_button, current_mode == CONTROL_MODE_KEYBOARD)
        self.draw_control_button(screen, self.mouse_button, current_mode == CONTROL_MODE_MOUSE)
        
        # Control descriptions
        descriptions = {
            CONTROL_MODE_KEYBOARD: [
                "• Use LEFT and RIGHT arrow keys to move paddle",
                "• Precise digital control",
                "• Good for consistent movement",
                "• Mouse input disabled during gameplay"
            ],
            CONTROL_MODE_MOUSE: [
                "• Move mouse to control paddle position", 
                "• Smooth analog control",
                "• Natural and intuitive",
                "• Arrow keys disabled during gameplay",
                "• ESC key always works for pause"
            ]
        }
        
        # Show description for current mode
        desc_y = 450
        mode_descriptions = descriptions.get(current_mode, [])
        for i, desc in enumerate(mode_descriptions):
            color = WHITE if not desc.startswith("•") else LIGHT_GRAY
            desc_surface = self.font_small.render(desc, True, color)
            desc_rect = desc_surface.get_rect()
            desc_rect.centerx = SCREEN_WIDTH // 2
            desc_rect.y = desc_y + i * 25
            screen.blit(desc_surface, desc_rect)
        
        # Back button
        self.back_button.draw(screen)
    
    def draw_control_button(self, screen, button: Button, is_selected: bool):
        """Draw a control button with selection indicator"""
        # Choose colors based on selection and hover state
        if is_selected:
            bg_color = (100, 150, 100) if not button.hovered else (120, 170, 120)
            border_color = (0, 255, 0)
            border_width = 3
        else:
            bg_color = MENU_BUTTON_HOVER if button.hovered else MENU_BUTTON
            border_color = WHITE
            border_width = 2
        
        # Draw button background
        pygame.draw.rect(screen, bg_color, button.rect)
        pygame.draw.rect(screen, border_color, button.rect, border_width)
        
        # Draw button text
        text_color = WHITE
        text_surface = button.font.render(button.text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = button.rect.center
        screen.blit(text_surface, text_rect)
        
        # Draw selection indicator
        if is_selected:
            indicator_text = "✓ SELECTED"
            indicator_surface = self.font_small.render(indicator_text, True, (0, 255, 0))
            indicator_rect = indicator_surface.get_rect()
            indicator_rect.centerx = button.rect.centerx
            indicator_rect.y = button.rect.bottom + 10
            screen.blit(indicator_surface, indicator_rect)

class SettingsMenu:
    def __init__(self, settings_manager: SettingsManager):
        pygame.font.init()
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.settings_manager = settings_manager
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_spacing = 70
        start_y = SCREEN_HEIGHT // 2 - 50
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.controls_button = Button(center_x, start_y, button_width, button_height, "Controls", self.font_medium)
        self.help_button = Button(center_x, start_y + button_spacing, button_width, button_height, "Help", self.font_medium)
        self.back_button = Button(50, SCREEN_HEIGHT - 100, 100, 40, "Back", self.font_small)
    
    def update(self, mouse_pos: Tuple[int, int], mouse_clicked: bool) -> Optional[str]:
        """Update settings menu"""
        self.controls_button.update(mouse_pos, mouse_clicked)
        self.help_button.update(mouse_pos, mouse_clicked)
        self.back_button.update(mouse_pos, mouse_clicked)
        
        if self.controls_button.clicked:
            return "control_settings"
        elif self.help_button.clicked:
            return "help"
        elif self.back_button.clicked:
            return "main_menu"
        
        return None
    
    def draw(self, screen):
        """Draw the settings menu"""
        screen.fill(MENU_BG)
        
        # Title
        title_text = "SETTINGS"
        title_surface = self.font_large.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2, 150)
        screen.blit(title_surface, title_rect)
        
        # Current control mode display
        current_mode = self.settings_manager.get_control_mode()
        mode_display = current_mode.title()
        mode_text = f"Current Control Mode: {mode_display}"
        mode_surface = self.font_small.render(mode_text, True, LIGHT_GRAY)
        mode_rect = mode_surface.get_rect()
        mode_rect.center = (SCREEN_WIDTH // 2, 220)
        screen.blit(mode_surface, mode_rect)
        
        # Draw buttons
        self.controls_button.draw(screen)
        self.help_button.draw(screen)
        self.back_button.draw(screen)
