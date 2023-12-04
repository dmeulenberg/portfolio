import pygame
from pygame.sprite import Sprite

class Ship:
    """A class to manage the ship"""

    def __init__(self, ss_game):
        """Initialize the ship and set its starting position."""
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.screen_rect = ss_game.screen.get_rect()

        # load the ship image and get its rect
        self.image = pygame.image.load('images/rocket_horiz.png').convert_alpha()
        self.image_flag = 'ship'
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Start each ship at the left center of the screen
        self.rect.midleft = self.screen_rect.midleft

        # Store a decimal value for the ship's vertical position
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on the movement flag"""
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        # Update rect object from self.y
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Return the ship to the starting position left center."""
        self.image = pygame.image.load('images/rocket_horiz.png').convert_alpha()
        self.image_flag = 'ship'
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)


class MiniShip(Sprite):
    """A class to manage 'ships left' graphics on screen."""

    def __init__(self, ss_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.screen_rect = ss_game.screen.get_rect()

        # load the ship image and get its rect
        mini_image = pygame.image.load('images/rocket_horiz.png').convert_alpha()
        self.image = pygame.transform.scale(mini_image, (100, 37))

        self.rect = self.image.get_rect()
        # self.mask = pygame.mask.from_surface(self.image)

        # Start each ship at the left center of the screen
        self.rect.midleft = self.screen_rect.midleft