import pygame.font
from pygame.sprite import Group
from ss_ship import MiniShip

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, tp_game):
        """Initialize scoring attributes."""
        self.tp_game = tp_game
        self.screen = tp_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = tp_game.settings
        self.target = tp_game.target
#        self.stats = ss_game.stats

        # Font settings for scoring info.
        self.text_color = (255, 255, 0)
        self.label_color = (255, 0, 0)
        self.font = pygame.font.SysFont('Comic Sans', 24, False)
        self.label_font = pygame.font.SysFont('Comic Sans', 24, False)

        # Prepare an initial score image
        self.prep_scoreboard()

    # def check_high_score(self):
    #     """Check to see if there is a new high score."""
    #     if self.stats.score > self.stats.high_score:
    #         self.stats.high_score = self.stats.score
    #         self.prep_high_score



    def prep_scoreboard(self):
        """Prep all elements of the scoreboard."""
        self.prep_misses()
        self.prep_target_hits()
        # self.prep_high_score()
        # self.prep_level()
        # self.prep_ships()

    def show_scoreboard(self):
        """Show all elements of the scoreboard."""
        self.show_target_hits()
        self.show_misses()
        # self.show_high_score()
        # self.show_level()
        # self.ships.draw(self.screen)



    def prep_misses(self):
        """Turn the fleet size into a rendered image."""
        misses_allowed_str = f" / {str(self.settings.misses_allowed)}"
        self.misses_allowed_img = self.label_font.render(misses_allowed_str, True,
            self.label_color, self.settings.bg_color)

        misses_str = str(self.settings.misses)
        self.misses_img = self.font.render(misses_str, True,
            self.text_color, self.settings.bg_color)

        misses_label = "Misses: "
        self.misses_label_image = self.label_font.render(
            misses_label, True, self.label_color, self.settings.bg_color)

        # Display Misses 0 / 15
        self.misses_allowed_rect = self.misses_allowed_img.get_rect()
        self.misses_allowed_rect.right = self.screen_rect.right - 20
        self.misses_allowed_rect.top = 20

        self.misses_rect = self.misses_img.get_rect()
        self.misses_rect.right = self.misses_allowed_rect.left
        self.misses_rect.top = self.misses_allowed_rect.top

        self.misses_label_rect = self.misses_label_image.get_rect()
        self.misses_label_rect.right = self.misses_rect.left
        self.misses_label_rect.top = self.misses_allowed_rect.top

    def show_misses(self):
        """Draw misses to the screen."""
        self.screen.blit(self.misses_allowed_img, self.misses_allowed_rect)
        self.screen.blit(self.misses_img, self.misses_rect)
        self.screen.blit(self.misses_label_image, self.misses_label_rect)


    def prep_target_hits(self):
        """Turn the target_hits into a rendered image."""
        target_hits_str = str(self.target.target_hits)
        target_hits_label_str = "Target hits: "
        self.target_hits_image = self.font.render(target_hits_str, True, 
            self.text_color, self.settings.bg_color)
        self.target_hits_label = self.label_font.render(target_hits_label_str, True, 
            self.label_color, self.settings.bg_color)

        # Display the target_hits in top right corner
        self.target_hits_label_rect = self.target_hits_label.get_rect()
        self.target_hits_label_rect.left = self.screen_rect.left + 20
        self.target_hits_label_rect.top = 20


        self.target_hits_rect = self.target_hits_image.get_rect()
        self.target_hits_rect.left = self.target_hits_label_rect.right
        self.target_hits_rect.top = 20



    def show_target_hits(self):
        """Draw target_hits to the screen."""
        self.screen.blit(self.target_hits_image, self.target_hits_rect)
        self.screen.blit(self.target_hits_label, self.target_hits_label_rect)




    # def prep_high_score(self):
    #     """Turn the score into a rendered image."""
    #     hi_score_str = str(self.stats.high_score)
    #     hi_score_label_str = "High score: "
    #     self.hi_score_image = self.font.render(hi_score_str, True, 
    #         self.text_color, self.settings.bg_color)
    #     self.hi_score_label = self.label_font.render(hi_score_label_str, True, 
    #         self.label_color, self.settings.bg_color)

    #     # Split center between label and hi score
    #     self.hi_score_rect = self.hi_score_image.get_rect()
    #     self.hi_score_rect.left = self.screen_rect.centerx 
    #     self.hi_score_rect.top = 20

    #     self.hi_score_label_rect = self.hi_score_label.get_rect()
    #     self.hi_score_label_rect.right = self.screen_rect.centerx 
    #     self.hi_score_label_rect.top = self.hi_score_rect.top

    # def show_high_score(self):
    #     """Draw score to the screen."""
    #     self.screen.blit(self.hi_score_image, self.hi_score_rect)
    #     self.screen.blit(self.hi_score_label, self.hi_score_label_rect)

    # def prep_level(self):
    #     """Turn the level into a rendered image."""
    #     level_str = str(self.stats.level)
    #     level_label_str = "Level: "
    #     self.level_image = self.font.render(level_str, True, 
    #         self.text_color, self.settings.bg_color)
    #     self.level_label = self.label_font.render(level_label_str, True, 
    #         self.label_color, self.settings.bg_color)

    #     # Display the level in top left corner -- even with score
    #     self.level_label_rect = self.level_label.get_rect()
    #     self.level_label_rect.left = 20 
    #     self.level_label_rect.top = self.score_rect.top

    #     self.level_rect = self.level_image.get_rect()
    #     self.level_rect.left = self.level_label_rect.right
    #     self.level_rect.top = self.level_label_rect.top

    # def show_level(self):
    #     """Draw score to the screen."""
    #     self.screen.blit(self.level_image, self.level_rect)
    #     self.screen.blit(self.level_label, self.level_label_rect)

    # def prep_ships(self):
    #     """Show how many ships are left."""
    #     self.ships = Group()
    #     for ship_number in range(self.stats.ships_left):
    #         ship = MiniShip(self.ss_game)
    #         ship.rect.x = 10 + ship_number * ship.rect.width
    #         ship.rect.y = 10
    #         self.ships.add(ship)