import pygame
import image
import weakref
import characters
import math
import pfov

# Enumerated constants for sprite sheets.
SPRITE_GROUND, SPRITE_WALL, SPRITE_BORDER, SPRITE_MISC, SPRITE_DECOR = range( 5 )

class SingTerrain( object ):
    # A singleton terrain class; use these objects as tokens for maps.
    def __init__( self, ident, spritesheet = SPRITE_GROUND, block_vision = False, block_walk = False, block_fly = False, frame = 0 ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.spritesheet = spritesheet
        self.block_vision = block_vision
        self.block_walk = block_walk
        self.block_fly = block_fly
        self.frame = frame
    def render( self, screen, dest, view, data ):
        view.sprites[ self.spritesheet ].render( screen, dest, self.frame )
    def prerender( self, screen, dest, view, data ):
        """Some wall types need a border that gets drawn first."""
        pass
    def get_data( self, view, x, y ):
        """Pre-generate display data for this tile."""
        return None
    def __str__( self ):
        return self.ident
    def __reduce__( self ):
        return self.ident

class GroundTerrain( SingTerrain ):
    # A singleton terrain class; use these objects as tokens for maps.
    def __init__( self, ident, spritesheet = SPRITE_GROUND, block_vision = False, block_walk = False, block_fly = False, frame = 0, edge = None ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.spritesheet = spritesheet
        self.block_vision = block_vision
        self.block_walk = block_walk
        self.block_fly = block_fly
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
    def __init__( self, ident, spritesheet = SPRITE_GROUND, block_vision = False, block_walk = True, block_fly = False, frame = 0 ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.spritesheet = spritesheet
        self.block_vision = block_vision
        self.block_walk = block_walk
        self.block_fly = block_fly
        self.frame = frame
    def get_data( self, view, x, y ):
        """Pre-generate display data for this tile- phase offset."""
        return ( x + y ) % 2
    def render( self, screen, dest, view, data ):
        view.sprites[ self.spritesheet ].render( screen, dest, self.frame + ( view.phase // 5 + data ) % 2 )

class WallTerrain( SingTerrain ):
    # A singleton terrain class; use these objects as tokens for maps.
    def __init__( self, ident, spritesheet = SPRITE_WALL, block_vision = True, block_walk = True, block_fly = True ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.spritesheet = spritesheet
        self.block_vision = block_vision
        self.block_walk = block_walk
        self.block_fly = block_fly

    def prerender( self, screen, dest, view, data ):
        if data[0] != None:
            view.sprites[ SPRITE_BORDER ].render( screen, dest, data[0] )
    def render( self, screen, dest, view, data ):
        if data[1] != None:
            view.sprites[ self.spritesheet ].render( screen, dest, data[1] )
    def get_data( self, view, x, y ):
        """Pre-generate display data for this tile- border frame, wall frame."""
        bor = view.calc_border_score( x, y )
        if bor == -1:
            bor = None
        if bor == 14:
            wal = None
        else:
            wal = view.calc_wall_score( x, y )

        return (bor,wal)

class DoorTerrain( WallTerrain ):
    # A singleton terrain class; use these objects as tokens for maps.
    def __init__( self, ident, spritesheet = SPRITE_WALL, block_vision = True, block_walk = True, block_fly = True, frame=0 ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.spritesheet = spritesheet
        self.block_vision = block_vision
        self.block_walk = block_walk
        self.block_fly = block_fly
        self.frame = frame
    def render( self, screen, dest, view, data ):
        if data[1] != None:
            view.sprites[ self.spritesheet ].render( screen, dest, self.frame + data[1] )
    def get_data( self, view, x, y ):
        """Pre-generate display data for this tile- border frame, wall frame."""
        bor = view.calc_border_score( x, y )
        if bor == -1:
            bor = None
        if view.space_to_south( x, y ):
            wal = 1
        else:
            wal = 0

        return (bor,wal)

class OnTheWallTerrain( SingTerrain ):
    def __init__( self, ident, spritesheet = SPRITE_DECOR, block_vision = False, block_walk = False, block_fly = False, frame = 0 ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.spritesheet = spritesheet
        self.block_vision = block_vision
        self.block_walk = block_walk
        self.block_fly = block_fly
        self.frame = frame
    def render( self, screen, dest, view, data ):
        view.sprites[ self.spritesheet ].render( screen, dest, self.frame + data )
    def get_data( self, view, x, y ):
        """Pre-generate display data for this tile- facing offset."""
        if view.space_to_south( x, y ):
            return 1
        else:
            return 0

# GROUND TYPES
WATER = WaterTerrain( "WATER", frame = 56 )
LOGROUND = GroundTerrain( "LOGROUND", frame = 28, edge = WATER )
HIGROUND = GroundTerrain( "HIGROUND", edge = LOGROUND )

# WALL TYPES
BASIC_WALL = WallTerrain( "BASIC_WALL" )
CLOSED_DOOR = DoorTerrain( "CLOSED_DOOR", frame = 15 )
OPEN_DOOR = DoorTerrain( "OPEN_DOOR", block_vision = False, block_walk = False, block_fly = False, frame = 17 )
FAKE_OPEN_DOOR = DoorTerrain( "FAKE_OPEN_DOOR", frame = 17 )
STAIRS_UP = DoorTerrain( "STAIRS_UP", frame = 19 )
STAIRS_DOWN = DoorTerrain( "STAIRS_DOWN", frame = 21 )
MOUNTAIN_TOP = SingTerrain( "MOUNTAIN_TOP", block_walk = True, frame = 59 )
MOUNTAIN_LEFT = SingTerrain( "MOUNTAIN_LEFT", block_walk = True, frame = 60 )
MOUNTAIN_RIGHT = SingTerrain( "MOUNTAIN_RIGHT", block_walk = True, frame = 61 )
MOUNTAIN_BOTTOM = SingTerrain( "MOUNTAIN_BOTTOM", block_walk = True, frame = 62 )

# DECOR TYPES
BOOKSHELF = OnTheWallTerrain( "BOOKSHELF", frame = 13 )
PUDDLE = SingTerrain( "PUDDLE", frame = 58 )
SKULL = SingTerrain( "SKULL", spritesheet = SPRITE_DECOR, frame = 0 )
BONE = SingTerrain( "BONE", spritesheet = SPRITE_DECOR, frame = 1 )
SKELETON = SingTerrain( "SKELETON", spritesheet = SPRITE_DECOR, frame = 2 )
HANGING_SKELETON = OnTheWallTerrain( "HANGING_SKELETON", frame = 3 )



class Tile( object ):
    def __init__(self, floor=LOGROUND, wall=None, decor=None, visible=False):
        self.floor = floor
        self.wall = wall
        self.decor = decor
        self.visible = visible

    def blocks_vision( self ):
        return ( self.floor and self.floor.block_vision ) or (self.wall and self.wall.block_vision ) or ( self.decor and self.decor.block_vision )

    def blocks_walking( self ):
        return ( self.floor and self.floor.block_walk ) or (self.wall and self.wall.block_walk ) or ( self.decor and self.decor.block_walk )

DEFAULT_SPRITES = { SPRITE_GROUND: "terrain_ground_forest.png", \
    SPRITE_WALL: "terrain_wall_lightbrick.png", \
    SPRITE_BORDER: "terrain_border.png", \
    SPRITE_MISC: "", \
    SPRITE_DECOR: "terrain_decor.png" }

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
        """Safely return floor of tile x,y, or None if off map."""
        if self.on_the_map(x,y):
            return self.map[x][y].floor
        else:
            return None

    def get_wall( self, x, y ):
        """Safely return wall of tile x,y, or None if off map."""
        if self.on_the_map(x,y):
            return self.map[x][y].wall
        else:
            return None

    def tile_blocks_vision( self, x, y ):
        if self.on_the_map(x,y):
            return self.map[x][y].blocks_vision()
        else:
            return True

    def validate_terrain( self ):
        """Make sure that HIGROUND never touches water."""
        for x in range( self.width ):
            for y in range( self.height ):
                if self.get_floor(x,y) == HIGROUND:
                    for dx,dy in self.DELTA8:
                        if self.get_floor(x+dx,y+dy) == WATER:
                            self.map[x][y].floor = LOGROUND
                            break

    def get_character_at_spot( self, pos ):
        """Find and return first character at given position."""
        npc = None
        for m in self.contents:
            if isinstance( m , characters.Character ) and m.pos == pos and m.is_alive():
                npc = m
                break
        return npc

    def range( self, pos1, pos2 ):
        return math.sqrt( ( pos1[0]-pos2[0] )**2 + ( pos1[1]-pos2[1] )**2 )

    def update_pc_position( self, pc ):
        pfov.PCPointOfView( self, pc.pos[0], pc.pos[1], 10 )


OVERLAY_ITEM = 0
OVERLAY_CURSOR = 1
OVERLAY_ATTACK = 2
OVERLAY_MOVETILE = 3
OVERLAY_AOE = 4
OVERLAY_CURRENTCHARA = 5

SCROLL_STEP = 12

class SceneView( object ):
    def __init__( self, scene ):
        self.sprites = dict()
        for k,v in scene.sprites.iteritems():
            self.sprites[k] = image.Image( v, 54, 54 )
        self.extrasprite = image.Image( "sceneview_extras.png", 54, 54 )
        self.overlays = dict()
        self.anims = dict()

        self.modelmap = dict()
        self.modelsprite = weakref.WeakKeyDictionary()

        self.scene = scene
        self.seed = 1
        self.x_off = 600
        self.y_off = -200
        self.phase = 0

        self.mouse_tile = (-1,-1)

        self.map = []
        for x in range( scene.width ):
            self.map.append( [] )
            for y in range( scene.height ):
                self.map[x].append( Tile() )

                if scene.map[x][y].floor:
                    self.map[x][y].floor = scene.map[x][y].floor.get_data( self, x, y )
                if scene.map[x][y].wall:
                    self.map[x][y].wall = scene.map[x][y].wall.get_data( self, x, y )
                if scene.map[x][y].decor:
                    self.map[x][y].decor = scene.map[x][y].decor.get_data( self, x, y )


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

    def calc_wall_score( self, x, y ):
        """Return bitmask of visible connected walls at x,y."""
        it = -1
        if isinstance(self.scene.get_wall( x , y - 1 ),WallTerrain) and \
         not ( self.scene.tile_blocks_vision( x-1 , y -1 ) and self.scene.tile_blocks_vision( x - 1 , y ) \
         and self.scene.tile_blocks_vision( x + 1 , y - 1 ) and self.scene.tile_blocks_vision( x + 1 , y ) ):
            it += 1
        if isinstance(self.scene.get_wall( x+1 , y ),WallTerrain) and \
         not ( self.scene.tile_blocks_vision( x+1 , y -1 ) and self.scene.tile_blocks_vision( x , y-1 ) \
         and self.scene.tile_blocks_vision( x + 1 , y + 1 ) and self.scene.tile_blocks_vision( x , y+1 ) ):
            it += 2
        if isinstance(self.scene.get_wall( x , y + 1 ),WallTerrain) and \
         not ( self.scene.tile_blocks_vision( x-1 , y +1 ) and self.scene.tile_blocks_vision( x - 1 , y ) \
         and self.scene.tile_blocks_vision( x + 1 , y + 1 ) and self.scene.tile_blocks_vision( x + 1 , y ) ):
            it += 4
        if isinstance(self.scene.get_wall( x-1 , y ),WallTerrain) and \
         not ( self.scene.tile_blocks_vision( x-1 , y -1 ) and self.scene.tile_blocks_vision( x , y-1 ) \
         and self.scene.tile_blocks_vision( x - 1 , y + 1 ) and self.scene.tile_blocks_vision( x , y+1 ) ):
            it += 8

        if it == -1:
            it = 14
        return it

    def is_border_wall( self, x, y ):
        """Return True if this loc is a wall or off the map."""
        return isinstance(self.scene.get_wall( x , y ),WallTerrain ) or not self.scene.on_the_map( x,y )

    def calc_border_score( self, x, y ):
        """Return the wall border frame for this tile."""
        it = -1
        if self.is_border_wall( x-1 , y-1 ) and self.is_border_wall( x-1 , y ) and self.is_border_wall( x , y-1 ):
            it += 1
        if self.is_border_wall( x+1 , y-1 ) and self.is_border_wall( x+1 , y ) and self.is_border_wall( x , y-1 ):
            it += 2
        if self.is_border_wall( x+1 , y+1 ) and self.is_border_wall( x+1 , y ) and self.is_border_wall( x , y+1 ):
            it += 4
        if self.is_border_wall( x-1 , y+1 ) and self.is_border_wall( x-1 , y ) and self.is_border_wall( x , y+1 ):
            it += 8
        return it

    def space_to_south( self, x, y ):
        """Return True if no wall in tile to south."""
        return not self.scene.get_wall( x , y + 1 )

    def get_pseudo_random( self ):
        self.seed = ( 73 * self.seed + 101 ) % 1024
        return self.seed

    # Half tile width and half tile height
    HTW = 27
    HTH = 13

    def relative_x( self, x, y ):
        """Return the relative x position of this tile, ignoring offset."""
        return ( x * self.HTW ) - ( y * self.HTW )

    def relative_y( self, x, y ):
        """Return the relative y position of this tile, ignoring offset."""
        return ( y * self.HTH ) + ( x * self.HTH )

    def map_x( self, sx, sy ):
        """Return the map x column for the given screen coordinates."""
        return ( ( sx - self.x_off ) / self.HTW + ( sy - self.y_off ) / self.HTH ) // 2

    def map_y( self, sx, sy ):
        """Return the map y row for the given screen coordinates."""
        return ( ( sy - self.y_off ) / self.HTH - ( sx - self.x_off ) / self.HTW ) // 2

    def check_origin( self ):
        """Make sure the offset point is within map boundaries."""
        if -self.x_off < self.relative_x( 0 , self.scene.height-1 ):
            self.x_off = -self.relative_x( 0 , self.scene.height-1 )
        elif -self.x_off > self.relative_x( self.scene.width-1 , 0 ):
            self.x_off = -self.relative_x( self.scene.width-1 , 0 )
        if -self.y_off < self.relative_y( 0 , 0 ):
            self.y_off = -self.relative_y( 0 , 0 )
        elif -self.y_off > self.relative_y( self.scene.width-1 , self.scene.height-1 ):
            self.y_off = -self.relative_y(  self.scene.width-1 , self.scene.height-1  )

    def focus( self, screen, x, y ):
        self.x_off = screen.get_width()//2 - self.relative_x( x,y )
        self.y_off = screen.get_height()//2 - self.relative_y( x,y )
        self.check_origin()

    def regenerate_avatars( self, models ):
        """Regenerate the avatars for the listed models."""
        for m in models:
            self.modelsprite[ m ] = m.generate_avatar()

    def __call__( self , screen ):
        """Draws this mapview to the provided screen."""
        screen_area = screen.get_rect()
        mouse_x,mouse_y = pygame.mouse.get_pos()
        screen.fill( (0,0,0) )

        # Check for map scrolling, depending on mouse position.
        if mouse_x < 20:
            self.x_off += SCROLL_STEP
            self.check_origin()
        elif mouse_x > ( screen_area.right - 20 ):
            self.x_off -= SCROLL_STEP
            self.check_origin()
        if mouse_y < 20:
            self.y_off += SCROLL_STEP
            self.check_origin()
        elif mouse_y > ( screen_area.bottom - 20 ):
            self.y_off -= SCROLL_STEP
            self.check_origin()


        # Fill the modelmap and itemmap.
        self.modelmap.clear()
        itemmap = dict()
        for m in self.scene.contents:
            if isinstance( m , characters.Character ) and m.is_alive():
                self.modelmap[ tuple( m.pos ) ] = m
            else:
                itemmap[ tuple( m.pos ) ] = True

        x_min = self.map_x( *screen_area.topleft ) - 1
        x_max = self.map_x( *screen_area.bottomright )
        y_min = self.map_y( *screen_area.topright ) - 1
        y_max = self.map_y( *screen_area.bottomleft )

        tile_x,tile_y = self.mouse_tile

        dest = pygame.Rect( 0, 0, 54, 54 )

        for x in range( x_min, x_max + 1 ):
            for y in range( y_min, y_max + 1 ):
                sx = self.relative_x( x, y ) + self.x_off
                sy = self.relative_y( x, y ) + self.y_off
                dest.topleft = (sx,sy)

                # Check the mouse position.
                if ( mouse_x >= sx ) and ( mouse_x < ( sx + 54 ) ) and ( mouse_y >= ( sy + 41 ) ) and ( mouse_y < ( sy + 54 ) ):
                    # If it's in the lower left triangle, it's one tile south.
                    # If it's in the lower right triangle, it's one tile east.
                    # Otherwise it's right here.
                    if mouse_y > ( sy + 41 + ( mouse_x - sx ) // 2 ):
                        tile_x = x
                        tile_y = y+1
                    elif mouse_y > ( sy + 67 - ( mouse_x - sx ) // 2 ):
                        tile_x = x + 1
                        tile_y = y
                    else:
                        tile_x = x
                        tile_y = y

                if self.scene.on_the_map( x , y ) and self.scene.map[x][y].visible and screen_area.colliderect( dest ):
                    if self.scene.map[x][y].floor:
                        self.scene.map[x][y].floor.render( screen, dest, self, self.map[x][y].floor )

                    if self.scene.map[x][y].wall:
                        self.scene.map[x][y].wall.prerender( screen, dest, self, self.map[x][y].wall )

                    # Print overlay in between the wall border and the wall proper.
                    if self.overlays.get( (x,y) , None ):
                        self.extrasprite.render( screen, dest, self.overlays[(x,y)] )

                    if self.scene.map[x][y].wall:
                        self.scene.map[x][y].wall.render( screen, dest, self, self.map[x][y].wall )

                    if self.scene.map[x][y].decor:
                        self.scene.map[x][y].decor.render( screen, dest, self, self.map[x][y].decor )

                    if itemmap.get( (x,y), False ):
                        self.extrasprite.render( screen, dest, OVERLAY_ITEM )


                    m = self.modelmap.get( (x,y) , None )
                    if m:
                        msprite = self.modelsprite.get( m , None )
                        if not msprite:
                            msprite = m.generate_avatar()
                            self.modelsprite[ m ] = msprite
                        msprite.render( screen, dest, m.FRAME )

                    m = self.anims.get( (x,y) , None )
                    if m:
                        m.render( self, screen, dest )


        self.phase = ( self.phase + 1 ) % 600
        self.mouse_tile = ( tile_x, tile_y )


