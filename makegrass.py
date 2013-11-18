import pygame
import random
import util
import collections

if __name__=='__main__':
    import random

    # Set the screen size.
    screen = pygame.display.set_mode( (432,432) )

    # Analyze the sample.
    sample = pygame.image.load( util.image_dir( "sample.png" ) ).convert()

    # There are two ways to try and copy a terrain texture- the first is just
    # to apply random colors with the same frequency as the sample. The second
    # is to use a left to right markov chain generator to decide on pixel colors.
    spots = []
    mc_spots = collections.defaultdict( list )

    last_a,last_b,last_c = (0,0,0,255),(0,0,0,255),(0,0,0,255)

    for y in range( sample.get_height() ):
        for x in range( sample.get_width() ):
            c = sample.get_at( (x,y) )
            if c != (0,0,0,255):
                spots.append( c )
                mc_spots[(last_a,last_b,last_c)].append(c)
                last_a,last_b,last_c = last_b,last_c,c

    spots = spots * 100
    random.shuffle( spots )

    i = 0
    last_a,last_b,last_c = (0,0,0,255),(0,0,0,255),(0,0,0,255)
    for y in range( 432 ):
        for x in range( 432 ):
            screen.set_at( (x,y), spots[i] )
            i += 1
            if i >= len( spots ):
                i = 0

    pygame.image.save( screen , "out_shuffle.png" )
    pygame.display.flip()


    i = 0
    last_a,last_b,last_c = (0,0,0,255),(0,0,0,255),(0,0,0,255)
    for y in range( 432 ):
        for x in range( 432 ):
            c = random.choice( mc_spots[(last_a,last_b,last_c)] )
            screen.set_at( (x,y), c )
            last_a,last_b,last_c = last_b,last_c,c

    pygame.image.save( screen , "out_markovchain.png" )
    pygame.display.flip()

    while True:
        ev = pygame.event.wait()
        if ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
            break



