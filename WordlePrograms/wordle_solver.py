

def create_answer_list():
# *** Open and create list of answer words ***

    filename = 'wordle_answers_alphabetical.txt'
    allowed_guesses = []
    temp_list = []
    try:
        with open(filename) as f:
            lines = f.readlines()

            # remove new line markers from list, make uppercase
            for line in lines:
                word = line.rstrip()
                word = word.upper()
                allowed_guesses.append(word)

            # print(allowed_guesses)
            # print(len(allowed_guesses))

    except FileNotFoundError:
        print(f"ERROR: file {filename} not found.")

    # copy allowed_guesses list to deletable_list
    deletable_list = allowed_guesses[:]
    to_be_deleted = []

    print(f"  *****\n  *****   deletable list start = {len(deletable_list)}\n  *****\n")
    answer_count = 0

    return deletable_list




# **********************************
# *** User interface CLI program ***
# **********************************

def welcome_user():
    print("\n\n\n")
    print("*********************************")
    print("*** Welcome to Wordle Solver! ***")
    print("*********************************")
    print("\n")
    print("Make your first guess, then enter the results below:\n")

def get_guess_results_gray(letters_out):
    print("Enter the DARK GRAY letters, separated by commas (no spaces)")
    print("Do not enter gray letters that are also yellow or green.")

    ltrs_out = input("Example: G,R,Y:   ")
    # ltrs_out = "o, u, T,"

    ltrs_out_list = ltrs_out.rsplit(",")
    # print(ltrs_out_list)

    updated_list = []
    for ltr in ltrs_out_list:
        ltr = ltr.upper()
        if len(ltr) > 1:
            ltr = ltr.strip()
        updated_list.append(ltr)

    ltrs_out_list = updated_list

    for ltr in ltrs_out_list:       # add dark gray letters to letters_out list, it is cumulative
        letters_out.append(ltr)

    # print(ltrs_out_list)
    print(letters_out)
    print("\n")
    return letters_out


def get_guess_results_yellow(yellow_letters):
    print("\nEnter only the YELLOW letters, separated by commas. Enter nothing where ")
    print("there are letters that are not yellow. You should have 4 commas total.")
    yellowLetters = input("Example: Y,,L,,:   ")
    # yellowLetters = ",y,   ,o, "  

    if len(yellowLetters) > 0:

        yellowLettersList = yellowLetters.rsplit(",")
        # print(yellowLettersList)

        updated_list = []
        for ltr in yellowLettersList:
            ltr = ltr.upper()   # make uppercase
            if len(ltr) > 1:    # strip extra spaces
                ltr = ltr.strip()
            if ltr == " ":
                ltr = ""
            updated_list.append(ltr)

        yellowLettersList = updated_list
        yellow_letters.append(yellowLettersList)     # append the entire list into yellowLetters--it is a list of lists
        
    else: 
        yellow_letters.append(["","","","",""])

    print(yellow_letters)    
    print("\n")
    return yellow_letters



def get_guess_results_green():
    print("\nEnter only the GREEN letters, separated by commas. Enter nothing where ")
    print("there are letters that are not yellow. You should have 4 commas total.")
    greenLetters = input("Example: G,,E,,:   ")
    # greenLetters = ",g, r  ,e, "  

    if len(greenLetters) > 0:

        greenLettersList = greenLetters.rsplit(",")
        # print(greenLettersList)

        updated_list = []
        for ltr in greenLettersList:
            ltr = ltr.upper()   # make uppercase
            if len(ltr) > 1:    # strip extra spaces
                ltr = ltr.strip()
            if ltr == " ":
                ltr = ""
            updated_list.append(ltr)

        greenLettersList = updated_list

        green_letters = greenLettersList        # replace green_letters with current list
    else:
        green_letters = ["","","","",""]

    print(green_letters)
    print("\n")
    return green_letters








# ******************************************
# *** Get yellow and green calcs done ***
# ******************************************


