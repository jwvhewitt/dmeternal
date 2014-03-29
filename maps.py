import pygame
import image
import weakref
import characters
import math
import pfov
import collections
import pygwrap
import enchantments
import items
import context
import random
import monsters
import container

# Enumerated constants for sprite sheets.
SPRITE_GROUND, SPRITE_WALL, SPRITE_BORDER, SPRITE_INTERIOR, SPRITE_FLOOR, \
 SPRITE_DECOR, SPRITE_CHEST, SPRITE_SIGNS = range( 8 )

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
    def place( self, scene, pos ):
        if scene.on_the_map( *pos ):
            scene.map[pos[0]][pos[1]].decor = self
    def __str__( self ):
        return self.ident
    def __reduce__( self ):
        return self.ident

class VariableTerrain( SingTerrain ):
    def __init__( self, ident, spritesheet = SPRITE_FLOOR, block_vision = False, block_walk = False, block_fly = False, frames = (0,1,) ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.spritesheet = spritesheet
        self.block_vision = block_vision
        self.block_walk = block_walk
        self.block_fly = block_fly
        self.frames = frames
    def render( self, screen, dest, view, data ):
        view.sprites[ self.spritesheet ].render( screen, dest, self.frames[ data ] )
    def get_data( self, view, x, y ):
        """Pre-generate display data for this tile."""
        return view.get_pseudo_random() % len(self.frames)


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

class OnTheWallVariable( SingTerrain ):
    def __init__( self, ident, spritesheet = SPRITE_DECOR, block_vision = False, block_walk = False, block_fly = False, frames = (0,1) ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.spritesheet = spritesheet
        self.block_vision = block_vision
        self.block_walk = block_walk
        self.block_fly = block_fly
        self.frames = frames
    def render( self, screen, dest, view, data ):
        view.sprites[ self.spritesheet ].render( screen, dest, data )
    def get_data( self, view, x, y ):
        """Pre-generate display data for this tile- facing offset."""
        if view.space_to_south( x, y ):
            return self.frames[ view.get_pseudo_random() % len( self.frames ) ] + 1
        else:
            return self.frames[ view.get_pseudo_random() % len( self.frames ) ]

class BedHeadTerrain( SingTerrain ):
    def __init__( self, ident, spritesheet = SPRITE_INTERIOR, block_vision = False, block_walk = False, block_fly = False, frame = 0, partner=None ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.spritesheet = spritesheet
        self.block_vision = block_vision
        self.block_walk = block_walk
        self.block_fly = block_fly
        self.frame = frame
        self.partner = partner
    def render( self, screen, dest, view, data ):
        view.sprites[ self.spritesheet ].render( screen, dest, self.frame + data )
    def get_data( self, view, x, y ):
        """Pre-generate display data for this tile- facing offset."""
        if view.scene.get_decor( x, y+1 ) == self.partner:
            return 1
        else:
            return 0

class BedFootTerrain( SingTerrain ):
    def __init__( self, ident, spritesheet = SPRITE_INTERIOR, block_vision = False, block_walk = False, block_fly = False, frame = 0, partner=None ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.spritesheet = spritesheet
        self.block_vision = block_vision
        self.block_walk = block_walk
        self.block_fly = block_fly
        self.frame = frame
        self.partner = partner
    def render( self, screen, dest, view, data ):
        view.sprites[ self.spritesheet ].render( screen, dest, self.frame + data )
    def get_data( self, view, x, y ):
        """Pre-generate display data for this tile- facing offset."""
        if view.scene.get_decor( x, y-1 ) == self.partner:
            return 1
        else:
            return 0

class CrowdTerrain( SingTerrain ):
    def __init__( self, ident, spritesheet = SPRITE_GROUND, block_vision = False, block_walk = True, block_fly = True, inner_frames = (0,1), outer_frames=(2,3) ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.spritesheet = spritesheet
        self.block_vision = block_vision
        self.block_walk = block_walk
        self.block_fly = block_fly
        self.inner_frames = inner_frames
        self.outer_frames = outer_frames
    def render( self, screen, dest, view, data ):
        view.sprites[ self.spritesheet ].render( screen, dest, data )
    def get_data( self, view, x, y ):
        """Pre-generate display data for this tile- facing offset."""
        if view.space_nearby( x, y ):
            return self.outer_frames[ view.get_pseudo_random() % len(self.outer_frames) ]
        else:
            return self.inner_frames[ view.get_pseudo_random() % len(self.inner_frames) ]

# GROUND TYPES
WATER = WaterTerrain( "WATER", frame = 56 )
LOGROUND = GroundTerrain( "LOGROUND", frame = 28, edge = WATER )
HIGROUND = GroundTerrain( "HIGROUND", edge = LOGROUND )
BASIC_FLOOR = VariableTerrain( "BASIC_FLOOR", frames=(0,1,2,3,4,5) )

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
SPIRAL_STAIRS_UP = SingTerrain( "SPIRAL_STAIRS_UP", block_walk = True, spritesheet=SPRITE_INTERIOR, frame=0 )
SPIRAL_STAIRS_DOWN = SingTerrain( "SPIRAL_STAIRS_DOWN", block_walk = True, spritesheet=SPRITE_INTERIOR, frame=1 )
ROCKS = VariableTerrain( "ROCKS", spritesheet = SPRITE_GROUND, block_walk=True, frames = (23,24,25,26,27) )
TREES = CrowdTerrain( "TREES", inner_frames = (51,52,53,54,55), outer_frames = (63,64,65,66,67,68,69) )

# DECOR TYPES
PUDDLE = SingTerrain( "PUDDLE", frame = 58 )

SKULL = SingTerrain( "SKULL", spritesheet = SPRITE_DECOR, frame = 0 )
BONE = SingTerrain( "BONE", spritesheet = SPRITE_DECOR, frame = 1 )
SKELETON = SingTerrain( "SKELETON", spritesheet = SPRITE_DECOR, frame = 2 )
HANGING_SKELETON = OnTheWallTerrain( "HANGING_SKELETON", frame = 3 )
PORTRAIT = OnTheWallTerrain( "PORTRAIT", frame = 5 )
SUN_PICTURE = OnTheWallTerrain( "SUN_PICTURE", frame = 7 )
MOON_PICTURE = OnTheWallTerrain( "MOON_PICTURE", frame = 9 )
LANDSCAPE_PICTURE = OnTheWallTerrain( "LANDSCAPE_PICTURE", frame = 11 )
BOOKSHELF = OnTheWallTerrain( "BOOKSHELF", frame = 13, block_walk=True )
MESSAGE_SIGN = OnTheWallTerrain( "MESSAGE_SIGN", frame = 15 )
FIREPLACE = OnTheWallTerrain( "HANGING_SKELETON", frame = 17 )
SWITCH_UP = OnTheWallTerrain( "SWITCH_UP", frame = 19 )
SWITCH_DOWN = OnTheWallTerrain( "SWITCH_DOWN", frame = 21 )
KEG = SingTerrain( "KEG", spritesheet = SPRITE_DECOR, frame = 23, block_walk = True )
SMALL_WINDOW = OnTheWallTerrain( "SMALL_WINDOW", frame = 24 )
BRIGHT_WINDOW = OnTheWallTerrain( "BRIGHT_WINDOW", frame = 26 )
DARK_WINDOW = OnTheWallTerrain( "DARK_WINDOW", frame = 28 )
CASTLE_WINDOW = OnTheWallTerrain( "CASTLE_WINDOW", frame = 30 )
STAINED_GLASS = OnTheWallTerrain( "STAINED_GLASS", frame = 32 )
WALL_CRATES = OnTheWallVariable( "WALL_CRATES", frames = (34,36) )
CURTAIN = OnTheWallTerrain( "CURTAIN", frame = 38 )
WALL_WEAPON_RACK = OnTheWallVariable( "WALL_WEAPON_RACK", frames = (40,42,44,46,48,50,52) )
WELL = SingTerrain( "WELL", spritesheet = SPRITE_DECOR, frame = 54, block_walk=True )
CART = SingTerrain( "CART", spritesheet = SPRITE_DECOR, frame = 55, block_walk=True )
PROVISIONS = OnTheWallVariable( "PROVISIONS", frames = (56,58,60) )
HIGH_SHELF = OnTheWallVariable( "HIGH_SHELF", frames = (62,64) )
ANVIL = SingTerrain( "ANVIL", spritesheet = SPRITE_DECOR, frame = 66, block_walk=True )
DESK = SingTerrain( "DESK", spritesheet = SPRITE_DECOR, frame = 67, block_walk=True )
FORGE = WaterTerrain( "FORGE", frame = 68, spritesheet = SPRITE_DECOR )
BIG_SHELF = OnTheWallVariable( "BIG_SHELF", frames = (70,72,74) )
PILED_GOODS = VariableTerrain( "PILED_GOODS", spritesheet = SPRITE_DECOR, block_walk=True, frames = (76,77,78) )
FOUNTAIN = SingTerrain( "FOUNTAIN", spritesheet = SPRITE_DECOR, frame = 79, block_walk=True )
MINE_ENTRANCE = SingTerrain( "MINE_ENTRANCE", spritesheet = SPRITE_DECOR, frame = 80, block_walk=True )
DUNGEON_ENTRANCE = SingTerrain( "DUNGEON_ENTRANCE", spritesheet = SPRITE_DECOR, frame = 81, block_walk=True )
CRYPT_ENTRANCE = SingTerrain( "CRYPT_ENTRANCE", spritesheet = SPRITE_DECOR, frame = 82, block_walk=True )
RUIN_ENTRANCE = SingTerrain( "RUIN_ENTRANCE", spritesheet = SPRITE_DECOR, frame = 83, block_walk=True )
SECRET_ENTRANCE = SingTerrain( "SECRET_ENTRANCE", spritesheet = SPRITE_DECOR, frame = 84, block_walk=True )
FLOOR_BLOOD = VariableTerrain( "FLOOR_BLOOD", spritesheet = SPRITE_DECOR, block_walk=False, frames = (85,86,87,88,89) )

BED_HEAD = BedHeadTerrain( "BED_HEAD", block_walk=True, frame=2 )
BED_FOOT = BedFootTerrain( "BED_FOOT", block_walk=True, frame=4, partner=BED_HEAD )
BED_HEAD.partner = BED_FOOT

DRESSER = OnTheWallTerrain( "DRESSER", block_walk=True, spritesheet=SPRITE_INTERIOR, frame = 6 )
BENCH = OnTheWallTerrain( "BENCH", block_walk=True, spritesheet=SPRITE_INTERIOR, frame = 8 )
TABLE = SingTerrain( "TABLE", block_walk=True, spritesheet=SPRITE_INTERIOR, frame = 10 )
ANKH_ALTAR = SingTerrain( "ANKH_ALTAR", block_walk=True, spritesheet=SPRITE_INTERIOR, frame = 11 )
CANDLE_ALTAR = SingTerrain( "CANDLE_ALTAR", block_walk=True, spritesheet=SPRITE_INTERIOR, frame = 12 )
SKULL_ALTAR = SingTerrain( "SKULL_ALTAR", block_walk=True, spritesheet=SPRITE_INTERIOR, frame = 13 )
LIGHT_STAND = SingTerrain( "CANDLE_STAND", block_walk=True, spritesheet=SPRITE_INTERIOR, frame = 14 )
COLUMN = OnTheWallTerrain( "COLUMN", block_walk=True, spritesheet=SPRITE_INTERIOR, frame = 15 )
WALL_LIGHT = OnTheWallTerrain( "WALL_LIGHT", block_walk=True, spritesheet=SPRITE_INTERIOR, frame = 17 )

SWORD_SIGN = OnTheWallTerrain( "SWORD_SIGN", spritesheet=SPRITE_SIGNS, frame = 0 )
ANKH_SIGN = OnTheWallTerrain( "ANKH_SIGN", spritesheet=SPRITE_SIGNS, frame = 2 )
BOOK_SIGN = OnTheWallTerrain( "BOOK_SIGN", spritesheet=SPRITE_SIGNS, frame = 4 )
DRINK_SIGN = OnTheWallTerrain( "DRINK_SIGN", spritesheet=SPRITE_SIGNS, frame = 6 )
SHIELD_SIGN = OnTheWallTerrain( "SHIELD_SIGN", spritesheet=SPRITE_SIGNS, frame = 8 )
WEAPONS_SIGN = OnTheWallTerrain( "WEAPONS_SIGN", spritesheet=SPRITE_SIGNS, frame = 10 )
POTION_SIGN = OnTheWallTerrain( "POTION_SIGN", spritesheet=SPRITE_SIGNS, frame = 12 )
BOW_SIGN = OnTheWallTerrain( "BOW_SIGN", spritesheet=SPRITE_SIGNS, frame = 14 )
TOWER_SIGN = OnTheWallTerrain( "TOWER_SIGN", spritesheet=SPRITE_SIGNS, frame = 16 )


SMALL_CHEST = VariableTerrain( "SMALL_CHEST", spritesheet = SPRITE_CHEST, frames = (0,1), block_walk=True )
SMALL_CHEST_OPEN = VariableTerrain( "SMALL_CHEST_OPEN", spritesheet = SPRITE_CHEST, frames = (2,3), block_walk=True )
MEDIUM_CHEST = VariableTerrain( "MEDIUM_CHEST", spritesheet = SPRITE_CHEST, frames = (4,5), block_walk=True )
MEDIUM_CHEST_OPEN = VariableTerrain( "MEDIUM_CHEST_OPEN", spritesheet = SPRITE_CHEST, frames = (6,7), block_walk=True )
LARGE_CHEST = VariableTerrain( "LARGE_CHEST", spritesheet = SPRITE_CHEST, frames = (8,9), block_walk=True )
LARGE_CHEST_OPEN = VariableTerrain( "LARGE_CHEST_OPEN", spritesheet = SPRITE_CHEST, frames = (10,11), block_walk=True )


class Tile( object ):
    def __init__(self, floor=LOGROUND, wall=None, decor=None, visible=False):
        self.floor = floor
        self.wall = wall
        self.decor = decor
        self.visible = visible

    def blocks_vision( self ):
        return ( self.floor and self.floor.block_vision ) or (self.wall and self.wall.block_vision ) or ( self.decor and self.decor.block_vision )

    def blocks_walking( self ):
        return ( self.floor and self.floor.block_walk ) or (self.wall and ( self.wall is True or self.wall.block_walk )) or ( self.decor and self.decor.block_walk )

DEFAULT_SPRITES = { SPRITE_GROUND: "terrain_ground_forest.png", \
    SPRITE_WALL: "terrain_wall_lightbrick.png", \
    SPRITE_BORDER: "terrain_border.png", \
    SPRITE_INTERIOR: "terrain_int_default.png", \
    SPRITE_FLOOR: "terrain_floor_gravel.png", \
    SPRITE_DECOR: "terrain_decor.png", \
    SPRITE_CHEST: "terrain_chest_wood.png", \
    SPRITE_SIGNS: "terrain_signs_default.png" }

class Scene( object ):
    DELTA8 = ( (-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1) )
    def __init__(self,width=128,height=128,sprites=None,biome=None,setting=None,desctags=()):
        self.name = ""
        self.width = width
        self.height = height
        self.contents = container.ContainerList(owner=self)
        self.sprites = DEFAULT_SPRITES.copy()
        if sprites:
            self.sprites.update( sprites )
        self.biome=biome
        self.setting=setting
        self.desctags = desctags
        self.scripts = list()
        self.parent_scene = None
        self.in_sight = set()

        self.last_updated = 0
        self.monster_zones = list()

        # Fill the map with empty tiles
        self.map = [[ Tile()
            for y in range(height) ]
                for x in range(width) ]

    def root_scene( self ):
        rs = self
        while rs.parent_scene:
            rs = rs.parent_scene
        return rs

    def on_the_map( self , x , y ):
        # Returns true if on the map, false otherwise
        return ( ( x >= 0 ) and ( x < self.width ) and ( y >= 0 ) and ( y < self.height ) )

    def get_encounter_request( self ):
        # Return the basic encounter request.
        req = dict()
        # Add biome.
        req[ (context.HAB_EVERY,self.biome or context.HAB_EVERY) ] = True
        # Add setting.
        req[ (context.SET_EVERY,self.setting or context.SET_EVERY) ] = True
        # Add optional descriptors.
        if self.biome:
            req[self.biome] = context.MAYBE
        if self.setting:
            req[self.setting] = context.MAYBE
        for t in self.desctags:
            req[t] = context.MAYBE
        return req

    def choose_monster( self, min_rank, max_rank, habitat=None ):
        """Choose a random monster class as close to range as possible."""
        possible_list = list()
        backup_list = list()
        if not habitat:
            habitat = self.get_encounter_request()
        for m in monsters.MONSTER_LIST:
            if m.ENC_LEVEL <= max_rank:
                n = context.matches_description( m.HABITAT, habitat )
                if n:
                    backup_list += (m,) * m.ENC_LEVEL
                    if m.ENC_LEVEL >= min_rank:
                        possible_list += (m,) * max( n * 2 - 3, 1 )
        if possible_list:
            return random.choice( possible_list )
        elif backup_list:
            return random.choice( backup_list )

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

    def get_decor( self, x, y ):
        """Safely return decor of tile x,y, or None if off map."""
        if self.on_the_map(x,y):
            return self.map[x][y].decor
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

    def is_model( self, thing ):
        """Return True if thing is a model which blocks movement through tile."""
        return isinstance( thing , characters.Character )

    def get_character_at_spot( self, pos ):
        """Find and return first character at given position."""
        npc = None
        for m in self.contents:
            if isinstance( m , characters.Character ) and m.pos == pos and m.is_alright():
                npc = m
                break
        return npc

    def get_field_at_spot( self, pos ):
        """Find and return first field at given position."""
        fld = None
        for m in self.contents:
            if m.pos == pos and isinstance( m , enchantments.Field ):
                fld = m
                break
        return fld

    def get_bumpable_at_spot( self, pos ):
        """Find and return first bumpable at given position."""
        bump = None
        for m in self.contents:
            if m.pos == pos and hasattr( m, "bump" ):
                bump = m
                break
        return bump

    def distance( self, pos1, pos2 ):
        return round( math.sqrt( ( pos1[0]-pos2[0] )**2 + ( pos1[1]-pos2[1] )**2 ) )

    def update_party_position( self, party ):
        self.in_sight = set()
        for pc in party:
            if pc.is_alright():
                self.in_sight |= pfov.PCPointOfView( self, pc.pos[0], pc.pos[1], 10 ).tiles

    def find_free_points_in_rect( self, area=None ):
        # Return a list of all points in rect that are unoccupied + unblocked.
        points = list()
        if not area:
            area = pygame.Rect( 0,0,self.width,self.height )
        for x in range( area.x, area.x+area.width ):
            for y in range( area.y, area.y+area.height ):
                if self.on_the_map(x,y) and not self.map[x][y].blocks_walking():
                    points.append( (x,y) )
        for m in self.contents:
            if self.is_model( m ) and m.pos in points:
                points.remove( m.pos )
        return points

    def find_entry_point_in_rect( self, area=None ):
        # Given the provided area, find a tile that is unoccupied + unblocked.
        candidates = self.find_free_points_in_rect( area )
        if candidates:
            return random.choice( candidates )
        else:
            return None

    def monster_zone_is_empty( self, mzone ):
        all_clear = True
        for m in self.contents:
            if isinstance( m , characters.Character ) and mzone.collidepoint( m.pos ):
                all_clear = False
                break
        return all_clear

    def __str__( self ):
        if self.name:
            return self.name
        else:
            return repr( self )

OVERLAY_ITEM = 0
OVERLAY_CURSOR = 1
OVERLAY_ATTACK = 2
OVERLAY_MOVETILE = 3
OVERLAY_AOE = 4
OVERLAY_CURRENTCHARA = 5
OVERLAY_HIDDEN = 6

SCROLL_STEP = 12

class SceneView( object ):
    def __init__( self, scene ):
        self.sprites = dict()
        for k,v in scene.sprites.iteritems():
            self.sprites[k] = image.Image( v, 54, 54 )
        self.extrasprite = image.Image( "sceneview_extras.png", 54, 54 )
        self.overlays = dict()
        self.anims = collections.defaultdict(list)

        self.modelmap = dict()
        self.fieldmap = dict()
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

    def space_nearby( self, x, y ):
        """Return True if a tile without a wall is adjacent."""
        found_space = False
        for d in self.scene.DELTA8:
            if not self.scene.get_wall( x + d[0], y + d[1] ):
                found_space = True
                break
        return found_space

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

    def draw_caption( self, screen, center, txt ):
        myimage = pygwrap.TINYFONT.render( txt, True, (240,240,240) )
        mydest = myimage.get_rect(center=center)
        myfill = pygame.Rect( mydest.x - 2, mydest.y - 1, mydest.width + 4, mydest.height + 2 )
        screen.fill( (36,37,36), myfill )
        screen.blit( myimage, mydest )

    def quick_model_status( self, screen, dest, model ):
        # Do a quick model status for this model.
        self.draw_caption( screen, (dest.centerx,dest.y-8), str( model ) )

        box = pygame.Rect( dest.x + 7, dest.y , 40, 3 )
        screen.fill( ( 250, 0, 0, 200 ), box )
        hp = model.max_hp()
        hpd = min( model.hp_damage, hp )
        if hp > 0:
            box.x += box.w - ( hpd * box.w ) // hp
            box.w = dest.x + 7 + box.w - box.x
            screen.fill( (120, 0, 0, 100), box )

        box = pygame.Rect( dest.x + 7, dest.y + 4 , 40, 3 )
        screen.fill( ( 0, 150, 250, 200 ), box )
        hp = model.max_mp()
        hpd = min( model.mp_damage, hp )
        if hp > 0:
            box.x += box.w - ( hpd * box.w ) // hp
            box.w = dest.x + 7 + box.w - box.x
            screen.fill( (0, 0, 120, 100), box )


    def __call__( self , screen, show_quick_stats=True ):
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


        # Fill the modelmap, fieldmap, and itemmap.
        self.modelmap.clear()
        self.fieldmap.clear()
        itemmap = dict()
        for m in self.scene.contents:
            if isinstance( m , characters.Character ):
                self.modelmap[ tuple( m.pos ) ] = m
            elif isinstance( m , enchantments.Field ):
                self.fieldmap[ tuple( m.pos ) ] = m
            elif isinstance( m, items.Item ):
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


                    modl = self.modelmap.get( (x,y) , None )
                    if modl:
                        if modl.hidden:
                            # This is easy! All hidden models get the same sprite.
                            self.extrasprite.render( screen, dest, OVERLAY_HIDDEN )
                        else:
                            msprite = self.modelsprite.get( modl , None )
                            if not msprite:
                                msprite = modl.generate_avatar()
                                self.modelsprite[ modl ] = msprite
                            msprite.render( screen, dest, modl.FRAME )

                    fild = self.fieldmap.get( (x,y) , None )
                    if fild:
                        msprite = self.modelsprite.get( fild , None )
                        if not msprite:
                            msprite = fild.generate_avatar()
                            self.modelsprite[ fild ] = msprite
                        msprite.render( screen, dest, fild.frame( self.phase ) )


                    if ( x==tile_x ) and ( y==tile_y) and modl and show_quick_stats and not modl.hidden:
                        self.quick_model_status( screen, dest, modl )

                    mlist = self.anims.get( (x,y) , None )
                    if mlist:
                        for m in mlist:
                            m.render( self, screen, dest )





        self.phase = ( self.phase + 1 ) % 600
        self.mouse_tile = ( tile_x, tile_y )


