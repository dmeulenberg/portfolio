# EXERCISE 13-5   Sideways Shooter, Part 2 (page 272 hard copy)

# COPIED FROM EXERCISE 12-6   Sideways Shooter, page 253 (hard copy)

import sys

import pygame

from pygame.sprite import Sprite
from time import sleep
from random import randint

from ss_settings import Settings
from ss_game_stats import GameStats
from ss_ship import Ship
from ss_bullet import Bullet
from ss_alien import Alien
from ss_playbutton import PlayButton
from ss_scoreboard import Scoreboard


class SidewaysShooter:
    """Overall class for Sideways Shooter exercise"""

    def __init__(self):
        """Initialize the game and create resources"""
        pygame.init()
        self.settings = Settings()
        self.stats = GameStats(self)

        self.screen = pygame.display.set_mode((self.settings.screen_width,
            self.settings.screen_height))
        pygame.display.set_caption("Sideways Shooter")

        self._make_starfield()
        self._make_title()
        self._make_game_over()
        self._make_level_up()
        self.fleet_full = False

        # Make a Play button
        self.play_button = PlayButton(self)

        # Make a Scoreboard
        self.sb = Scoreboard(self)

        # Create a ship, aliens, and bullets groups
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        #self._create_alien()


    def run_game(self):
        """Start the main loop for the game"""

        # Set a counter for the game to time next alien
        self.game_counter = 0  

        self.levelup_counter = 0

        while True:
            # Main loop for game
            self._check_events()

            # If game is in an active state
            if self.stats.game_active:
                self.game_counter += 1
                # print(self.game_counter)
                self._update_aliens()

            if not self.stats.game_over:
                self.ship.update()
                self._update_bullets()
                
            if self.settings.levelup_flag:
                # print(f"levelup_counter = {self.levelup_counter}")
                self.levelup_counter += 1

                if self.levelup_counter > self.settings.levelup_counter_max:
                    # print("TEST 2")
                    self._level_up_part_2()

            self._update_screen()

    def _update_screen(self):
        # Redraw the screen during each pass of the loop
        self.screen.fill(self.settings.bg_color)
        self._draw_starfield()

        if not self.stats.game_active: # game is not active at startup
            self._show_title()
            self.play_button.draw_playbutton()

        else:   # draw game elements if game active
            self.ship.blitme()

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            if self.stats.game_over: # show "game over"
                self._show_game_over()

            if self.settings.levelup_flag: # show "level up"
                self._show_level_up()

            self.aliens.update()
            self.aliens.draw(self.screen)

            self.sb.show_scoreboard()

            if self.stats.show_playbutton: # show button flag
                # self.screen.blit(self.play_button.play_button, self.play_button.play_button_rect)
                self.play_button.draw_playbutton()
        
        # Make the most recently redrawn screen visible
        pygame.display.flip()

    def _check_events(self):
        # Watch for keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.write_high_score_to_file()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.stats.write_high_score_to_file()
                    sys.exit()
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down = True
                elif event.key == pygame.K_UP:
                    self.ship.moving_up = True
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()
                elif event.key == pygame.K_p:
                    self._start_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.ship.moving_down = False
                elif event.key == pygame.K_UP:
                    self.ship.moving_up = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.play_button_rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

        if button_clicked and self.stats.game_over:
            self._start_game()

    def _start_game(self):
        #reset the game stats
        self.stats.reset_stats()
        self.stats.game_active = True
        self.stats.game_over = False
        self.stats.show_playbutton = False
        self.settings.initialize_dynamic_settings()
        self.fleet_full = False
#        self.settings.aliens_created = 0
        self.sb.prep_scoreboard()


        # Get rid of remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # create a new alien and recenter ship
        self._create_alien()
        self.ship.center_ship()


        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

# ******* VISUAL HELPER METHODS (stars, titles, buttons) ********        

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
        self.title_img = pygame.image.load('images/ss_title.png').convert_alpha()
        self.title_img_rect = self.title_img.get_rect()
        self.title_img_rect.centerx = self.screen_rect.centerx
        self.title_img_rect.centery = self.screen_rect.centery - 100

    def _show_title(self):
        self.screen.blit(self.title_img, self.title_img_rect)

    def _make_game_over(self):
        """Load the 'Game Over' image and place it on the screen"""
        self.screen_rect = self.screen.get_rect()
        self.gameover_img = pygame.image.load('images/game_over.png').convert_alpha()
        self.gameover_img_rect = self.gameover_img.get_rect()
        self.gameover_img_rect.centerx = self.screen_rect.centerx
        self.gameover_img_rect.centery = self.screen_rect.centery - 100

    def _show_game_over(self):
        self.screen.blit(self.gameover_img, self.gameover_img_rect)

    def _make_level_up(self):
        """Load the "Level Up" image and place it on the screen"""
        self.screen_rect = self.screen.get_rect()
        self.levelup_img = pygame.image.load('images/level_up.png').convert_alpha()
        self.levelup_img_rect = self.levelup_img.get_rect()
        self.levelup_img_rect.center = self.screen_rect.center

    def _show_level_up(self):
        self.screen.blit(self.levelup_img, self.levelup_img_rect)


