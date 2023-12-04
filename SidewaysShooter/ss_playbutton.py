import pygame

class PlayButton:
    """Load the image of the play button and place it on the screen"""

    def __init__(self, ss_game):
        """Initialize button attributes."""
        self.screen = ss_game.screen
        self.screen_rect = self.screen.get_rect()

        self.play_button = pygame.image.load('images/playbutton.png').convert_alpha()
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.centerx = self.screen_rect.centerx
        self.play_button_rect.bottom = self.screen_rect.bottom - 125

    def draw_playbutton(self):
        self.screen.blit(self.play_button, self.play_button_rect)
