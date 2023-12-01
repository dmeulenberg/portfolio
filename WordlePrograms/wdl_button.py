import pygame.font
from time import sleep
#from pygame.sprite import Sprite

# from wdl_settings import Settings

class TopSquare():
    """Class to create answer squares in the top 5x6 grid."""

    def __init__(self, wdl_game, row, column, value, status, x_coord, y_coord):
        """Initialize Top Square attributes."""
        self.settings = wdl_game.settings
        self.screen = wdl_game.screen
        self.screen_rect = self.screen.get_rect()
        self.row = row
        self.column = column
        self.value = value
        self.status = status
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.new_status = ''

        # Set the dimensions and properties of the square.
        self.width, self.height = self.settings.top_square_size, self.settings.top_square_size

        if self.status == 'empty':
            self.button_color = self.settings.color_lt_gray
            self.text_color = self.settings.bg_color
        elif self.status == 'guess':
            self.button_color = self.settings.color_lt_gray
            self.text_color = self.settings.font_black
        elif self.status == 'wrong':
            self.button_color = self.settings.color_dk_gray
            self.text_color = self.settings.font_white
        elif self.status == 'correct_in_spot':
            self.button_color = self.settings.color_green
            self.text_color = self.settings.font_white
        elif self.status == 'correct_not_spot':
            self.button_color = self.settings.color_yellow
            self.text_color = self.settings.font_white

        self.font = pygame.font.SysFont('Arial', self.settings.top_sq_font_size, True)

        # Build the top square's rect object and center it
        self.rect = pygame.Rect(self.x_coord, self.y_coord, self.width, self.height)

        # The button message has to be prepped only once.
        self._prep_top_sq_msg()

    def _prep_top_sq_msg(self):
        """Turn msg (value) into a rendered image and center text on the button"""

        # empty squares vs. filled-in squares
        if self.status == 'empty' or self.status == 'guess':
            self.msg_image = self.font.render(self.value, True, self.text_color,
                self.settings.bg_color)
        else:   
            self.msg_image = self.font.render(self.value, True, self.text_color,
                self.button_color)

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_top_square(self):
        # Draw a blank button and then draw the message

        if self.status == 'empty':
            self.button_color = self.settings.color_lt_gray
            self.text_color = self.settings.bg_color
        elif self.status == 'guess':
            self.button_color = self.settings.color_dk_gray
            self.text_color = self.settings.font_black
        elif self.status == 'wrong':
            self.button_color = self.settings.color_dk_gray
            self.text_color = self.settings.font_white
        elif self.status == 'correct_in_spot':
            self.button_color = self.settings.color_green
            self.text_color = self.settings.font_white
        elif self.status == 'correct_not_spot':
            self.button_color = self.settings.color_yellow
            self.text_color = self.settings.font_white

        self.rect = pygame.Rect(self.x_coord, self.y_coord, self.width, self.height)

        self._prep_top_sq_msg()

        
        if self.status == 'empty' or self.status == 'guess': # draw with border not filled 
            pygame.draw.rect(self.screen, self.button_color, self.rect, 4, 0)
        else:
            pygame.draw.rect(self.screen, self.button_color, self.rect, 0, 0)

        self.screen.blit(self.msg_image, self.msg_image_rect)

    def animate_guess(self):
        if self.status == 'guess':  #draw with animation
            self.rect_sm = pygame.Rect(self.x_coord+3, self.y_coord+3, 
                self.width-6, self.height-6)
            pygame.draw.rect(self.screen, self.button_color, self.rect_sm, 4, 0)
            pygame.display.flip()
            sleep(0.1)

    def animate_commit_part1(self):
        """First half of top square animation when you commit a guess.
              Up to the point where the status changes."""

        y_coord = self.y_coord
        height = self.height
        intervals = int(height/2)

        # prep letter scaling
        self._prep_top_sq_msg()
        self.letter_img = self.msg_image
        self.letter_img_rect = self.letter_img.get_rect()
        self.letter_img_height = self.letter_img_rect.height
        self.letter_img_width = self.letter_img_rect.width
        self.letter_img_y_coord = self.letter_img_rect.centery
        letter_interval_float = (self.letter_img_height/intervals)

        for y in range(0, intervals):
            y_coord += 1
            height -= 2
            self.rect_anim = pygame.Rect(self.x_coord, y_coord, 
                self.width, height)
            
            self.letter_img_height -= letter_interval_float
            LETTER_IMG_SIZE = (self.letter_img_width, int(self.letter_img_height))
            self.letter_img = pygame.transform.scale(self.letter_img, LETTER_IMG_SIZE)
            self.letter_img_rect = self.letter_img.get_rect()
            self.letter_img_rect.center = self.rect_anim.center

            # erase previous square
            pygame.draw.rect(self.screen, self.settings.bg_color, self.rect, 0, 0)

            # draw new square
            pygame.draw.rect(self.screen, self.button_color, self.rect_anim, 4, 0)

            # draw scaled letter image
            self.screen.blit(self.letter_img, self.letter_img_rect)

            pygame.display.flip()
            sleep(.005)

    def animate_commit_part2(self):

        if self.status == 'empty':
            self.button_color = self.settings.color_lt_gray
            self.text_color = self.settings.bg_color
        elif self.status == 'guess':
            self.button_color = self.settings.color_dk_gray
            self.text_color = self.settings.font_black
        elif self.status == 'wrong':
            self.button_color = self.settings.color_dk_gray
            self.text_color = self.settings.font_white
        elif self.status == 'correct_in_spot':
            self.button_color = self.settings.color_green
            self.text_color = self.settings.font_white
        elif self.status == 'correct_not_spot':
            self.button_color = self.settings.color_yellow
            self.text_color = self.settings.font_white

        y_coord = self.y_coord + (self.height/2)
        height = 1
        intervals = int(self.height/2)

        # prep letter scaling
        self._prep_top_sq_msg()
        self.letter_img = self.msg_image
        self.letter_img_rect = self.letter_img.get_rect()
        self.letter_img_height = self.letter_img_rect.height
        animation_height = 1
        self.letter_img_width = self.letter_img_rect.width
        letter_interval_float = (self.letter_img_height/intervals)
        
        for y in range(0, intervals):
            y_coord -= 1
            height += 2
            self.rect_anim = pygame.Rect(self.x_coord, y_coord, 
                self.width, height)

            animation_height += letter_interval_float
            LETTER_IMG_SIZE = (self.letter_img_width, int(animation_height))
            self.letter_img = self.msg_image
            self.letter_img = pygame.transform.scale(self.letter_img, LETTER_IMG_SIZE)
            self.letter_img_rect = self.letter_img.get_rect()
            self.letter_img_rect.center = self.rect_anim.center

            # draw new square
            pygame.draw.rect(self.screen, self.button_color, self.rect_anim, 4, 0)

            # draw scaled letter image
            self.screen.blit(self.letter_img, self.letter_img_rect)

            pygame.display.flip()
            sleep(.005)
 


