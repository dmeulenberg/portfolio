# EXERCISE 14-2   Target Practice
# Basing it on sideways shooter (early stage)

# EXERCISE 12-6   Sideways Shooter, page 253 (hard copy)

import sys

import pygame
import pygame.font

from pygame.sprite import Sprite
from time import sleep
from random import randint
from tp_scoreboard import Scoreboard
from tp_playbutton import PlayButton


class SidewaysShooter:
    """Overall class for Sideways Shooter exercise"""

    def __init__(self):
        """Initialize the game and create resources"""
        pygame.init()
        self.settings = Settings()



        self.screen = pygame.display.set_mode((1492,930))  #1870
        pygame.display.set_caption("Target Practice: Project 14-2")

        self._make_starfield()

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.target = Target(self)
        self.sb = Scoreboard(self)

        # Make the Play button
        self.play_button = PlayButton(self)

        self._make_title()
        self._make_you_win()
        self._make_you_lose()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.settings.game_active:
                self.ship.update()
                self.bullets.update()
                self.target.update()

                # Get rid of old bullets
                for bullet in self.bullets.copy():
                    if bullet.rect.right > 1920:
                        self.bullets.remove(bullet)
                        self.settings.misses += 1
                        print(f"Misses: {self.settings.misses}")
                        self.sb.prep_scoreboard()
                        if self.settings.misses >= self.settings.misses_allowed:
                            #self.settings.game_active = False
                            self.settings.you_lose_flag = True
                            self._show_you_lose()
                            self.sb.prep_scoreboard()
                            # Make the most recently redrawn screen visible
                            pygame.display.flip()
                            sleep(5)
                            self._game_over()
                            print("You lose!!!!!!")
                # print(len(self.bullets))

                self._check_target_bullet_collision()

            self._update_screen()

    def _update_screen(self):
        # Redraw the screen during each pass of the loop
        self.screen.fill(self.settings.bg_color)
        self._draw_starfield()

        self.ship.blitme()
        self.target.draw_target()

        self.sb.show_scoreboard()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()



        # if self.settings.game_over: # show "game over"
        #     self.play_button.draw_playbutton()
        #     if self.settings.you_win_flag:
        #         self._show_you_win()

        #     elif self.settings.you_lose_flag:
        #         self._show_you_lose()


        # Draw the Play button if the game is inactive. (Do this last!)
        if not self.settings.game_active:
            self._show_title()
            self.play_button.draw_playbutton()


            # Make mouse cursor visible
            pygame.mouse.set_visible(True)

        # Make the most recently redrawn screen visible
        pygame.display.flip()

    def _make_starfield(self):
        """Create a field of random stars"""
        self.stars = []
        number_of_stars = 100

        for star in range(number_of_stars):
            star_size_x = randint(2,4)
            star_size_y = randint(2,4)
            star_x = randint(0, self.screen.get_width())
            star_y = randint(0, self.screen.get_height())

            star_dict = {}
            star_dict['coord_x'] = star_x
            star_dict['coord_y'] = star_y
            star_dict['size_x'] = star_size_x
            star_dict['size_y'] = star_size_y

            self.stars.append(star_dict)

        # print(self.stars)
            
    def _draw_starfield(self):
        """Draw the stars to the screen"""
        for star in self.stars:
            self.rect = (star['coord_x'], star['coord_y'], 
                star['size_x'], star['size_y'])
            pygame.draw.rect(self.screen, (200, 200, 200), self.rect)

    def _make_title(self):
        """Load the title image and place it on the screen"""
        self.screen_rect = self.screen.get_rect()
        self.title_img = pygame.image.load('images/target_practice.png').convert_alpha()
        self.title_img_rect = self.title_img.get_rect()
        self.title_img_rect.centerx = self.screen_rect.centerx
        self.title_img_rect.centery = self.screen_rect.centery - 100

    def _show_title(self):
        self.screen.blit(self.title_img, self.title_img_rect)

    def _make_you_lose(self):
        """Load the 'Game Over' image and place it on the screen"""
        self.screen_rect = self.screen.get_rect()
        self.you_lose_img = pygame.image.load('images/tp_you_lose.png').convert_alpha()
        self.you_lose_img_rect = self.you_lose_img.get_rect()
        #self.you_lose_img_rect.center = self.screen_rect.center
        self.you_lose_img_rect.centerx = self.screen_rect.centerx + 200
        self.you_lose_img_rect.centery = self.screen_rect.centery + 100

    def _show_you_lose(self):
        self.screen.blit(self.you_lose_img, self.you_lose_img_rect)

    def _make_you_win(self):
        """Load the "Level Up" image and place it on the screen"""
        self.screen_rect = self.screen.get_rect()
        self.you_win_img = pygame.image.load('images/tp_you_win.png').convert_alpha()
        self.you_win_img_rect = self.you_win_img.get_rect()
        self.you_win_img_rect.center = self.screen_rect.center

    def _show_you_win(self):
        self.screen.blit(self.you_win_img, self.you_win_img_rect)

    def _check_events(self):
        # Watch for keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down = True
                elif event.key == pygame.K_UP:
                    self.ship.moving_up = True
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()
                elif event.key == pygame.K_p and not self.settings.game_active:
                    self._start_game()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.ship.moving_down = False
                elif event.key == pygame.K_UP:
                    self.ship.moving_up = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_play_button(self, mouse_pos):
            """Start a new game when the player clicks the Play button."""
            button_clicked =  self.play_button.play_button_rect.collidepoint(mouse_pos)

            if button_clicked and not self.settings.game_active: # only recoginze button while inactive
                self._start_game()           

    def _check_target_bullet_collision(self):
        collision = pygame.sprite.spritecollideany(self.target, self.bullets)
        if collision:
            print(f"Target hit!!")
            #remove bullet so it doesn't register a hit for each pixel width of target
            self.bullets.remove(collision)

            # Make target smaller, faster, more red, and at a random distance from ship
            self.target.target_hits += 1
            self.target.target_speed  += 0.1
            self.target.height -= 50
            self.target.green_value -= 40
            self.sb.prep_scoreboard()

            self.target.target_x_coord = randint(746, 1392)
            if self.target.green_value < 0:
                self.target.target_color = (255, 0, 0)
            else:
                self.target.target_color = (255, self.target.green_value, 0)

            if self.target.height <= 0:
                self.settings.you_win_flag = True
                self._show_you_win()
                self.sb.prep_scoreboard()
                # Make the most recently redrawn screen visible
                pygame.display.flip()

                sleep(5)
                self._game_over()
                print("You WIN !!!!!!")


    def _start_game(self):
        """Start a new game."""
        self.screen_rect = self.screen.get_rect()
        #print(self.screen_rect)
        self.settings.game_active = True
        self.settings.misses = 0
        self.settings.target_hits = 0
        self.target.target_hits = 0
        self.sb.prep_scoreboard()
        self.target.height = self.settings.target_height
        self.target.target_speed = self.settings.target_speed
        self.bullets.empty()
        self.target.target_color = (255, 255, 0)
        self.target.green_value = self.settings.green_value
        self.target.target_x_coord = self.settings.target_x_coord
        self._make_starfield()

        # Create a new fleet and center the ship
        self.screen_rect = self.screen.get_rect()
        self.ship.rect.midleft = self.screen_rect.midleft

        # Hide mouse cursor
        pygame.mouse.set_visible(False)

    def _game_over(self):
        """Game over, dude, game over!!!!!"""
        # Get rid of any remaining aliens and bullets
        # self.aliens.empty()  # Leaving aliens and BOOM moving 'cause it's fun
        self.bullets.empty()
        #self.settings.game_over = True
        #self.settings.show_playbutton_flag = True


        self.settings.game_active = False

        pygame.mouse.set_visible(True)


