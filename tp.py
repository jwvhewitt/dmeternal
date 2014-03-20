# Test Plots

import narrator
import context

print "Hellow World!"
init = narrator.plots.PlotState(rank=1)
nart = narrator.Narrative( init )

if nart.story:
    nart.story.display()
else:
    print "Plot loading failed."


if __name__=='__main__':
    import pygame
    import pygwrap
    import rpgmenu
    import campaign
    import util
    import pickle

    # Set the screen size.
    screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN )
#    screen = pygame.display.set_mode( (800,600) )
    pygame.init()
    pygwrap.init()
    rpgmenu.init()

    nart.build()
    camp = nart.camp

    camp.party = campaign.load_party( screen )

    if camp.party:
        for pc in camp.party:
            pc.choose_random_spells()
        camp.place_party()

#        camp.save()
#        f = open( util.user_dir( "rpg_BobDwarf19.sav" ) , "rb" )
#        camp = pickle.load( f )
#        f.close()

        camp.play( screen )


