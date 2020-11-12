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
        * Can't start hangman during a standup
        * Can't start a standup during hangman
        * Can't use message_sendlater for hangman related messages

Weather
    * /weather location
        * Returns the weather at that location
        * Tries to guess what location you meant if slightly incorrect
            * eg "/weather sydne" would return the weather of Sydney
    * Errors (taken care of)
        * Very incorrect locations will raise an InputError
            * eg "/weather 602" would raise an InputError

Reacts
    * Added 3 new reacts (heart, star and thumbDown)
    * Made the heart red
    * Made the star yellow
    * Can only react once on each message 
    * Created a new file for each react
        * src/components/Message/MessageReact2
        * src/components/Message/MessageReact3
        * src/components/Message/MessageReact4
    * Edited src/components/Message/index.js (to add each react)