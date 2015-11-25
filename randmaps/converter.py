import maps
import random
import plasma

#  **********************
#  ***   CONVERTERS   ***
#  **********************

class BasicConverter( object ):
    """Convert True walls to BASIC_WALLs."""
    def __init__( self, terr=maps.BASIC_WALL ):
        self.terr = terr

    def __call__( self, mapgen ):
        for x in range( mapgen.width ):
            for y in range( mapgen.height ):
                if mapgen.gb.map[x][y].wall is True:
                    mapgen.gb.map[x][y].wall = self.terr


class EdgyConverter( object ):
    """Convert edge walls to trees, internal to walls."""
    def __init__( self, edge=maps.TREES, terr=maps.BASIC_WALL ):
        self.edge = edge
        self.terr = terr

    def count_true_walls( self,mapgen,x0,y0 ):
        n = 0
        for x in range(x0-1,x0+2):
            for y in range(y0-1,y0+2):
                if mapgen.gb.on_the_map(x,y):
                    if mapgen.gb.map[x][y].wall is True:
                        n += 1
                else:
                    n += 1
        return n
    def mutate_walls( self, mapgen ):
        to_convert = list()
        for x in range( mapgen.width ):
            for y in range( mapgen.height ):
                if mapgen.gb.map[x][y].wall is True and self.count_true_walls(mapgen,x,y) < 6:
                    to_convert.append( (x,y) )
        for p in to_convert:
            mapgen.gb.map[p[0]][p[1]].wall = self.edge
    def __call__( self, mapgen ):
        for x in range( random.randint(1,3) ):
            self.mutate_walls( mapgen )
        for x in range( mapgen.width ):
            for y in range( mapgen.height ):
                if mapgen.gb.map[x][y].wall is True:
                    mapgen.gb.map[x][y].wall = self.terr

class ForestConverter( object ):
    """Convert True walls to rocks and trees and trees and rocks and rocks and trees and trees and rocks and mountains."""
    def __init__( self, treeline=0.85 ):
        self.treeline = treeline
    def water_nearby( self, mapgen, x, y ):
        """Return True if a water tile is adjacent."""
        found_water = False
        for d in mapgen.gb.DELTA8:
            if mapgen.gb.get_floor( x + d[0], y + d[1] ) is maps.WATER:
                found_water = True
                break
        return found_water

    def four_true_walls( self, mapgen, x, y ):
        """Return True if this tile is upper left corner of block of four True walls."""
        return (mapgen.gb.get_wall(x+1,y) is True) and (mapgen.gb.get_wall(x+1,y+1) is True) and (mapgen.gb.get_wall(x,y+1) is True)

    def __call__( self, mapgen ):
        if not hasattr( mapgen, "plasma" ):
            mapgen.plasma = plasma.Plasma()
        for x in range( mapgen.width ):
            for y in range( mapgen.height ):
                if mapgen.gb.map[x][y].wall is True:
                    if x%3 == 0 and y%3 == 0 and self.four_true_walls(mapgen,x,y) and random.triangular(0.3,1.0,0.90) < mapgen.plasma.map[x][y]:
                        mapgen.gb.map[x][y].wall = maps.MOUNTAIN_TOP
                        mapgen.gb.map[x+1][y].wall = maps.MOUNTAIN_RIGHT
                        mapgen.gb.map[x][y+1].wall = maps.MOUNTAIN_LEFT
                        mapgen.gb.map[x+1][y+1].wall = maps.MOUNTAIN_BOTTOM
                    elif self.water_nearby( mapgen, x, y ):
                        if random.randint(1,3) != 2:
                            mapgen.gb.map[x][y].wall = maps.ROCKS
                        else:
                            mapgen.gb.map[x][y].wall = None
                    else:
                        if mapgen.plasma.map[x][y] < self.treeline:
                            mapgen.gb.map[x][y].wall = maps.TREES
                        else:
                            mapgen.gb.map[x][y].wall = maps.ROCKS

class DesertConverter( ForestConverter ):
    """Convert True walls to rocks and trees and trees and rocks and rocks and trees and trees and rocks and mountains."""
    def desert_nearby( self, mapgen, x, y, terrain_to_check=(maps.HIGROUND,maps.HIHILL,None)):
        """Return True if all adjacent tiles are LOGROUND."""
        all_hi = True
        for d in mapgen.gb.DELTA8:
            if mapgen.gb.get_floor( x + d[0], y + d[1] ) not in terrain_to_check:
                all_hi = False
                break
        return all_hi
    def __call__( self, mapgen ):
        for x in range( mapgen.width ):
            for y in range( mapgen.height ):
                if mapgen.gb.map[x][y].wall is True:
                    if x%3 == 0 and y%3 == 0 and self.four_true_walls(mapgen,x,y) and random.randint(1,100) == 1:
                        mapgen.gb.map[x][y].wall = maps.MOUNTAIN_TOP
                        mapgen.gb.map[x+1][y].wall = maps.MOUNTAIN_RIGHT
                        mapgen.gb.map[x][y+1].wall = maps.MOUNTAIN_LEFT
                        mapgen.gb.map[x+1][y+1].wall = maps.MOUNTAIN_BOTTOM
                    elif self.water_nearby( mapgen, x, y ):
                        if random.randint(1,3) == 2:
                            mapgen.gb.map[x][y].wall = maps.TREES
                        else:
                            mapgen.gb.map[x][y].wall = None
                    elif mapgen.gb.get_floor(x,y) == maps.HIGROUND:
                        if self.desert_nearby( mapgen, x, y ) and random.randint(1,30) != 1:
                            mapgen.gb.map[x][y].wall = None
                            mapgen.gb.map[x][y].floor = maps.HIHILL

                        else:
                            mapgen.gb.map[x][y].wall = maps.ROCKS
                    else:
                        mapgen.gb.map[x][y].wall = maps.TREES


