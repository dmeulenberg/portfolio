import pygame

class Settings:
    """A class to store settings for game."""

    def __init__(self):
        """Initialize the game's static settings"""

        self.game_active = True
        self.show_message_flag = False
        self.game_over = False

        # Screen settings
        self.screen_width = 768   
            # 1440 x 2960 is standard Samsung Gal 8/9
        self.screen_height = 1024   
            # Viewport settings are smaller (768x1024).
        self.bg_color = (255, 255, 255)

        # Color settings for letters
        self.color_lt_gray = (212, 212, 212)
        self.color_dk_gray = (124, 124, 124)
        self.color_yellow = (201, 180, 87)
        self.color_green = (107, 170, 100)
        # self.color_green = (52, 58, 235)   # Experimented with blue at Justin's request.
        self.font_white = (255, 255, 255)
        self.font_black = (0, 0, 0)

        # Font size settings
        self.top_sq_font_size = 40
        self.key_sq_font_size = 24

        # Size settings for rectangles
        self.top_square_size = 80
        self.top_square_spacing = 5
        self.top_margin = 50

        self.key_rect_width = 50
        self.key_rect_height = 90
        self.key_rect_spacing = 7
        self.large_key_rect_width = 80
        self.top_kb_row_y = 0  #just a placeholder, value will be assigned

        # Word settings
        self.answer_list = []
        self.allowed_guesses = []
        self.key_row_1 = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
        self.key_row_2 = ['A', 'S', 'D' ,'F' ,'G', 'H', 'J', 'K', 'L']
        self.key_row_3 = ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BKSP']

        self.kb_row_1 = []
        self.kb_row_2 = []
        self.kb_row_3 = []



        self.initialize_dynamic_settings()



    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""

        # Word settings
        self.answer_word = ''
        self.top_grid = []

        # Keyboard settings
        self.kb_list = []


        # Guess settings
        self.guess_column_number = 0
        self.guess_row_number = 0 

        self.current_guess = ''
        self.guess_1 = ''
        self.guess_2 = ''
        self.guess_3 = ''
        self.guess_4 = ''
        self.guess_5 = ''
        self.guess_6 = ''



