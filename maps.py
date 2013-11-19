import pygame
import image

GROUND1, GROUND2, WATER = range( 3 )

class Tile( object ):
    def __init__(self, floor=GROUND2, wall=None, decor=None, visible=False):
        self.floor = floor
        self.wall = wall
        self.decor = decor
        self.visible = visible


class Scene( object ):
    DELTA8 = ( (-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1) )
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

    def get_floor( self, x, y ):
        if self.on_the_map(x,y):
            return self.map[x][y].floor
        else:
            return None

    def check_floors( self ):
        """Make sure that GROUND1 never touches water."""
        for x in range( self.width ):
            for y in range( self.height ):
                if self.get_floor(x,y) == GROUND1:
                    for dx,dy in self.DELTA8:
                        if self.get_floor(x+dx,y+dy) == WATER:
                            self.map[x][y].floor = GROUND2
                            break

class SceneView( object ):
    def __init__( self, scene ):
        self.ground_gfx = image.Image( "terrain_ground_forest.png", 54, 54 )
        self.scene = scene
        self.seed = 1
        self.x_off = 550
        self.y_off = 50

        self.map = []
        for x in range( scene.width ):
            self.map.append( [] )
            for y in range( scene.height ):
                self.map[x].append( [] )

                if scene.map[x][y].floor == GROUND1:
                    n = self.calc_floor_score( x , y , GROUND2 )
                    if n > 0:
                        self.map[x][y].append( ( self.ground_gfx , 6 + n ) )
                    else:
                        self.map[x][y].append( ( self.ground_gfx , self.get_pseudo_random() % 7 ) )
                elif scene.map[x][y].floor == GROUND2:
                    n = self.calc_floor_score( x , y , WATER )
                    if n > 0:
                        self.map[x][y].append( ( self.ground_gfx , 34 + n ) )
                    else:
                        self.map[x][y].append( ( self.ground_gfx , 28 + self.get_pseudo_random() % 7 ) )
                elif scene.map[x][y].floor == WATER:
                    self.map[x][y].append( ( self.ground_gfx , 56 ) )


    def calc_floor_score( self, x, y, terr ):
        """Return bitmask of how many floors of type terrain border tile x,y."""
        it = 0
        if ( self.scene.get_floor( x - 1 , y - 1 ) == terr ) or \
          ( self.scene.get_floor( x , y - 1 ) == terr ) or \
          ( self.scene.get_floor( x - 1 , y ) == terr ):
            it += 1
        if ( self.scene.get_floor( x + 1 , y - 1 ) == terr ) or \
          ( self.scene.get_floor( x , y - 1 ) == terr ) or \
          ( self.scene.get_floor( x + 1 , y ) == terr ):
            it += 2
        if ( self.scene.get_floor( x + 1 , y + 1 ) == terr ) or \
          ( self.scene.get_floor( x , y + 1 ) == terr ) or \
          ( self.scene.get_floor( x + 1 , y ) == terr ):
            it += 4
        if ( self.scene.get_floor( x - 1 , y + 1 ) == terr ) or \
          ( self.scene.get_floor( x , y + 1 ) == terr ) or \
          ( self.scene.get_floor( x - 1 , y ) == terr ):
            it += 8
        return it

    def get_pseudo_random( self ):
        self.seed = ( 73 * self.seed + 101 ) % 1024
        return self.seed

    def __call__( self , screen ):
        for x in range( self.scene.width ):
            for y in range( self.scene.height ):
                sx = ( x * 27 ) - ( y * 27 ) + self.x_off
                sy = ( y * 13 ) + ( x * 13 ) + self.y_off
                for sprite,frame in self.map[x][y]:
                    sprite.render( screen, (sx,sy), frame )


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
                myimg.render( screen, (sx,sy), 28 + seed % 7 )
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

    myscene = Scene( 30 , 30 )
    terrain_list = (GROUND1, GROUND1, GROUND1, GROUND1, GROUND1, GROUND1, GROUND1, GROUND1, GROUND1, GROUND1, GROUND1, GROUND1, GROUND2, GROUND2, WATER )
    for x in range( myscene.width ):
        for y in range( myscene.height ):
            myscene.map[x][y].floor = random.choice( terrain_list )
    myscene.check_floors()
    mysceneview = SceneView( myscene )
    mysceneview( screen )
    pygame.display.flip()
    WaitAMinit()


