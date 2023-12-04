import pygame.font
from pygame.sprite import Group
from ss_ship import MiniShip

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ss_game):
        """Initialize scoring attributes."""
        self.ss_game = ss_game
        self.screen = ss_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ss_game.settings
        self.stats = ss_game.stats

        # Font settings for scoring info.
        self.text_color = (255, 255, 0)
        self.label_color = (255, 0, 0)
        self.font = pygame.font.SysFont('Comic Sans', 24, False)
        self.label_font = pygame.font.SysFont('Comic Sans', 24, False)

        # Prepare an initial score image
        self.prep_scoreboard()

    def check_high_score(self):
        """Check to see if there is a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score



    def prep_scoreboard(self):
        """Prep all elements of the scoreboard."""
        self.prep_aliens_destroyed()
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def show_scoreboard(self):
        """Show all elements of the scoreboard."""
        self.show_score()
        self.show_aliens_destroyed()
        self.show_high_score()
        self.show_level()
        self.ships.draw(self.screen)



    def prep_aliens_destroyed(self):
        """Turn the fleet size into a rendered image."""
        fleet_sz_str = f" / {str(self.settings.alien_fleet_size)}"
        self.fleet_sz_img = self.label_font.render(fleet_sz_str, True,
            self.label_color, self.settings.bg_color)

        aliens_destroyed_str = str(self.settings.aliens_destroyed)
        self.aliens_destroyed_img = self.font.render(aliens_destroyed_str, True,
            self.text_color, self.settings.bg_color)

        aliens_destroyed_label = "Aliens destroyed: "
        self.aliens_destroyed_label_image = self.label_font.render(
            aliens_destroyed_label, True, self.label_color, self.settings.bg_color)

        # Display Aliens Destroyed: 0 / 5
        self.fleet_sz_rect = self.fleet_sz_img.get_rect()
        self.fleet_sz_rect.right = self.screen_rect.right - 20
        self.fleet_sz_rect.top = 20

        self.aliens_destroyed_rect = self.aliens_destroyed_img.get_rect()
        self.aliens_destroyed_rect.right = self.fleet_sz_rect.left
        self.aliens_destroyed_rect.top = self.fleet_sz_rect.top

        self.aliens_destroyed_label_rect = self.aliens_destroyed_label_image.get_rect()
        self.aliens_destroyed_label_rect.right = self.aliens_destroyed_rect.left
        self.aliens_destroyed_label_rect.top = self.fleet_sz_rect.top

    def show_aliens_destroyed(self):
        """Draw score to the screen."""
        self.screen.blit(self.fleet_sz_img, self.fleet_sz_rect)
        self.screen.blit(self.aliens_destroyed_img, self.aliens_destroyed_rect)
        self.screen.blit(self.aliens_destroyed_label_image, self.aliens_destroyed_label_rect)


    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = str(self.stats.score)
        score_label_str = "Score: "
        self.score_image = self.font.render(score_str, True, 
            self.text_color, self.settings.bg_color)
        self.score_label = self.label_font.render(score_label_str, True, 
            self.label_color, self.settings.bg_color)

        # Display the score in top right corner
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.fleet_sz_rect.bottom + 10

        self.score_label_rect = self.score_label.get_rect()
        self.score_label_rect.right = self.score_rect.left 
        self.score_label_rect.top = self.score_rect.top

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.score_label, self.score_label_rect)




    def prep_high_score(self):
        """Turn the score into a rendered image."""
        hi_score_str = str(self.stats.high_score)
        hi_score_label_str = "High score: "
        self.hi_score_image = self.font.render(hi_score_str, True, 
            self.text_color, self.settings.bg_color)
        self.hi_score_label = self.label_font.render(hi_score_label_str, True, 
            self.label_color, self.settings.bg_color)

        # Split center between label and hi score
        self.hi_score_rect = self.hi_score_image.get_rect()
        self.hi_score_rect.left = self.screen_rect.centerx 
        self.hi_score_rect.top = 20

        self.hi_score_label_rect = self.hi_score_label.get_rect()
        self.hi_score_label_rect.right = self.screen_rect.centerx 
        self.hi_score_label_rect.top = self.hi_score_rect.top

    def show_high_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.hi_score_image, self.hi_score_rect)
        self.screen.blit(self.hi_score_label, self.hi_score_label_rect)

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        level_label_str = "Level: "
        self.level_image = self.font.render(level_str, True, 
            self.text_color, self.settings.bg_color)
        self.level_label = self.label_font.render(level_label_str, True, 
            self.label_color, self.settings.bg_color)

        # Display the level in top left corner -- even with score
        self.level_label_rect = self.level_label.get_rect()
        self.level_label_rect.left = 20 
        self.level_label_rect.top = self.score_rect.top

        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.level_label_rect.right
        self.level_rect.top = self.level_label_rect.top

    def show_level(self):
        """Draw score to the screen."""
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.level_label, self.level_label_rect)

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = MiniShip(self.ss_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)