class KeyboardKey:
    """Class to create keys for the virtual keyboard at the bottom of the 
           screen, and manage their status."""

    def __init__(self, wdl_game, letter, status, x_coord, y_coord):
        """Initialize Keyboard attributes."""
        self.settings = wdl_game.settings
        self.screen = wdl_game.screen
        self.screen_rect = self.screen.get_rect()
        # self.row = row
        # self.column = column
        self.letter = letter
        self.status = status
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.kb_key_rect = ''

        # Set the dimensions and properties of the square.
        if len(self.letter) > 1:  # big keys for Enter and Backspace
            self.width = self.settings.large_key_rect_width
        else: 
            self.width = self.settings.key_rect_width

        self.height = self.settings.key_rect_height

        # Note: unlike top squares, keyboard can't have status of 'empty'
        if self.status == 'default':
            self.button_color = self.settings.color_lt_gray
            self.text_color = self.settings.font_black
        elif self.status == 'wrong':
            self.button_color = self.settings.color_dk_gray
            self.text_color = self.settings.font_white
        elif self.status == 'correct_in_spot':
            self.button_color = self.settings.color_green
            self.text_color = self.settings.font_white
        elif self.status == 'correct_not_spot':
            self.button_color = self.settings.color_yellow
            self.text_color = self.settings.font_white

        self.font = pygame.font.SysFont('Arial', self.settings.key_sq_font_size, True)

        # Build the Key's rect object and center it
        self.rect = pygame.Rect(self.x_coord, self.y_coord, self.width, self.height)
        self.kb_key_rect = self.rect

        # The button message has to be prepped only once.
        self._prep_key_letter()

    def _prep_key_letter(self):
        """Turn letter into a rendered image and center text on the button"""

        # empty squares vs. filled-in squares
        self.msg_image = self.font.render(self.letter, True, self.text_color,
            self.button_color)

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_keyboard_key(self):
        # Draw a blank button and then draw the message

        if self.status == 'default':
            self.button_color = self.settings.color_lt_gray
            self.text_color = self.settings.font_black
        elif self.status == 'wrong':
            self.button_color = self.settings.color_dk_gray
            self.text_color = self.settings.font_white
        elif self.status == 'correct_in_spot':
            self.button_color = self.settings.color_green
            self.text_color = self.settings.font_white
        elif self.status == 'correct_not_spot':
            self.button_color = self.settings.color_yellow
            self.text_color = self.settings.font_white

        self.rect = pygame.Rect(self.x_coord, self.y_coord, self.width, self.height)

        self._prep_key_letter()

        pygame.draw.rect(self.screen, self.button_color, self.rect, 0, 4)

        self.screen.blit(self.msg_image, self.msg_image_rect)



    def _prep_key_letter(self):
        """Turn letter into a rendered image and center text on the button"""

        # empty squares vs. filled-in squares
        self.msg_image = self.font.render(self.letter, True, self.text_color,
            self.button_color)

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


#   pygame.draw.rect(surface, color, rect, width=0, border_radius=0, 
#       border_top_left_radius=-1, border_top_right_radius=-1, 
#       border_bottom_left_radius=-1, border_bottom_right_radius=-1)
#
#   width=0 is the width of the border, 0 fills the rectangle
#   border_radius is the pixels of curve, use first argument to make them all 
#       equal, or individual settings for unequal.