def combine_yellow_letter_lists(yellow_letters):
    # Combine yellow letter lists into one list of yellow letters for yl check #1
    print("Combining yellow letters into one list for check #1")
    yl_letters_ck1 = []

    for yl_list in yellow_letters:
        print(f"  {yl_list}")
        for letter in yl_list:
            if letter == "":
                # print("  Space.")
                pass
            else:
                if letter in yl_letters_ck1:
                    # print(f"  {letter} already in yl_letters_ck1")
                    pass
                else:
                    yl_letters_ck1.append(letter)
                    # print(f"  Added {letter}.")
        # print("\n")

    print("\nyl_letters_ck1:  "  , end="")
    print(yl_letters_ck1)
    # print("\n")

    # print(f"  Entered yl_count: {yl_count}")

    return yl_letters_ck1

def calculate_yl_count(yl_letters_ck1):
    # Calculate yl_count
    yl_count = len(yl_letters_ck1)
    print(f"Calculated yl_count: {yl_count}\n")
    return yl_count

def calculate_gl_count(green_letters):
    #print("Calculating gl_count")
    # print(f"  Entered gl_count: {gl_count}")

    print(green_letters)

    gl_count = 0

    for letter in green_letters:
        if letter == "":
            # print("     Space.")
            pass
        else:
            # print(f"     {letter}")
            gl_count += 1

    print(f"Calculated gl_count: {gl_count}\n")
    return gl_count




def check_answers(deletable_list, yellow_letters, yl_count, green_letters, gl_count):
    # print(f"  *****\n  *****   deletable list before gray check = {len(deletable_list)}\n  *****\n")
    #  ****** REMOVE ALL WORDS WITH LETTERS IN LETTERS_OUT ********
    print("*** Removing words that contain dark gray letters ***")

    to_be_deleted = []

    for word in deletable_list:
        # print(word)

        for letter in word:
            # print(f"{letter} :: {word}")

            # is the letter in "letters out"? If so, go to next word
            if letter in letters_out:
                # print(f"{letter} :: {word} LETTER OUT")
                if not word in to_be_deleted:
                    to_be_deleted.append(word)

    # print(f"\nTo be deleted after dark gray letter check: {len(to_be_deleted)}\n{to_be_deleted}\n\n")

    for word in to_be_deleted:
        deletable_list.remove(word)

    # print(f"*****\n*****   deletable list after gray letters = {len(deletable_list)}\n*****\n\n")


    #  ***** REMOVE WORDS THAT DON'T MATCH GREEN LETTERS ****
    print("*** Removing words that don't match green letters ***")

    if gl_count > 0:

        to_be_deleted = []

        for word in deletable_list:
            # print(word)
            x = 0
            gl = 0

            for letter in word:
            # print(f"{letter} :: {word}")
                
                # is it a green letter matching position?
                if letter == green_letters[x]:
                    gl += 1
                    # print(f"YES --{letter}, x={x}, {green_letters}, gl={gl}")
                else:
                    pass
                    # print(f"NO --{letter}, x={x}, {green_letters}, gl={gl}")

                x += 1

            if gl != gl_count:
                to_be_deleted.append(word)
                # print(f"adding {word} to to_be_deleted\n")
            else:
                pass
                # print("Word matches. Go on.\n")

            # print(f"to be deleted after green letter check: {len(to_be_deleted)}")
            # print(to_be_deleted)
            # print("\n")

        for word in to_be_deleted:
            deletable_list.remove(word)

        # print(f"\n*****\n*****   deletable list after green letters = {len(deletable_list)}\n*****\n")

    else:
        print("No green letters.  Skip this step.")


    #  ***** REMOVE WORDS THAT DON'T CONTAIN YELLOW LETTERS ****
    print("*** Removing words that don't have yellow letters.  DUPLICATE LETTERS MAY NOT BE ACCOUNTED FOR ***")

    # to_be_deleted = []

    if yl_count > 0:

        # Simplified version

        # print(f"yellow letters = {yl_letters_ck1}\n")


        for yellow_letter in yl_letters_ck1:

            to_be_deleted = []

            # print(f"\n***************************************\n\nYellow Letter '{yellow_letter}'\n")

            for word in deletable_list:
                # print(f"\nIs {yellow_letter} in {word}?", end="")
                if yellow_letter in word:
                    pass
                    # print(f"   Yes, go on.")
                else:  # Yellow letter not in word, delete it. 
                    if word not in to_be_deleted:
                        # print(f"   No. Adding {word} to to_be_deleted")
                        to_be_deleted.append(word) 

            # print(f"\nDeleting words with {yellow_letter}. from deletable_list")
            # print(f"   Records in deletable_list: {len(deletable_list)}")
            # print(f"   Records in to_be_deleted: {len(to_be_deleted)}\n")
            for word in to_be_deleted:
                # print(f"preparing to remove {word} from deletable_list")
                deletable_list.remove(word)
                # print("Removed.\n")
            # print(f"   Records in deletable_list AFTER yellow letter {yellow_letter}: {len(deletable_list)}\n\n")

        # print(f"\n*****\n*****   deletable list after yellow letter check #1 = {len(deletable_list)}\n*****\n\n")
        # print(f"Deletable list:  {deletable_list}")

    else:
        print("No yellow letters.  Skip this step.")


    #  ***** REMOVE WORDS THAT MATCH YELLOW LETTERS BY POSITION ****
    print("*** Removing words that match yellow letter by position ***")

    if yl_count > 0:

        # to_be_deleted = []

        for yl_list in yellow_letters:
            to_be_deleted = []

            for word in deletable_list:
                # print(word)
                x = 0
                yl = 0

                for letter in word:
                # print(f"{letter} :: {word}")
                    
                    # is it a yellow letter matching position?
                    if letter == yl_list[x]:
                        yl += 1
                        # print(f"YES --{letter}, x={x}, {yl_list}, yl={yl}")

                        # if yellow letter matches, then word should be removed
                        if word in to_be_deleted:
                            pass
                            # print(f"{word} is already in to_be_deleted")
                        else:
                            to_be_deleted.append(word)
                            # print(f"Added {word} to to_be_deleted.")
                     
                    else:
                        pass
                        # print(f"NO --{letter}, x={x}, {yl_list}, yl={yl}")

                    x += 1

                # print(f"to be deleted: {len(to_be_deleted)}")
                # print(to_be_deleted)
                # print("\n")

            # print(f"\n\nDeletable list: {deletable_list}\n")
            # print(f"to be deleted: {to_be_deleted}\n")

            for word in to_be_deleted:
                deletable_list.remove(word)

        # print(f"\n\n*****\n*****   deletable list after yellow letter check #2 = {len(deletable_list)}\n*****\n\n")

    else:
        print("No yellow letters.  Skip this step.")
    return deletable_list


