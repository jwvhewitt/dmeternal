import random
import maps
import pygame

#  ********************************
#  ***   INTERIOR  DECORATORS   ***
#  ********************************
# Not to be confused with Python function decorators... these add decor and
# props to a scene.

class BuildingDec( object ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ()
    def __init__( self, win = maps.SMALL_WINDOW ):
        self.win = win
    def windowize( self, gb, area ):
        y1 = area.y
        y2 = area.y + area.height - 1
        for x in range( area.x+1, area.x + area.width-1, 4 ):
            if gb.get_wall(x,y1) == maps.BASIC_WALL and not gb.map[x][y1].decor:
                gb.map[x][y1].decor = self.win
        x1 = area.x
        x2 = area.x + area.width - 1
        for y in range( area.y+1, area.y + area.height-1, 4 ):
            if gb.get_wall(x1,y) == maps.BASIC_WALL and not gb.map[x1][y].decor:
                gb.map[x1][y].decor = self.win
            if gb.get_wall(x2,y) == maps.BASIC_WALL and not gb.map[x2][y].decor:
                gb.map[x2][y].decor = self.win

    def __call__( self, gb, area ):
        if self.WALL_DECOR:
            for x in range( area.x+1, area.x + area.width-1 ):
                if gb.get_wall(x,area.y) == maps.BASIC_WALL and random.randint(1,3)==1 and not gb.map[x][area.y].decor:
                    random.choice( self.WALL_DECOR ).place( gb, (x,area.y) )
            for y in range( area.y+1, area.y + area.height-1 ):
                if gb.get_wall(area.x,y) == maps.BASIC_WALL and random.randint(1,3)==1 and not gb.map[area.x][y].decor:
                    gb.map[area.x][y].decor = random.choice( self.WALL_DECOR )
        self.windowize(gb,area)

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

class RockyDec( object ):
    """Add some rocks to the floor."""
    FLOOR_DECOR = ( maps.ROCKS, maps.ROCKS, maps.ROCKS, maps.TREES )
    def __init__( self, fill_factor = 42 ):
        self.fill_factor = fill_factor
    CARDIR = ( (1,0), (-1,0), (0,1), (0,-1) )
    def decor_nearby( self, gb, x, y ):
        """Return True if a decor is in one of four adjacent tiles."""
        decor_found = False
        for dx,dy in self.CARDIR:
            if gb.get_decor( x + dx, y + dy ):
                decor_found = True
                break
        return decor_found
    def __call__( self, gb, area ):
        for t in range( area.w * area.h // self.fill_factor ):
            x = random.choice( range( area.x , area.x + area.width ) )
            y = random.choice( range( area.y , area.y + area.height ) )
            if gb.on_the_map(x,y) and not gb.map[x][y].blocks_walking() and not gb.map[x][y].wall and not gb.map[x][y].decor and gb.wall_wont_block(x,y) and not self.decor_nearby(gb,x,y):
                # This is a good space. Add some decor.
                gb.map[x][y].decor = random.choice(self.FLOOR_DECOR)

class GoblinHomeDec( RockyDec ):
    FLOOR_DECOR = ( maps.PUDDLE, maps.BONE, maps.KEG, maps.PILED_GOODS )

class CarnageDec( RockyDec ):
    FLOOR_DECOR = (maps.SKULL, maps.BONE, maps.SKELETON, maps.FLOOR_BLOOD, maps.FLOOR_BLOOD)


