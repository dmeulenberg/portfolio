# Welcome to Dave's version of Wordle.  Plan is to make a wordle clone you can
#    play as often as you like (wordle_practice), and then modify it into a 
#    party version you can plan online against other people.

import sys
import pygame
import pygame.font
import json

from time import sleep
from random import randint

from wdl_settings import Settings
from wdl_button import TopSquare, KeyboardKey


class Wordle:
    """Overall class for Wordle Game"""

    def __init__(self):
        """Initialize the game and create resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,
            self.settings.screen_height))
        pygame.display.set_caption("Wordle DM Practice mode")

        # Use FULLSCREEN MODE (replaces above) MUST BE ABLE TO QUIT WITH 'Q'!!
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # Only create the answer list once per session, so same word can't be 
        #     picked more than once.
        self._create_answer_list()
        self._create_allowed_guesses()


    def run_game(self):
        """Start the main loop for the game."""

        # Set a counter for timed messages
        self.game_counter = 0 

        self._start_game()
        self.screen.fill(self.settings.bg_color)
        pygame.display.flip()

        while True:
            self._check_events()

            # If game is in an active state
            if self.settings.game_active:
                self.game_counter += 1

            if self.settings.game_over:
                if not self.settings.game_active:
                    self._show_message("Press F12 (or tap Enter) to play again.")

            self._update_screen() 


    def _update_screen(self):
        #Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        for square in self.settings.top_grid:
            # square.surface.fill(self.settings.bg_color)
            square.draw_top_square()

        for key in self.settings.kb_row_1:
            key.draw_keyboard_key()

        for key in self.settings.kb_row_2:
            key.draw_keyboard_key()

        for key in self.settings.kb_row_3:
            key.draw_keyboard_key()

        if self.settings.show_message_flag == True:
            self.screen.blit(self.msg_image, self.msg_image_rect)
            if self.game_counter >= 3000:
                self.settings.show_message_flag = False
                
                if self.settings.game_over:
                    self.settings.game_active = False


        # Make the most recently drawn screen visible.
        pygame.display.flip()


    def _check_events(self):
        # Respond to keypresses and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Write high score to file
                # self.stats.write_high_score_to_file()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_key_buttons(mouse_pos)

    def _check_key_buttons(self, mouse_pos):
        """Accept key strokes from mouse on screen keyboard."""
        for kb_row in self.settings.kb_list:
            for key in kb_row:
                button_clicked = key.kb_key_rect.collidepoint(mouse_pos)
                if button_clicked and self.settings.game_active:
                    if len(key.letter) > 1:
                        if key.letter == 'BKSP':
                            self._backspace_key_pressed()
                        elif key.letter == 'ENTER':
                            if len(self.settings.current_guess) == 5:
                                self._commit_guess()
                    else:
                        self._letter_key_pressed(key.letter)

                # need a way to restart using mouse/touchscreen        
                elif button_clicked and not self.settings.game_active:
                    if key.letter == 'ENTER':
                        self._start_game()


    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_ESCAPE:
            # Quit if player presses 'ESCAPE'
            sys.exit()

        # Player pushes a letter key
        elif event.key == pygame.K_q:
            self._letter_key_pressed('Q')
        elif event.key == pygame.K_w:
            self._letter_key_pressed('W')
        elif event.key == pygame.K_e:
            self._letter_key_pressed('E')
        elif event.key == pygame.K_r:
            self._letter_key_pressed('R')
        elif event.key == pygame.K_t:
            self._letter_key_pressed('T')
        elif event.key == pygame.K_y:
            self._letter_key_pressed('Y')
        elif event.key == pygame.K_u:
            self._letter_key_pressed('U')
        elif event.key == pygame.K_i:
            self._letter_key_pressed('I')
        elif event.key == pygame.K_o:
            self._letter_key_pressed('O')
        elif event.key == pygame.K_q:
            self._letter_key_pressed('Q')
        elif event.key == pygame.K_p:
            self._letter_key_pressed('P')
        elif event.key == pygame.K_a:
            self._letter_key_pressed('A')
        elif event.key == pygame.K_s:
            self._letter_key_pressed('S')
        elif event.key == pygame.K_d:
            self._letter_key_pressed('D')
        elif event.key == pygame.K_f:
            self._letter_key_pressed('F')
        elif event.key == pygame.K_g:
            self._letter_key_pressed('G')
        elif event.key == pygame.K_h:
            self._letter_key_pressed('H')
        elif event.key == pygame.K_j:
            self._letter_key_pressed('J')
        elif event.key == pygame.K_k:
            self._letter_key_pressed('K')
        elif event.key == pygame.K_l:
            self._letter_key_pressed('L')
        elif event.key == pygame.K_z:
            self._letter_key_pressed('Z')
        elif event.key == pygame.K_x:
            self._letter_key_pressed('X')
        elif event.key == pygame.K_c:
            self._letter_key_pressed('C')
        elif event.key == pygame.K_v:
            self._letter_key_pressed('V')
        elif event.key == pygame.K_b:
            self._letter_key_pressed('B')
        elif event.key == pygame.K_n:
            self._letter_key_pressed('N')
        elif event.key == pygame.K_m:
            self._letter_key_pressed('M')

        elif event.key == pygame.K_F12:
            if not self.settings.game_active:
                self._start_game()

        elif event.key == pygame.K_BACKSPACE:
            # print("pressed the BACKSPACE key")
            self._backspace_key_pressed()

        elif event.key == pygame.K_RETURN:
            # print("Pressed the RETURN key")
            if len(self.settings.current_guess) == 5:
                self._commit_guess()

        elif event.key == pygame.K_KP_ENTER:
            # print("Pressed the (keypad) RETURN key")
            if len(self.settings.current_guess) == 5:
                self._commit_guess()


    def _start_game(self):
        """Start a new game with an empty set of squares."""
        self.settings.game_active = True
        self.settings.game_over = False
        self.settings.show_message_flag = False
        self.settings.initialize_dynamic_settings()
        self._create_top_squares()
        self._create_keyboard()
        self._pick_answer_word()

    

    def _create_top_squares(self):
        """Plot and display top 5 x 6 grid."""

        # Calculate horizontal centering
        total_width = self.settings.screen_width
        square_size = self.settings.top_square_size
        square_spacing = self.settings.top_square_spacing

        grid_width = (square_size * 5) + (square_spacing * 4)
        left_margin = (total_width - grid_width)/2

        # Vertical spacing starting point
        top_margin = self.settings.top_margin

        # Create a list of TopSquare objects
        self.settings.top_grid = []

        for row in range(0,6):
            for column in range(0,5):
                x_coord = left_margin + ((square_size + square_spacing) * column)
                y_coord = top_margin + ((square_size + square_spacing) * row)
                square = TopSquare(self, row, column, ' ', 'empty', x_coord, y_coord )

                self.settings.top_grid.append(square)

        # Set starting y coord for keyboard at 1 row below last top square.
        self.settings.top_kb_row_y = top_margin + ((square_size + square_spacing) * 6.3)

    def _create_keyboard(self):
        """Plot and display keyboard under top grid."""

        # Calculate horizontal centering
        total_width = self.settings.screen_width
        key_width = self.settings.key_rect_width
        lg_key_width = self.settings.large_key_rect_width
        key_height = self.settings.key_rect_height
        key_spacing = self.settings.key_rect_spacing
        num_key_row_1 = len(self.settings.key_row_1)
        num_key_row_2 = len(self.settings.key_row_2)
        num_key_row_3 = len(self.settings.key_row_3)


        # Vertical spacing starting point
        top_kb_row_y = self.settings.top_kb_row_y

    # Do this for each row in the keyboard

        grid_width = (key_width * num_key_row_1) + (key_spacing * (num_key_row_1 - 1))
        left_margin = (total_width - grid_width)/2
        
        # Create a list of Keyboard objects
        self.settings.kb_row_1 = []

        for key in range(0, num_key_row_1):
            x_coord = left_margin + ((key_width + key_spacing) * key)
            y_coord = top_kb_row_y
            kb_key = KeyboardKey(self, self.settings.key_row_1[key], 'default', x_coord, y_coord )

            self.settings.kb_row_1.append(kb_key)

        self.settings.kb_list.append(self.settings.kb_row_1)

    # Keyboard row 2
        self.settings.kb_row_2 = []

        grid_width = (key_width * num_key_row_2) + (key_spacing * (num_key_row_2 - 1))
        left_margin = (total_width - grid_width)/2

        for key in range(0, num_key_row_2):
            x_coord = left_margin + ((key_width + key_spacing) * key)
            y_coord = top_kb_row_y + key_height + (2 * key_spacing)
            kb_key = KeyboardKey(self, self.settings.key_row_2[key], 'default', x_coord, y_coord )

            self.settings.kb_row_2.append(kb_key)

        self.settings.kb_list.append(self.settings.kb_row_2)

    # Keyboard row 3
        self.settings.kb_row_3 = []

        grid_width = ((key_width * (num_key_row_3-2)) + (lg_key_width * 2) + 
            (key_spacing * (num_key_row_3 - 1)))
        left_margin = (total_width - grid_width)/2

        for key in range(0, num_key_row_3):
            if key == 0: #first big key
                x_coord = left_margin
            elif key >= 1: # middle regular-sized keys and last key
                x_coord = left_margin + lg_key_width + key_spacing + ((key_width + key_spacing) * (key-1))

            y_coord = top_kb_row_y + (2 * key_height) + (4 * key_spacing)
            kb_key = KeyboardKey(self, self.settings.key_row_3[key], 'default', x_coord, y_coord )

            self.settings.kb_row_3.append(kb_key)
    
        self.settings.kb_list.append(self.settings.kb_row_3)

    def _create_answer_list(self):
        """Open file of answer words and make it into a list."""

        filename = 'wordle_answers_alphabetical.txt'
        try:
            with open(filename) as f:
                lines = f.readlines()
                self.settings.answer_list = []

                # remove new line markers from list, make uppercase
                for line in lines:
                    word = line.rstrip()
                    word = word.upper()
                    self.settings.answer_list.append(word)

                # print(answer_list)
                # print(len(answer_list))

        except FileNotFoundError:
            print(f"ERROR: file {filename} not found.")
            sys.exit()


    def _create_allowed_guesses(self):
        """Open files of allowed guesses and answers, strip and combine them."""

        # Make allowable guesses list
        filename1 = 'wordle_allowed_guesses.txt'
        try:
            with open(filename1) as f:
                lines = f.readlines()
                self.settings.allowed_guesses = []

                # remove new line markers from list, make uppercase
                for line in lines:
                    word = line.rstrip()
                    word = word.upper()
                    self.settings.allowed_guesses.append(word)

        except FileNotFoundError:
            print(f"ERROR: file {filename1} not found.")
            sys.exit()

        # Add answer list as allowed guesses
        filename = 'wordle_answers_alphabetical.txt'
        try:
            with open(filename) as f:
                lines = f.readlines()

                # remove new line markers from list, make uppercase
                for line in lines:
                    word = line.rstrip()
                    word = word.upper()
                    self.settings.allowed_guesses.append(word)

                # print(self.settings.allowed_guesses)
                # print(len(self.settings.allowed_guesses))

        except FileNotFoundError:
            print(f"ERROR: file {filename} not found.")
            sys.exit()


    def _pick_answer_word(self):
        """Choose an answer from the answer list, remove it so the same answer
               can't be picked twice in one session."""

        answer_number = randint(0, (len(self.settings.answer_list)-1))
        self.settings.answer_word = self.settings.answer_list.pop(answer_number)


    def _letter_key_pressed(self, letter):
        """Respond to player entering a letter"""

        # Only accept a letter key press if the game is active
        if self.settings.game_active:

            # Only add a letter if there is an open space in the row
            if self.settings.guess_column_number <= 4:
                row_pos = self.settings.guess_row_number
                column_pos = self.settings.guess_column_number

                grid_list_pos = column_pos + (row_pos * 5)

                self.settings.top_grid[grid_list_pos].value = letter
                self.settings.top_grid[grid_list_pos].status = 'guess'

                self.settings.top_grid[grid_list_pos].animate_guess()

                # Advance to next square
                self.settings.guess_column_number += 1
                self.settings.current_guess += letter


    def _backspace_key_pressed(self):
        """Respond to player pressing backspace"""
        row_pos = self.settings.guess_row_number
        column_pos = self.settings.guess_column_number

        if column_pos > 0:
            grid_list_pos = column_pos + (row_pos * 5) -1    # -1 for backspace
        else:
            grid_list_pos = column_pos + (row_pos * 5) # don't go to prev line

        self.settings.top_grid[grid_list_pos].value = ' '
        self.settings.top_grid[grid_list_pos].status = 'empty'

        # reverse to next square, truncate current_guess by 1 letter
        if self.settings.guess_column_number > 0: #can't be negative
            self.settings.guess_column_number -= 1
            prev_len = len(self.settings.current_guess)
            prev_guess = self.settings.current_guess
            new_guess = prev_guess[:(prev_len - 1)]

            # set current_guess to truncated guess 
            self.settings.current_guess = new_guess
        else:
            pass
            # print("Can't backspace any more.")


    def _commit_guess(self):
        """Respond appropriately if the player hits the enter key."""

        # Only accept if game is active
        if self.settings.game_active:

            current_guess = self.settings.current_guess

            # Only respond if all 5 squares are full
            if self.settings.guess_column_number >= 5:
                # commit the guess
                if self.settings.guess_row_number == 0:
                    self.settings.guess_1 = current_guess
                elif self.settings.guess_row_number == 1:
                    self.settings.guess_2 = current_guess
                elif self.settings.guess_row_number == 2:
                    self.settings.guess_3 = current_guess
                elif self.settings.guess_row_number == 3:
                    self.settings.guess_4 = current_guess
                elif self.settings.guess_row_number == 4:
                    self.settings.guess_5 = current_guess
                elif self.settings.guess_row_number == 5:
                    self.settings.guess_6 = current_guess

                print(f"\nGuesses:\n1. {self.settings.guess_1}")
                print(f"2. {self.settings.guess_2}")  
                print(f"3. {self.settings.guess_3}")
                print(f"4. {self.settings.guess_4}")
                print(f"5. {self.settings.guess_5}")
                print(f"6. {self.settings.guess_6}") 

                self._check_guess()


    def _check_guess(self):
        """Check current guess against allowed guesses, update grid with
             correct/incorrect letters"""

        # Check current guess against allowed guesses
        if self.settings.current_guess in self.settings.allowed_guesses:

            self._update_statuses()

            
            # Reset to next row
            self.settings.guess_column_number = 0
            self.settings.guess_row_number += 1
            self.settings.current_guess = ''

        else:
            self._shake_current_row()
            self._show_message("Not in word list.")

    def _update_statuses(self):
        """Update statuses of guess with colored letters based on matches"""

        answer_word = self.settings.answer_word
        current_guess = self.settings.current_guess

        # Not sure where animation will fit in this,
        row_pos = self.settings.guess_row_number
        row_first_num = row_pos * 5
        row_last_num = row_first_num + 5

        # Compare each letter of guess to answer word, change status to dark gray
        #    or yellow.  Will change to green in next step.

        # print("Parsing current_guess")
        column_pos = 0
        letter_pos = 0
        guess_word_letters = []
        guess_double_letters = {}
        answer_word_letters = []
        answer_double_letters = {}

        # Double letters in current guess must have special handling
        for letter in current_guess:
            guess_word_letters.append(letter)

            occurences = current_guess.count(letter)
            if occurences > 1:
                guess_double_letters[letter] = occurences
                print(guess_double_letters)


        for letter in answer_word:
            answer_word_letters.append(letter)

            occurences = answer_word.count(letter)
            if occurences > 1:
                answer_double_letters[letter] = occurences

        # print(guess_word_letters)
        # print(guess_double_letters)
        # print(answer_word_letters)
        # print(answer_double_letters)


        # check for dark gray or yellow letters
        double_letter_counter = 0

        for letter in guess_word_letters:
            grid_list_pos = row_first_num + column_pos

            if letter in answer_word_letters:  # guess letter is in answer

                if letter in guess_double_letters: # letter is repeated in guess
                    gdl = guess_double_letters[letter] # gdl = occurences in guess
                else:
                    gdl = 1

                if letter in answer_double_letters:
                    adl = answer_double_letters[letter] # adl = occurences in answer
                else:
                    adl = 1


                print(f"gdl = {gdl} adl = {adl}")
                if gdl <= adl: # make all yellow
                    self.settings.top_grid[grid_list_pos].new_status = 'correct_not_spot'
                    self._update_keyboard(letter, 'correct_not_spot')
                elif gdl > adl: # make some yellow, remainder dark gray
                    if double_letter_counter < adl:  # make yellow
                        self.settings.top_grid[grid_list_pos].new_status = 'correct_not_spot'
                        self._update_keyboard(letter, 'correct_not_spot')
                        double_letter_counter += 1
                    else: #  make dark gray
                        self.settings.top_grid[grid_list_pos].new_status = 'wrong'
                        self._update_keyboard(letter, 'wrong')
                        double_letter_counter += 1

            else: # guess letter is NOT in answer
                self.settings.top_grid[grid_list_pos].new_status = 'wrong'
                self._update_keyboard(letter, 'wrong')
            column_pos += 1

        # check for green letters
        # print("\nChecking for green letters")
        for letter_pos in range(0, 5):
            grid_list_pos = row_first_num + letter_pos
            letter = guess_word_letters[letter_pos]
            # print(f"{letter_pos}- Does {guess_word_letters[letter_pos]} == {answer_word_letters[letter_pos]}, {guess_double_letters}, {gdl}, {adl}")
            
            if guess_word_letters[letter_pos] == answer_word_letters[letter_pos]:
                self.settings.top_grid[grid_list_pos].new_status = 'correct_in_spot'
                self._update_keyboard(letter, 'correct_in_spot')


                # Check for double letters
                for letter in guess_word_letters:
                    grid_list_pos = row_first_num + column_pos

                    if letter in answer_word_letters:  # guess letter is in answer

                        if letter in guess_double_letters: # letter is repeated in guess
                            gdl = guess_double_letters[letter] # gdl = occurences in guess
                        else:
                            gdl = 1

                        if letter in answer_double_letters:
                            adl = answer_double_letters[letter] # adl = occurences in answer
                        else:
                            adl = 1

                    if gdl > adl:

                        for dbl_letter_pos in range(0, letter_pos):
                            if guess_word_letters[dbl_letter_pos] == answer_word_letters[letter_pos]:
                                dbl_grid_list_pos = row_first_num + dbl_letter_pos
                                self.settings.top_grid[dbl_grid_list_pos].new_status = 'wrong'
                                self._update_keyboard(letter, 'wrong')

        self._update_grid_and_animate()

        if current_guess == answer_word:
            print("\n*********************")
            print("****             ****")
            print("**** YOU WIN !!! ****")
            print("****             ****")
            print("*********************")
            self._update_screen()

            self._animate_win_happy_dance()

            self.settings.game_over = True
            #self.settings.game_active = False

            if row_pos == 0:
                self._show_message("Holy crap!!")
            elif row_pos == 1:
                self._show_message("Wow!!")
            elif row_pos == 2:
                self._show_message("Impressive!!")
            elif row_pos == 3:
                self._show_message("Excellent!")
            elif row_pos == 4:
                self._show_message("Well done.")
            elif row_pos == 5:
                self._show_message("Phew!!")

        if row_pos == 5 and current_guess != answer_word:
            print("\n********************")
            print("****            ****")
            print("**** YOU LOSE.  ****")
            print("****            ****")
            print("********************")

            self.settings.game_over = True
            #self.settings.game_active = False

            self._show_message(f"'{answer_word}'")

    def _animate_win_happy_dance(self):
        """Show the happy dance for each letter in winning guess."""

        # answer_word = self.settings.answer_word
        # current_guess = self.settings.current_guess

        row_pos = self.settings.guess_row_number
        row_first_num = row_pos * 5
        row_last_num = row_first_num + 5
        grid_list_pos = row_first_num 

        height = self.settings.top_square_size
        intervals = int(height/2)
        delay = int(intervals/2)
        anim_length = height + (4 * delay)

        # set a y_coord for each letter to beginning set, save orig for end
        y_coord_orig = self.settings.top_grid[grid_list_pos].y_coord
        y_coord_1 = y_coord_orig
        y_coord_2 = y_coord_orig
        y_coord_3 = y_coord_orig
        y_coord_4 = y_coord_orig
        y_coord_5 = y_coord_orig

        grid_list_pos_1 = grid_list_pos
        grid_list_pos_2 = grid_list_pos + 1
        grid_list_pos_3 = grid_list_pos + 2
        grid_list_pos_4 = grid_list_pos + 3
        grid_list_pos_5 = grid_list_pos + 4
        
        # column_pos = 0
        # letter_pos = 0

        for x in range(0, anim_length):
            # set y_coord for 1st square
            if x >= 0 and x < intervals:  # 1st square goes up
                y_coord_1 -= 1
            elif x >= intervals and y_coord_1 < y_coord_orig:
                y_coord_1 += 1
            else:
                y_coord_1 = y_coord_orig

            # set y_coord for 2nd square
            if x >= delay*1 and x < intervals+(delay*1):
                y_coord_2 -= 1
            elif x >= intervals+(delay*1) and y_coord_2 < y_coord_orig:
                y_coord_2 += 1
            else:
                y_coord_2 = y_coord_orig

            # set y_coord for 3rd square
            if x >= delay*2 and x < intervals+(delay*2):
                y_coord_3 -= 1
            elif x >= intervals+(delay*2) and y_coord_3 < y_coord_orig:
                y_coord_3 += 1
            else:
                y_coord_3 = y_coord_orig

            # set y_coord for 4th square
            if x >= delay*3 and x < intervals+(delay*3):
                y_coord_4 -= 1
            elif x >= intervals+(delay*3) and y_coord_4 < y_coord_orig:
                y_coord_4 += 1
            else:
                y_coord_4 = y_coord_orig

            # set y_coord for 5th square
            if x >= delay*4 and x < intervals+(delay*4):
                y_coord_5 -= 1
            elif x >= intervals+(delay*4) and y_coord_5 < y_coord_orig:
                y_coord_5 += 1
            else:
                y_coord_5 = y_coord_orig

            # update y_coord for each square:
            self.settings.top_grid[grid_list_pos_1].y_coord = y_coord_1
            self.settings.top_grid[grid_list_pos_2].y_coord = y_coord_2
            self.settings.top_grid[grid_list_pos_3].y_coord = y_coord_3
            self.settings.top_grid[grid_list_pos_4].y_coord = y_coord_4
            self.settings.top_grid[grid_list_pos_5].y_coord = y_coord_5

            # draw the squares
            self._update_screen()
            sleep(.003)  # .005


    def _update_grid_and_animate(self):
        """ """
        answer_word = self.settings.answer_word
        current_guess = self.settings.current_guess

        row_pos = self.settings.guess_row_number
        row_first_num = row_pos * 5
        row_last_num = row_first_num + 5

        column_pos = 0
        letter_pos = 0
        guess_word_letters = []
        answer_word_letters = []

        for letter in current_guess:
            guess_word_letters.append(letter)

        for letter in answer_word:
            answer_word_letters.append(letter)

        for letter_pos in range(0, 5):
            grid_list_pos = row_first_num + letter_pos
            #letter = guess_word_letters[letter_pos]
            # print(f"{letter_pos}- Does {guess_word_letters[letter_pos]} == {answer_word_letters[letter_pos]}, {guess_double_letters}, {gdl}, {adl}")
            
            self.settings.top_grid[grid_list_pos].animate_commit_part1()
            self.settings.top_grid[grid_list_pos].status = self.settings.top_grid[grid_list_pos].new_status
            self.settings.top_grid[grid_list_pos].animate_commit_part2()
            self.settings.top_grid[grid_list_pos].new_status = ''


    def _update_keyboard(self, letter, status):
        """Update the status of the keyboard letters so they change color."""
        if letter in self.settings.key_row_1:
            key_number = self.settings.key_row_1.index(letter)
            self.settings.kb_row_1[key_number].status = status

        elif letter in self.settings.key_row_2:
            key_number = self.settings.key_row_2.index(letter)
            self.settings.kb_row_2[key_number].status = status

        elif letter in self.settings.key_row_3:
            key_number = self.settings.key_row_3.index(letter)
            self.settings.kb_row_3[key_number].status = status


    def _shake_current_row(self):
        """Shake current row if guess is not in word list."""
        row_pos = self.settings.guess_row_number
        row_first_num = row_pos * 5
        row_last_num = row_first_num + 5
        
        for shakes in range(0, 4):  # number of back and forths
            for square in range(row_first_num, row_last_num):  # start_row
                self.settings.top_grid[square].x_coord += 3
            self._update_screen()
            sleep(0.05)

            for square in range(row_first_num, row_last_num):
                self.settings.top_grid[square].x_coord -= 3
            self._update_screen()
            sleep(0.05)


    def _show_message(self, message):
        """Display a message (Not in word list, or a winning message)."""
        self.font = pygame.font.SysFont('Arial', self.settings.top_sq_font_size, True)
        self.screen_rect = self.screen.get_rect()

        self.settings.show_message_flag = True
        self.game_counter = 0

        self.msg_image = self.font.render(message, True, 
            self.settings.font_black, self.settings.bg_color)

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center

        # self.screen.blit(self.msg_image, self.msg_image_rect)
        # pygame.display.flip()
        # sleep(2.5)



# ********** MAIN INSTANCE OF GAME **********

if __name__ == '__main__':
    # Make game instance and run game
    wdl = Wordle()
    wdl.run_game()