"""
This file contains the ASCII art for the different hangman stages.
This art mostly came from https://gieseanw.wordpress.com/2010/03/29/ascii-hangman/
and https://github.com/gieseanw/Hangman/blob/master/HangmanLogo2.txt.

While most of this art was found on the internet, I edited the base to make it
more prism-y, and I adjusted it for each of the different stages. I then adjusted it
so the pictures would look ok in flockr (which uses uneven letter spacing unfortunately)
"""
def mode_0():
    return ""
    
def mode_1():
    """
    After 1 incorrect guess
    """
    return """
       _______________
     /                          /|
   /______________ /  |
   |1 INCORRECT |  /
   |______________|/
    """

def mode_2():
    """
    After 2 incorrect guesses
    """
    return """

                  |
                  |
                  |
                  |
                  |
       ______|_________
     /           |              /|
   /______________ /  |
   |2 INCORRECT |  /
   |______________|/
"""

def mode_3():
    """
    After 3 incorrect guesses
    """
    return """
                  _______
                  |/       \\|
                  |
                  |
                  |
                  |
       ______|_________
     /           |              /|
   /______________ /  |
   |3 INCORRECT |  /
   |______________|/
"""

def mode_4():
    """
    After 4 incorrect guesses
    """
    return """
                  _______
                  |/       \\|
                  |         @
                  |
                  |
                  |
       ______|_________
     /           |              /|
   /______________ /  |
   |4 INCORRECT |  /
   |______________|/
"""

def mode_5():
    """
    After 5 incorrect guesses
    """
    return """
                  _______
                  |/       \\|
                  |         @
                  |          | 
                  |          |
                  |
       ______|_________
     /           |              /|
   /______________ /  |
   |5 INCORRECT |  /
   |______________|/
"""

def mode_6():
    """
    After 6 incorrect guesses
    """
    return """
                  _______
                  |/       \\|
                  |         @
                  |         /|
                  |          |
                  |
       ______|_________
     /           |              /|
   /______________ /  |
   |6 INCORRECT |  /
   |______________|/
"""

def mode_7():
    """
    After 7 incorrect guesses
    """
    return """
                  _______
                  |/       \\|
                  |         @
                  |         /|\\ 
                  |          |
                  |
       ______|_________
     /           |              /|
   /______________ /  |
   |7 INCORRECT |  /
   |______________|/
"""

def mode_8():
    """
    After 8 incorrect guesses
    """
    return """
                  _______
                  |/       \\|
                  |         @
                  |         /|\\ 
                  |          |
                  |         /
       ______|_________
     /           |              /|
   /______________ /  |
   |8 INCORRECT |  /
   |______________|/
"""

def mode_9():
    """
    After 9 incorrect guesses
    """
    return """
                  _______
                  |/       \\|
                  |         @
                  |         /|\\ 
                  |          |
                  |         / \\
       ______|_________
     /           |              /|
   /______________ /  |
   |9 INCORRECT |  /
   |______________|/
"""


def draw(mode):
    if mode == 0:
        return mode_0()
    if mode == 1:
        return mode_1()
    if mode == 2:
        return mode_2()
    if mode == 3:
        return mode_3()
    if mode == 4:
        return mode_4()
    if mode == 5:
        return mode_5()
    if mode == 6:
        return mode_6()
    if mode == 7:
        return mode_7()
    if mode == 8:
        return mode_8()
    if mode == 9:
        return mode_9()

if __name__ == '__main__':
    for i in range(1,10):
        print('=============')
        print(draw(i))
        print('=============')