# ******** ACTION HELPER METHODS (bullets, aliens, collisions) ********


    def _create_alien(self):
        """Create an alien, set random interval for next alien"""
        if self.settings.aliens_created < self.settings.alien_fleet_size:
            # Make an alien
            alien = Alien(self)
            self.aliens.add(alien)
            self.next_alien = randint(800, 1200)
            self.settings.aliens_created += 1
            #print(f"aliens_created += 1 = {self.settings.aliens_created}, len(self.aliens)={len(self.aliens)}")
        elif self.settings.aliens_created == self.settings.alien_fleet_size:
            self.fleet_full = True
            #print("All Aliens created for this level.")
        

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet position
        self.bullets.update()

        # Get rid of old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.right > 1920:
                self.bullets.remove(bullet)

        # Check for bullets that have hit aliens
        self._check_alien_bullet_collisions()


    def _update_aliens(self):
        """Update position of aliens, create new aliens, check collisions"""
        self.aliens.update()

        # Create new alien at random intervals
        if self.game_counter >= self.next_alien and not self.stats.game_over:
            self._create_alien()
            self.game_counter = 0

        # Check for aliens hitting the ship
        self._check_ship_alien_collisions()


    def _check_alien_bullet_collisions(self):
        # Check for alien/bullet collisions
        # If so, get rid of bullet, keep alien but replace with "boom" graphic
        collisions = pygame.sprite.groupcollide(
            self.aliens, self.bullets, False, True)

        if collisions:
            # Replace alien image with "boom" image, start explosion counter
            for alien in collisions:
                alien.explosion_counter = 1
                if alien.image_flag == 'alien':
                    self.settings.aliens_destroyed += 1
                    self.stats.score += self.settings.alien_points
                alien.image = pygame.image.load('images/boom_sm.png').convert_alpha()
                alien.image_flag = 'boom'
                self.sb.prep_scoreboard()
                self.sb.check_high_score()

        # Remove alien from group after explosion has shown for X cycles
        for alien in self.aliens:
            if alien.explosion_counter > 300:  # How long explosion will show
                self.aliens.remove(alien)
                # print(f"Alien destroyed!--aliens_destroyed = {self.settings.aliens_destroyed}, len(self.aliens) = {len(self.aliens)}")

        if self.fleet_full and not self.aliens: # all aliens created, all destroyed
            self._level_up()


    def _check_ship_alien_collisions(self):
        """Check for aliens hitting the ship"""
        if not self.stats.game_over:
            for alien in self.aliens:
                ship_collision = pygame.sprite.collide_mask(self.ship, alien)

                if ship_collision:
                    print(f"\nShip hit!!!! {ship_collision}")

                    # Replace alien sprite with 'boom' image.
                    if alien.image_flag == 'alien':
                        alien.image = pygame.image.load('images/boom_sm.png').convert_alpha()
                        alien.image_flag = 'boom'
                        self.settings.aliens_destroyed += 1
                        self.sb.prep_scoreboard()
                        # self.aliens.remove(alien)


                    # Replace ship with 'boom' image and update screen.
                    if self.ship.image_flag == 'ship':
                        #ship_rect = self.ship.rect
                        # print(f" Ship collision ship_rect = {self.ship.rect}")
                        #boom_rect_y = ship_rect.centery
                        self.ship.image = pygame.image.load('images/boom_lg.png').convert_alpha()
                        #self.ship.rect.centery = boom_rect_y
                        self.ship.image_flag = 'boom'

                    self._update_screen()

                    # Pause.
                    sleep(3)

                    self._ship_hit()

                    # self.aliens.remove(alien)
                    # print(f"\nship/alien collision!--aliens_destroyed = {self.settings.aliens_destroyed}, aliens_created={self.settings.aliens_created}, qlen(self.aliens) = {len(self.aliens)}")



                    # Last alien in level destroyed by hitting ship
                    if not self.stats.ships_left - 1 <= 0: # If not last ship left
                        #print(f"TEST 1: self.stats.ships_left = {self.stats.ships_left} - 1 <= 0")
                        #print(f"TEST 1: Fleet full {self.fleet_full}")
                        #print(f"TEST 1: len(self.aliens) {len(self.aliens)}")
                        if self.fleet_full and not self.aliens:
                            self._level_up()

                    break


    def _ship_hit(self):
        """Respond if a ship is hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1
            print(f"Ships remaining: {self.stats.ships_left}\n")
            self.sb.prep_scoreboard()

            aliens_alive = len(self.aliens)  # reset aliens_created
            if aliens_alive > 0:
                self.settings.fleet_full = False
                # print(f"\naliens_alive = {aliens_alive}, aliens_created = {self.settings.aliens_created}")
                self.settings.aliens_created = self.settings.aliens_destroyed

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new alien and recenter the ship
            self._create_alien()
            self.ship.center_ship()

            self._update_screen()
        else:
            self._game_over()

    def _level_up(self):
        """Show the level up card and wait for a bit."""
        self._show_level_up()
        pygame.display.flip()
        self.settings.levelup_flag = True

    def _level_up_part_2(self):
        """Reset and start the new level."""
        self.settings.increase_speed()
        self.bullets.empty()
        self.stats.level += 1
        self.levelup_counter = 0
        self.settings.levelup_flag = False
        print(f"\nLEVEL UP!!!  Level: {self.stats.level}")
        self.fleet_full = False
        self.sb.prep_scoreboard()
        #sleep(2)


    def _game_over(self):
        """Game over, dude, game over!!!!!"""
        # Get rid of any remaining aliens and bullets
        # self.aliens.empty()  # Leaving aliens and BOOM moving 'cause it's fun
        self.bullets.empty()
        self.stats.game_over = True
        self.stats.show_playbutton = True
        self.settings.alien_horiz_speed = 0.05
        self.settings.alien_vert_speed = 0.25

        #self.stats.game_active = False

        pygame.mouse.set_visible(True)
        
        print(f"\n\n\n**************************")
        print(f"**************************")
        print(f"*****                *****")
        print(f"*****   GAME OVER !! *****")
        print(f"*****                *****")
        print(f"**************************")
        print(f"**************************")



# ********** MAIN INSTANCE OF GAME **********

if __name__ == '__main__':
    # Make game instance and run game
    ss = SidewaysShooter()
    ss.run_game()