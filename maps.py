import pygame
import image

# Enumerated constants for sprite sheets.
SPRITE_GROUND, SPRITE_WALL, SPRITE_MISC, SPRITE_DECOR = range( 4 )

class SingTerrain( object ):
    # A singleton terrain class; use these objects as tokens for maps.
    def __init__( self, ident, spritesheet = SPRITE_GROUND, frame = 0 ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.spritesheet = spritesheet
        self.frame = frame
    def render( self, screen, dest, view, data ):
        view.sprites[ self.spritesheet ].render( screen, dest, self.frame )
    def get_data( self, view, x, y ):
        """Pre-generate display data for this tile."""
        return None
    def __str__( self ):
        return self.ident
    def __reduce__( self ):
        return self.ident

class GroundTerrain( SingTerrain ):
    # A singleton terrain class; use these objects as tokens for maps.
    def __init__( self, ident, spritesheet = SPRITE_GROUND, frame = 0, edge = None ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.spritesheet = spritesheet
        self.frame = frame
        self.edge = edge
    def render( self, screen, dest, view, data ):
        view.sprites[ self.spritesheet ].render( screen, dest, self.frame + data )
    def get_data( self, view, x, y ):
        """Pre-generate display data for this tile- frame offset."""
        n = view.calc_floor_score( x , y , self.edge )
        if n > 0:
            n += 6
        else:
            n = view.get_pseudo_random() % 7
        return n

class WaterTerrain( SingTerrain ):
    # A singleton terrain class; use these objects as tokens for maps.
    def __init__( self, ident, spritesheet = SPRITE_GROUND, frame = 0 ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.spritesheet = spritesheet
        self.frame = frame
    def render( self, screen, dest, view, data ):
        view.sprites[ self.spritesheet ].render( screen, dest, self.frame + ( view.phase // 10 ) % 2 )


WATER = WaterTerrain( "WATER", frame = 56 )
LOGROUND = GroundTerrain( "LOGROUND", frame = 28, edge = WATER )
HIGROUND = GroundTerrain( "HIGROUND", edge = LOGROUND )


class Tile( object ):
    def __init__(self, floor=LOGROUND, wall=None, decor=None, visible=False):
        self.floor = floor
        self.wall = wall
        self.decor = decor
        self.visible = visible

DEFAULT_SPRITES = { SPRITE_GROUND: "terrain_ground_forest.png", SPRITE_WALL: "", SPRITE_MISC: "", SPRITE_DECOR: "" }

class Scene( object ):
    DELTA8 = ( (-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1) )
    def __init__(self,width=128,height=128,sprites=None):
        self.width = width
        self.height = height
        self.contents = []
        self.sprites = DEFAULT_SPRITES.copy()
        if sprites:
            self.sprites.update( sprites )
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
        """Make sure that HIGROUND never touches water."""
        for x in range( self.width ):
            for y in range( self.height ):
                if self.get_floor(x,y) == HIGROUND:
                    for dx,dy in self.DELTA8:
                        if self.get_floor(x+dx,y+dy) == WATER:
                            self.map[x][y].floor = LOGROUND
                            break

class SceneView( object ):
    def __init__( self, scene ):
        self.sprites = dict()
        for k,v in scene.sprites.iteritems():
            self.sprites[k] = image.Image( v, 54, 54 )

        self.scene = scene
        self.seed = 1
        self.x_off = 550
        self.y_off = 50
        self.phase = 0

        self.map = []
        for x in range( scene.width ):
            self.map.append( [] )
            for y in range( scene.height ):
                self.map[x].append( Tile() )

                if scene.map[x][y].floor:
                    self.map[x][y].floor = scene.map[x][y].floor.get_data( self, x, y )


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
                dest = pygame.Rect( sx, sy, 54, 54 )

                if self.scene.map[x][y].floor:
                    self.scene.map[x][y].floor.render( screen, dest, self, self.map[x][y].floor )
        self.phase = ( self.phase + 1 ) % 600

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

    myscene = Scene( 30 , 30 )
    terrain_list = (HIGROUND, HIGROUND, HIGROUND, HIGROUND, HIGROUND, HIGROUND, HIGROUND, HIGROUND, HIGROUND, HIGROUND, HIGROUND, HIGROUND, LOGROUND, LOGROUND, WATER )
    for x in range( myscene.width ):
        for y in range( myscene.height ):
            myscene.map[x][y].floor = random.choice( terrain_list )
    myscene.check_floors()
    mysceneview = SceneView( myscene )

    while True:
        ev = pygwrap.wait_event()
        if ev.type == pygwrap.TIMEREVENT:
            mysceneview( screen )
            pygame.display.flip()
        elif ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
            break


