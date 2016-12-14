#!/usr/bin/python2

import game

def play_the_game():
    game.main()

import random

def roll_stats():
    # Roll 4d6, throw away the smallest, and sum the rest.
    rolls = [ random.randint( 1 , 6 ) for x in range( 4 ) ]
    rolls.sort()
    del rolls[0]
    return sum( rolls )

def test_average(n):
    total = 0
    for t in xrange(n):
        total += roll_stats()
    print float(total)/n

if __name__=='__main__':
    #test_average(1000000)
    play_the_game()

