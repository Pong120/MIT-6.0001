import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Loads a list of valid words from a file.

    Reads the word list from the file specified by WORDLIST_FILENAME.
    The file is assumed to contain a single line with space-separated words
    in lowercase.  Prints a message indicating the number of words loaded.

    Returns:
        list: A list of strings, where each string is a word from the file.
    """
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    Chooses a random word from a list of words.

    Selects a word at random from the provided list of words.

    Args:
        wordlist (list): A list of strings, where each string is a word.

    Returns:
        str: A randomly selected word from the input list.
    """
    return random.choice(wordlist)


wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    Checks if the secret word has been completely guessed.

    Determines whether all the letters in the secret word have been guessed
    by comparing them to the letters the user has guessed so far.

    Args:
        secret_word (str): The word the user is trying to guess (lowercase).
        letters_guessed (list): A list of letters (strings) that the user has guessed (lowercase).

    Returns:
        bool: True if all letters in secret_word are in letters_guessed, False otherwise.
    '''
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    Constructs the partially guessed word.

    Creates a string representing the user's current progress in guessing the
    secret word.  Letters that have been guessed are shown, while unguessed
    letters are represented by underscores.

    Args:
        secret_word (str): The word the user is trying to guess.
        letters_guessed (list): A list of letters (strings) that the user has guessed.

    Returns:
        str: A string showing the correctly guessed letters and underscores for unguessed ones.
             e.g., if secret_word is "apple" and letters_guessed is ['a', 'e'], the function
             returns "a_pe".
    '''
    guessed_word = ''
    for letter in secret_word:
        if letter in letters_guessed:
            guessed_word += letter
        else:
            guessed_word += '_ ' # add space for better readability
    return guessed_word



def get_available_letters(letters_guessed):
    '''
    Determines the letters that have not yet been guessed.

    Creates a string containing all the letters of the alphabet that the user
    has not yet guessed.

    Args:
        letters_guessed (list): A list of letters (strings) that the user has guessed.

    Returns:
        str: A string containing the letters of the alphabet that are not in letters_guessed.
    '''
    available_letters = ""
    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            available_letters += letter
    return available_letters



def hangman(secret_word):
    '''
    Plays the Hangman game with the user.

    Implements the interactive Hangman game logic.  The computer chooses a secret
    word, and the user tries to guess it by guessing letters.  The user has a
    limited number of guesses.

    Args:
        secret_word (str): The secret word the user is trying to guess.
    '''
    word_length = len(secret_word)
    guesses = 6
    letters_guessed = []

    print("Welcome to Hangman!")
    print("I am thinking of a word that is", word_length, "letters long.")

    while guesses > 0:
        print("--------------------")
        print(f"You have {guesses} guesses left.")
        available_letters = get_available_letters(letters_guessed)
        print("Available letters:", available_letters)
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        print("Word:", guessed_word)

        user_guess = input('Please guess a letter: ').lower()

        if not user_guess.isalpha() or len(user_guess) != 1:
            print("Please enter a single letter.")
            continue
        elif user_guess in letters_guessed:
            print("You have already guessed that letter.")
            continue

        letters_guessed.append(user_guess)

        if user_guess in secret_word:
            print(f"Good guess: {user_guess} is in the word!")
        else:
            print(f"Sorry, {user_guess} is not in the word.")
            guesses -= 1

        guessed_word = get_guessed_word(secret_word, letters_guessed)
        if is_word_guessed(secret_word, letters_guessed):
            print("--------------------")
            print("Congratulations! You've guessed the word:", secret_word)
            break

    if guesses == 0 and not is_word_guessed(secret_word, letters_guessed):
        print("--------------------")
        print(f"You ran out of guesses. The word was: {secret_word}")


def match_with_gaps(my_word, other_word):
    '''
    Checks if a word matches a partially guessed word.

    Determines if a given word (`other_word`) matches the pattern of a
    partially guessed word (`my_word`), where unguessed letters are
    represented by underscores.

    Args:
        my_word (str):  The partially guessed word, containing letters and underscores.
        other_word (str): The word to compare against the partially guessed word.

    Returns:
        bool: True if the words match (same length, and matching letters in
              non-underscore positions), False otherwise.
    '''
    my_word = my_word.replace(' ', '')  # Remove spaces from my_word
    if len(my_word) != len(other_word):
        return False

    for i in range(len(my_word)):
        if my_word[i] != '_' and my_word[i] != other_word[i]:
            return False
    return True



def show_possible_matches(my_word):
    '''
    Displays words that match a partially guessed word.

    Finds and prints all the words from the word list that match the
    partially guessed word pattern.

    Args:
        my_word (str): The partially guessed word, containing letters and underscores.

    Returns:
        None:  Prints the matching words to the console, separated by spaces.
               If no matches are found, prints "No matches found".
    '''
    matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            matches.append(word)
    if not matches:
        print("No matches found")
    else:
        print(' '.join(matches))



def hangman_with_hints(secret_word):
    '''
    Plays Hangman with hints.

    Similar to the regular Hangman game, but allows the user to request
    hints by entering the '*' character.

     Args:
        secret_word (str): The secret word the user is trying to guess.
    '''
    word_length = len(secret_word)
    guesses = 6
    letters_guessed = []

    print("Welcome to Hangman!")
    print("I am thinking of a word that is", word_length, "letters long.")

    while guesses > 0:
        print("--------------------")
        print(f"You have {guesses} guesses left.")
        available_letters = get_available_letters(letters_guessed)
        print("Available letters:", available_letters)
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        print("Word:", guessed_word)

        user_guess = input('Please guess a letter: ').lower()

        if user_guess == '*':
            print("Possible matches:")
            show_possible_matches(guessed_word)
            continue

        if not user_guess.isalpha() or len(user_guess) != 1:
            print("Please enter a single letter or *.")
            continue
        elif user_guess in letters_guessed:
            print("You have already guessed that letter.")
            continue

        letters_guessed.append(user_guess)

        if user_guess in secret_word:
            print(f"Good guess: {user_guess} is in the word!")
        else:
            print(f"Sorry, {user_guess} is not in the word.")
            guesses -= 1

        guessed_word = get_guessed_word(secret_word, letters_guessed)
        if is_word_guessed(secret_word, letters_guessed):
            print("--------------------")
            print("Congratulations! You've guessed the word:", secret_word)
            break

    if guesses == 0 and not is_word_guessed(secret_word, letters_guessed):
        print("--------------------")
        print(f"You ran out of guesses. The word was: {secret_word}")





if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)

    