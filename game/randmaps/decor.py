import random
from .. import maps
import pygame

#  ********************************
#  ***   INTERIOR  DECORATORS   ***
#  ********************************
# Not to be confused with Python function decorators... these add decor and
# props to a scene.

class OmniDec( object ):
    """Add windows, wall decor, and floor decor to an area."""
    WALL_DECOR = ()
    WALL_FILL_FACTOR = 0.3
    WIN_DECOR = None
    FLOOR_DECOR = ()
    FLOOR_FILL_FACTOR = 0.007
    def __init__( self, win=True, wall_fill_factor=None, floor_fill_factor=None ):
        if win is not True:
            self.WIN_DECOR = win
        self.WALL_FILL_FACTOR = wall_fill_factor or self.WALL_FILL_FACTOR
        self.FLOOR_FILL_FACTOR = floor_fill_factor or self.FLOOR_FILL_FACTOR
    def windowize( self, gb, area ):
        y1 = area.y
        y2 = area.y + area.height - 1
        for x in range( area.x+1, area.x + area.width-1, 4 ):
            if gb.get_wall(x,y1) == maps.BASIC_WALL and not gb.map[x][y1].decor:
                gb.map[x][y1].decor = self.WIN_DECOR
        x1 = area.x
        x2 = area.x + area.width - 1
        for y in range( area.y+1, area.y + area.height-1, 4 ):
            if gb.get_wall(x1,y) == maps.BASIC_WALL and not gb.map[x1][y].decor:
                gb.map[x1][y].decor = self.WIN_DECOR
            if gb.get_wall(x2,y) == maps.BASIC_WALL and not gb.map[x2][y].decor:
                gb.map[x2][y].decor = self.WIN_DECOR
    def is_good_spot_for_wall_decor( self, gb, pos ):
        # This is a good spot for wall decor if we have three basic walls in a
        # row, a space out front, and nothing else here.
        x,y = pos
        #if gb.get_bumpable_at_spot(pos) or not gb.map.get_wall(x,y) == maps.BASIC_WALL:
        #    return False
        if x >= gb.width-1 or y >= gb.height - 1:
            return False
        elif ( gb.get_wall(x-1,y)==maps.BASIC_WALL and 
          gb.get_wall(x+1,y)==maps.BASIC_WALL and
          not gb.tile_blocks_walking(x,y+1) ):
            return True
        elif ( gb.get_wall(x,y-1)==maps.BASIC_WALL and 
          gb.get_wall(x,y+1)==maps.BASIC_WALL and
          not gb.tile_blocks_walking(x+1,y) ):
            return True
    def draw_wall_decor( self, gb, x, y ):
        gb.map[x][y].decor = random.choice(self.WALL_DECOR)
    def draw_floor_decor( self, gb, x, y ):
        gb.map[x][y].decor = random.choice(self.FLOOR_DECOR)

    def __call__( self, gb, area ):
        good_wall_spots = list()
        good_floor_spots = list()
        for x in range(area.x, area.x + area.width-1):
            for y in range(area.y, area.y + area.height-1):
                pos = (x,y)
                if gb.get_wall(x,y) == maps.BASIC_WALL and self.is_good_spot_for_wall_decor(gb,pos):
                    good_wall_spots.append( pos )
                elif x > 0 and y > 0 and \
                  not gb.map[x][y].blocks_walking() and not gb.map[x][y].wall \
                  and not gb.map[x][y].decor and gb.wall_wont_block(x,y):
                    good_floor_spots.append( pos )
        for m in gb.contents:
            if hasattr(m,"pos"):
                if m.pos in good_wall_spots:
                    good_wall_spots.remove( m.pos )
                elif m.pos in good_floor_spots:
                    good_floor_spots.remove( m.pos )

        if self.FLOOR_DECOR:
            for t in range(int(len(good_floor_spots) * self.FLOOR_FILL_FACTOR)):
                x,y = random.choice( good_floor_spots )
                if gb.wall_wont_block(x,y):
                    self.draw_floor_decor(gb,x,y)
        if self.WALL_DECOR:
            for t in range( int( len(good_wall_spots) * self.WALL_FILL_FACTOR)):
                x,y = random.choice( good_wall_spots )
                if self.is_good_spot_for_wall_decor( gb,(x,y) ):
                    self.draw_wall_decor(gb,x,y)

        if self.WIN_DECOR:
            self.windowize(gb,area)