# ***** begin classes here *****************


class Settings:
    """A class to store settings for game."""

    def __init__(self):
        """Initialize the game's settings"""

        # #Screen settings
        self.bg_color = (0, 0, 0)

        self.game_active = False
        self.game_over = False
        self.you_win_flag = False
        self.you_lose_flag = False
        self.show_playbutton_flag = False

        # Ship settings
        self.ship_speed = .11

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 1

        # Target settings
        self.target_speed = 0.5
        self.target_color = (255, 255, 0)
        self.green_value = 255
        self.target_height = 300
        self.target_width = 25
        self.target_hits = 0
        self.misses_allowed = 15  #15
        self.target_x_coord = 1392

        self.misses = 0


class Ship:
    """A class to manage the ship"""

    def __init__(self, ss_game):
        """Initialize the ship and set its starting position."""
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.screen_rect = ss_game.screen.get_rect()

        # load the ship image and get its rect
        self.image = pygame.image.load('images/rocket_horiz.png')
        self.rect = self.image.get_rect()

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


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ss_game):
        """Create a bullet object at the ship's current position"""
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet at rect (0,0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, 
            self.settings.bullet_height)
        self.rect.midright = ss_game.ship.rect.midright

        # Store the bullet's position as a decimal value.
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet across the screen"""
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class Target:
    """Make a rectangular target on the right side of the screen"""
    def __init__(self, ss_game):
        """Initialize target attributes."""
        self.settings = ss_game.settings
        self.screen = ss_game.screen
        self.screen_rect = self.screen.get_rect()


        # Set the dimensions and properties of the target.
        self.width = self.settings.target_width
        self.height = self.settings.target_height
        self.target_color = self.settings.target_color
        self.target_hits = self.settings.target_hits
        self.target_speed = self.settings.target_speed
        self.green_value = self.settings.green_value
        self.target_x_coord = self.settings.target_x_coord

        # Build the target's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # self.rect.x = randint((self.screen_rect.x/2), (self.screen_rect.x - 100)
        self.rect.x = self.screen_rect.right - 100  # move off right side a bit
        self.rect.y = self.screen_rect.centery


        # Store a decimal for the target's Y value
        self.y = float(self.rect.y)
        print(f"Initial target Y coordinate = {self.y}")

        # Movement direction start with random to get 1 or -1
        new_v_direct = randint(-1, 1)
        while new_v_direct == 0: # don't allow for 0 as a result
                new_v_direct= randint(-1, 1)
        self.vertical_direction = new_v_direct         

    def update(self):
        self.y += (self.vertical_direction * self.target_speed)
        if self.y <= 0:  # reaches top of screen
            self.vertical_direction = 1

        if self.y >= self.screen_rect.bottom - self.height:  # reaches bottom of screen
            self.vertical_direction = -1

        self.rect.y = self.y


    def draw_target(self):
        # Draw a target
        self.rect.x = self.target_x_coord
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height)
        self.screen.fill(self.target_color, self.rect)






class Button:
    def __init__(self, ss_game, msg):
        """Initialize button attributes."""
        self.screen = ss_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (255, 0, 0)
        self.outline_color = (255, 255, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.outline_rect = pygame.Rect(0, 0, self.width+8, self.height+8)
        self.outline_rect.center = self.screen_rect.center
        self.rect = pygame.Rect(8, 8, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message has to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color,
            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw a blank button and then draw the message
        self.screen.fill(self.outline_color, self.outline_rect)
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)



# ********** End of Classes *******************

if __name__ == '__main__':
    # Make game instance and run game
    ss = SidewaysShooter()
    ss.run_game()