def print_remaining_answers():
    # ***** WRAP IT UP WITH A BOW *****

    # print("\n\nDeletable list (end):")
    # print(deletable_list)
    # print(len(deletable_list))
    # print("\n")
    # print("To be deleted (end):")
    # print(to_be_deleted)
    # print(len(to_be_deleted))



    # print("\n\nDeletable list (after deletions):")
    # print(deletable_list)
    # print(f"Answers: {len(deletable_list)}")

    print(f"\n\nRemaining answers: ")
    for word in deletable_list:
        print(word)
    if len(deletable_list) == 1:
        print(f"{len(deletable_list)} remaining answer.\n")
    else:
        print(f"{len(deletable_list)} remaining answers.\n")



# *************************
# *** MAIN GAME ROUTINE ***
# *************************

letters_out = []   
yellow_letters = []     # a list containing lists
green_letters = []  
allowed_guesses = []
temp_list = []
to_be_deleted = []
deletable_list = []
yl_letters_ck1 = []

yl_count = 0
gl_count = 0
answer_count = 0

deletable_list = create_answer_list()
welcome_user()

for rounds in range(6):
    print("\n***** ROUND " + str(rounds + 1) + " *****")
    
    letters_out = get_guess_results_gray(letters_out)
    yellow_letters = get_guess_results_yellow(yellow_letters)
    green_letters = get_guess_results_green()

    yl_letters_ck1 = combine_yellow_letter_lists(yellow_letters)
    yl_count = calculate_yl_count(yl_letters_ck1)
    gl_count = calculate_gl_count(green_letters)

    deletable_list = check_answers(deletable_list, yellow_letters, yl_count, green_letters, gl_count)
    print_remaining_answers()

    print("Make your next guess from the list above.\n")
    if input("Did you win? (y/n)  ").lower() == "y":
        print("\nCONGRATULATIONS!!! YOU ARE A WINNER!!")
        break





# ************************
# *** END GAME ROUTINE ***
# ************************