class BuildingDec( OmniDec ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WIN_DECOR = maps.SMALL_WINDOW

class TavernDec( BuildingDec ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ( maps.WALL_LIGHT, )

class WeaponShopDec( BuildingDec ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ( maps.WALL_WEAPON_RACK, maps.WALL_WEAPON_RACK, maps.WALL_CRATES )

class ArmorShopDec( BuildingDec ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ( maps.BENCH, maps.DRESSER, maps.DRESSER, maps.WALL_CRATES )


class GeneralStoreDec( BuildingDec ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ( maps.PROVISIONS, maps.PROVISIONS, maps.WALL_CRATES, maps.WALL_WEAPON_RACK,
        maps.BIG_SHELF, maps.BIG_SHELF )

class LibraryDec( BuildingDec ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ( maps.PORTRAIT, maps.LANDSCAPE_PICTURE, maps.HIGH_SHELF, maps.BENCH )

class BedroomDec( BuildingDec ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ( maps.LANDSCAPE_PICTURE, maps.BENCH, maps.BENCH, maps.DRESSER, maps.DRESSER )
    def all_clear( self, gb, area, point ):
        """Return true if no walls or decor in area, no map contents in point."""
        ok = True
        for x in range( area.x, area.x + area.width ):
            for y in range( area.y, area.y + area.height ):
                if gb.get_wall(x,y) or gb.get_decor(x,y):
                    ok = False
                    break
        if ok:
            if any( m.pos == point for m in gb.contents if hasattr(m,"pos") ):
                ok = False
        return ok
    def __call__( self, gb, area ):
        beds = random.randint(2,5)
        if self.WALL_DECOR:
            for x in range( area.x+1, area.x + area.width-1 ):
                if gb.get_wall(x,area.y) == maps.BASIC_WALL and not gb.map[x][area.y].decor:
                    if beds > 0 and self.all_clear(gb,pygame.Rect(x-1,area.y+1,3,2),(x,area.y+1)) and random.randint(1,4)==1:
                        gb.map[x][area.y].decor = maps.BED_HEAD
                        gb.map[x][area.y+1].decor = maps.BED_FOOT
                        beds += -1
                    elif random.randint(1,3)==1:
                        random.choice( self.WALL_DECOR ).place( gb, (x,area.y) )
            for y in range( area.y+1, area.y + area.height-1 ):
                if gb.get_wall(area.x,y) == maps.BASIC_WALL and not gb.map[area.x][y].decor:
                    if beds > 0 and self.all_clear(gb,pygame.Rect(area.x+1,y-1,2,3),(area.x+1,y)) and random.randint(1,2)==1:
                        gb.map[area.x][y].decor = maps.BED_HEAD
                        gb.map[area.x+1][y].decor = maps.BED_FOOT
                        beds += -1
                    elif random.randint(1,3)==1:
                        random.choice( self.WALL_DECOR ).place( gb, (x,area.y) )
        self.windowize(gb,area)

class TempleDec( BuildingDec ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ( maps.SUN_PICTURE, maps.MOON_PICTURE, maps.HIGH_SHELF, maps.BENCH,
        maps.COLUMN, maps.COLUMN, maps.WALL_LIGHT, maps.WALL_LIGHT )

class MonsterDec( object ):
    """Just add this room to the monster_zones list. Maybe add some monster sign."""
    FLOOR_DECOR = (maps.SKULL, maps.BONE, maps.SKELETON, maps.FLOOR_BLOOD, maps.FLOOR_BLOOD)
    def __call__( self, gb, area ):
        gb.monster_zones.append( area )
        if random.randint(1,3)!=1:
            for t in range( random.randint(1,3) ):
                x = random.choice( range( area.x , area.x + area.width ) )
                y = random.choice( range( area.y , area.y + area.height ) )
                if gb.on_the_map(x,y) and not gb.map[x][y].blocks_walking() and not gb.map[x][y].wall and not gb.map[x][y].decor:
                    # This is an empty space. Add some carnage.
                    gb.map[x][y].decor = random.choice(self.FLOOR_DECOR)



class RockyDec( OmniDec ):
    """Add some rocks to the floor."""
    FLOOR_DECOR = ( maps.ROCKS, maps.ROCKS, maps.ROCKS, maps.TREES )
    FLOOR_FILL_FACTOR = 0.2
    CARDIR = ( (1,0), (-1,0), (0,1), (0,-1) )
    def basic_wall_nearby( self, gb, x, y ):
        """Return True if a wall is in one of four adjacent tiles."""
        wall_found = False
        for dx,dy in self.CARDIR:
            if gb.get_wall( x + dx, y + dy ) == maps.BASIC_WALL:
                wall_found = True
                break
        return wall_found
    def draw_floor_decor( self, gb, x, y ):
        if self.basic_wall_nearby(gb,x,y):
            gb.map[x][y].wall = maps.BASIC_WALL
        else:
            gb.map[x][y].decor = random.choice(self.FLOOR_DECOR)

class GoblinHomeDec( OmniDec ):
    FLOOR_DECOR = ( maps.PUDDLE, maps.BONE, maps.KEG, maps.PILED_GOODS )

class CarnageDec( OmniDec ):
    FLOOR_DECOR = (maps.SKULL, maps.BONE, maps.SKELETON, maps.FLOOR_BLOOD, maps.FLOOR_BLOOD)

class BarracksDec( OmniDec ):
    WALL_DECOR = (maps.PROVISIONS, maps.WALL_CRATES, maps.WALL_WEAPON_RACK,
        maps.WALL_WEAPON_RACK, maps.BIG_SHELF, maps.WALL_LIGHT)
    FLOOR_DECOR = (maps.FLOOR_BLOOD, maps.KEG)
    FLOOR_FILL_FACTOR = 0.007


