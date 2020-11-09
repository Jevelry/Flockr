EXTRA STUFF

Hangman
    * /hangman start word
        * Starts a game of hangman using 'word' as the word.
        * 'word' can have spaces, dashes and apostophes (which user's don't need to guess)
        * Hangman status gets pinned
    * /guess letter
        * Allows the user to guess a letter in the current hangman session
        * If letter is correct, all occurences of the letter is revealed
        * If guess is incorrect, hangman drawing updates
        * 9th incorrect guess will end the game
    * /hangman stop
        * Admins or the hangman 'creator' can stop an active hangman session
        * Used primarily to fix pinned messages or when word is not appropriate
    * hangman.py
        * Where most of the code is stored.
        * Contains 3 main functions (start, guess, stop) and other helper functions
    * hangman_draw.py
        * Where the hangman drawing for each stage is stored.
        * Gets called after every hangman guess
    * hangman_test.py
        * Where all the hangman tests are
    * Also edited:
        * message.py (Determine whether message is normal, guess, start or stop)
        * validation.py (Determine whether user can use each command)
        * data.py (Interacts directly with the hangman state in each channel)
    * Possible errors (All taken care of):
        * Creator can't guess their own word
        * Hangman word must be between 3 and 15 letters
        * Can only guess 1 letter at a time
        * Words and guesses must be letters only (No numbers, punctuation, etc)
            * Words can have spaces, dashes and apostrophes
        * Can't start a hangman session when one is already running
        * Can't guess the same successful letter multiple times
        * Can't use '/hangman stop' if not an owner or hangman starter
    * Assumptions (Not tested):
        * Can't start hangman during a startup
        * Can't start a startup during hangman
        * Can't use message_sendlater for hangman related messages