from .. import maps
import plasma

#   ******************
#   ***  PREPPERS  ***
#   ******************
#
# Before map generation proper takes place, the grid must be prepared.
# Generally this will involve setting a terrain for the floor of each tile
# and setting the wall values to True. Note that "True" is not a valid terrain
# type- it will be converted to proper walls later on in the generation process.
#
# The prepper may also set the map generator's plasma attribute.

class BasicPrep( object ):
    """Fill map with True walls and basic floors."""
    def __init__( self, terr=maps.BASIC_FLOOR ):
        self.terr = terr

    def __call__( self, mapgen ):
        mapgen.fill( mapgen.gb, mapgen.area, floor=self.terr, wall=True )

class HeightfieldPrep( object ):
    """Use a plasma map to fill with water, lo, hi ground"""
    def __init__( self, loground=0.3, higround=0.5 ):
        self.loground = loground
        self.higround = higround
    def __call__( self, mapgen ):
        mapgen.plasma = plasma.Plasma()
        for x in range( mapgen.width ):
            for y in range( mapgen.height ):
                if mapgen.plasma.map[x][y] < self.loground:
                    mapgen.gb.map[x][y].floor = maps.WATER
                elif mapgen.plasma.map[x][y] < self.higround:
                    mapgen.gb.map[x][y].floor = maps.LOGROUND
                    mapgen.gb.map[x][y].wall = True
                else:
                    mapgen.gb.map[x][y].floor = maps.HIGROUND
                    mapgen.gb.map[x][y].wall = True


