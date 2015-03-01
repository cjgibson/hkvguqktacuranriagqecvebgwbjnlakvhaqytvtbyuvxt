###
# AUTHORS: CHRISTIAN GIBSON, 
# PROJECT: REDDIT CHALLENGES
# UPDATED: FEBURARY 25, 2015
# USAGE:   
# EXPECTS: python 2.7.6
###

task = """
create a program that will ask the users name, age, and reddit username.
have it tell them the information back, in the format:

    your name is (blank), you are (blank) years old, and your username is (blank)

for extra credit, have the program log this information in a file to be
accessed later.
"""

import os
import time

def reddit_info(log=False):
    name = raw_input('What is your name? ')
    age = None
    while not age:
        try:
            age = raw_input('What is your age? ')
            age = int(age)
        except ValueError:
            try:
                age = float(age)
            except ValueError:
                age = None
                print "I'm sorry, that doesn't appear to be a number."
    username = raw_input('What is your reddit username? ')
    if not username.startswith('/u/'):
        username = '/u/' + username

    print ('your name is %s, '
           + 'you are %d years old, '
           + 'and your username is %s.') % (name, age, username)
    
    if log:
        if not os.path.isfile('reddit_user_data.csv'):
            header = True

        with open('reddit_user_data.csv', 'a') as fh:
            if header:
                fh.write('"timestamp","realname","realage","redditname"\n')
            fh.write('"%f","%s","%d","%s"\n' % (time.time, name, age, username))