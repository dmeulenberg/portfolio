import pygame

class Settings:
    """A class to store settings for game."""

    def __init__(self):
        """Initialize the game's static settings"""

        # Screen settings
        self.screen_width = 1870   # 1870
        self.screen_height = 930
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 10

        # Alien settings
        # moved to dynamic settings

        # How quickly the game speeds up
        self.speedup_scale = 1.2


        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1
        self.bullet_speed = 1.0
        self.alien_fleet_size = 10           # 10
        self.alien_horiz_speed = 0.15
        self.alien_vert_speed = 0.5
        self.aliens_destroyed = 0
        self.aliens_created = 0

        # Plan for pausing while active between levels
        self.levelup_counter = 0
        self.levelup_counter_max = 1500
        self.levelup_flag = False

        # Scoring
        self.alien_points = 100

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_horiz_speed *= self.speedup_scale
        self.alien_vert_speed *= self.speedup_scale
        self.alien_fleet_size += 5
        self.aliens_created = 0
        self.aliens_destroyed = 0
        self.alien_points += 20
