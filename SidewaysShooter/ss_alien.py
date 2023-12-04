import pygame
from pygame.sprite import Sprite
from random import randint

class Alien(Sprite):
    """A class to represent a single alien"""

    def __init__(self, ss_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.screen_rect = ss_game.screen.get_rect()

        # Counter to adjust how long "boom" stays visible when alien is shot
        self.explosion_counter = 0

        # Load the alien and get its rect    
        self.image = pygame.image.load('images/ufo_horiz.png').convert_alpha()
        self.image_flag = 'alien'
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Start each alien at the right side with a random Y coordinate
        self.rect.x = self.screen_rect.width
        self.rect.y = randint(0, self.screen_rect.height)

        # Store the alien's exact position as decimals
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # print(f"New alien position: {self.x}, {self.y}")

        # Set a random vertical direction
        self.vertical_direction = randint(-1,1)
        # print(f"self.vertical_direction = {self.vertical_direction}")

        # Set initial horizongal direction = right to left (-1) 
        self.horizontal_direction = -1

    def update(self):
        """Move the alien on the screen"""
        # if the alien has exploded, don't move the "boom"
        # increase the counter to time how long the explosion stays visible
        if self.explosion_counter > 0:
            self.explosion_counter += 1
        else:    # Alien has not exploded
            # Move the alien

            # Check for left edge
                # If reach left edge, randomly move right (1) or up/down (0)
                # unless ship is moving horizonally only, then move right (don't park)

            if self.x < 0 and self.horizontal_direction != 0: # reached left edge, not parked there 
                
                if self.vertical_direction == 0: # ships moving horizontally only
                    self.horizontal_direction = 1  # bounce back right
                    new_v_direct = randint(-1, 1)
                    while new_v_direct == 0: # don't allow for 0 as a result
                        new_v_direct= randint(-1, 1)
                    self.vertical_direction = new_v_direct            
                else:   # don't "park" ships moving horizonally only
                    self.horizontal_direction = randint(0,1)
                    

            # If heading right (away from ship), change to left at 2/3rds way across
            if self.horizontal_direction == 1:
                if self.x >= (self.screen_rect.right*2/3): #don't care about width of alien
                    # If reach right boundary set above, move left
                    self.horizontal_direction = -1

            # Check for top and bottom, if so, change direction
            if self.y <= 0:
                self.vertical_direction = 1
                if self.horizontal_direction == 0:  # moving down at left edge, bounce back right
                    self.horizontal_direction = 1
            if self.y >= self.screen_rect.bottom - 126: # alien height=126 pixels
                self.vertical_direction = -1
                if self.horizontal_direction == 0:  # moving up at left edge, bounce back right
                    self.horizontal_direction = 1

            # Make changes
            self.y += (self.vertical_direction * self.settings.alien_vert_speed) # + (float(randint(0, 10))/100)
            self.x += (self.horizontal_direction * self.settings.alien_horiz_speed) # + (float(randint(0, 10))/100)

            # Make aliens that don't go up and down move faster horizontally
            if self.vertical_direction == 0: 
                self.x += self.settings.alien_horiz_speed * 4 * self.horizontal_direction
            else:
                self.x += self.settings.alien_horiz_speed * self.horizontal_direction



            # Update the rect positions
            self.rect.y = self.y
            self.rect.x = self.x