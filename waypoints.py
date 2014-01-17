
# A Waypoint is a special effect waiting on a tile. It is normally invisible,
# but can affect the terrain of the tile it is placed in. Walking onto the tile
# or bumping it will activate its effect.

import maps
import services

class Waypoint( object ):
    TILE = None
    def __init__( self, scene, pos ):
        """Place this waypoint in a scene."""
        self.place( scene, pos )

    def place( self, scene, pos ):
        self.pos = pos
        scene.contents.append( self )
        if scene.on_the_map( *pos ) and self.TILE:
            if self.TILE.floor:
                scene.map[pos[0]][pos[1]].floor = self.TILE.floor
            if self.TILE.wall:
                scene.map[pos[0]][pos[1]].wall = self.TILE.wall
            if self.TILE.decor:
                scene.map[pos[0]][pos[1]].decor = self.TILE.decor

    def bump( self, explo ):
        # Perform this waypoint's special action.
        pass

class Bookshelf( Waypoint ):
    TILE = maps.Tile( None, None, maps.BOOKSHELF )
    LIBRARY = services.Library()
    def bump( self, explo ):
        self.LIBRARY( explo )

class SpiralStairsUp( Waypoint ):
    TILE = maps.Tile( None, maps.SPIRAL_STAIRS_UP, None )
    destination = None
    otherside = None
    def bump( self, explo ):
        if self.destination and self.otherside:
            explo.camp.destination = self.destination
            explo.camp.entrance = self.otherside
        else:
            explo.alert( "You have just bumped the stairs. Woohoo!" )

class SpiralStairsDown( Waypoint ):
    TILE = maps.Tile( None, maps.SPIRAL_STAIRS_DOWN, None )
    destination = None
    otherside = None
    def bump( self, explo ):
        if self.destination and self.otherside:
            explo.camp.destination = self.destination
            explo.camp.entrance = self.otherside
        else:
            explo.alert( "You have just bumped the stairs. Woohoo!" )

