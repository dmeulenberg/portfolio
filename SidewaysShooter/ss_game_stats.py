import json

class GameStats:
    """Track game statistics for Sideways Shooter."""

    def __init__(self, ss_game):
        """Initialize stats."""

        self.settings = ss_game.settings

        # High score should never be reset.
        filename = 'ss_high_score.txt'
        try:
            with open(filename) as f:
                self.high_score = json.load(f)
                print(f"Imported all-time high score: {self.high_score}")
        except FileNotFoundError:
            self.high_score = 0

        self.reset_stats()

        # Start Sideways Shooter in an inactive state
        self.game_active = False
        self.game_over = False  # to say if title or "GAME OVER" appears
        self.show_playbutton = True

    def reset_stats(self):
        """Initialize stats that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        print(f"Level: {self.level}")

    def write_high_score_to_file(self):
        filename = 'ss_high_score.txt'
        try:
            with open(filename, 'w') as f:
                json.dump(self.high_score, f)
                print(f"New high Score: {self.high_score}")
        except:
            print("Could not open High Score file.")
