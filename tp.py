# Test Plots

import narrator
import context
import maps

print "Hellow World!"
init = narrator.plots.PlotState(rank=1)
nart = narrator.Narrative( init )

def display_contents( thing, lead="" ):
    thing.identified = True
    print lead + str( thing )
    if hasattr( thing, "contents" ):
        for sp in thing.contents:
            display_contents(sp,lead+" ")

def display_scenes( thing, lead="" ):
    if isinstance( thing, maps.Scene ):
        print lead + str( thing )
    if hasattr( thing, "contents" ):
        for sp in thing.contents:
            display_scenes(sp,lead+" ")

def display_contents2( thing, lead="" ):
    for t in narrator.plots.all_contents( thing ):
        print lead + str( t )


if nart.story:
    nart.story.display()
else:
    print "Plot loading failed."
    for e in nart.errors:
        print e

if __name__=='__main__':
    import pygame
    import pygwrap
    import rpgmenu
    import campaign
    import util
    import pickle

    if nart.story:

        # Set the screen size.
#        screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN )
        screen = pygame.display.set_mode( (800,600) )
        pygame.init()
        pygwrap.init()
        rpgmenu.init()

        display_scenes( nart.camp )

        nart.build()
        camp = nart.camp

        camp.party = campaign.load_party( screen )

        if camp.party:
            for pc in camp.party:
                pc.choose_random_spells()
            camp.place_party()

            camp.play( screen )




