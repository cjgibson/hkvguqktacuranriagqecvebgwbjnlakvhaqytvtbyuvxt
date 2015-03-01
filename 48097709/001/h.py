###
# AUTHORS: CHRISTIAN GIBSON, 
# PROJECT: REDDIT CHALLENGES
# UPDATED: FEBURARY 25, 2015
# USAGE:   
# EXPECTS: python 2.7.6
###

task = """
we all know the classic "guessing game" with higher or lower prompts.
lets do a role reversal; you create a program that will guess numbers
between 1-100, and respond appropriately based on whether users say
that the number is too high or too low. Try to make a program that can
guess your number based on user input and great code!
"""

def guess(floor=1, ceiling=100):
    if (not isinstance(floor, (int, float, long))
        or not isinstance(ceiling, (int, float, long))):
        raise TypeError
    elif floor > ceiling:
        floor, ceiling = ceiling, floor
    elif floor == ceiling:
        return floor

    current = (floor + ceiling)/2
    print 'My first guess is %d.' % current
    while True:
        _next = raw_input('Is that too high, too low, or correct? ')
        if 'h' in _next:
            ceiling = current - 1
        elif 'l' in _next:
            floor = current + 1
        elif 'c' in _next:
            return current
        else:
            print "I'm sorry, I didn't understand your input."
        current = (floor + ceiling)/2
        print 'My next guess is %d.' % current