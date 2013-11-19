import pygame
import image

GROUND1, GROUND2, WATER = range( 3 )

class Tile( object ):
    def __init__(self, floor=GROUND1, wall=None, decor=None, visible=False):
        self.floor = floor
        self.wall = wall
        self.decor = decor
        self.visible = visible


class Scene( object ):
    def __init__(self,width=128,height=128):
        self.width = width
        self.height = height
        self.contents = []
        # Fill the map with empty tiles
        self.map = [[ Tile()
            for y in range(height) ]
                for x in range(width) ]

    def on_the_map( self , x , y ):
        # Returns true if on the map, false otherwise
        return ( ( x >= 0 ) and ( x < self.width ) and ( y >= 0 ) and ( y < self.height ) )

class SceneView( object ):
    def __init__( self, scene ):
        self.ground_gfx = image.Image( "terrain_ground_forest.png", 54, 54 )


if __name__=='__main__':
    import random
    import pygwrap
    import util

    pygame.init()

    # Set the screen size.
    screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN )

    myimg = image.Image( "terrain_ground_forest.png", 54, 54 )

    def WaitAMinit():
        while True:
            ev = pygame.event.wait()
            if ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
                break

    def OldDemo():
        seed = 1
        for x in range( 0, 20 ):
            for y in range( 0, 20 ):
                sx = ( x * 27 ) - ( y * 27 ) + 550
                sy = ( y * 13 ) + ( x * 13 ) + 50
                seed = ( 73 * seed + 101 ) % 1024
                myimg.render( screen, (sx,sy), 0 + seed % 7 )
#                myimg.render( screen, (sx,sy), 28 )
        pygame.display.flip()
        WaitAMinit()
        pygame.image.save( screen , util.image_dir( "sample.png" ) )


        frame = 0
        while True:
            ev = pygwrap.wait_event()
            if ev.type == pygwrap.TIMEREVENT:
                for x in range( 0, 20 ):
                    for y in range( 0, 20 ):
                        sx = ( x * 27 ) - ( y * 27 ) + 550
                        sy = ( y * 13 ) + ( x * 13 ) + 50
                        myimg.render( screen, (sx,sy), 56 + frame // 10 )
                frame = ( frame + 1 ) % 20
                pygame.display.flip()
            elif ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
                break

    OldDemo()

