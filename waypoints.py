
# A Waypoint is a special effect waiting on a tile. It is normally invisible,
# but can affect the terrain of the tile it is placed in. Walking onto the tile
# or bumping it will activate its effect.

import maps
import services
import exploration
import items
import traps
import random

class Waypoint( object ):
    TILE = None
    ATTACH_TO_WALL = False
    def __init__( self, scene=None, pos=(0,0) ):
        """Place this waypoint in a scene."""
        if scene:
            self.place( scene, pos )
        self.contents = list()

    def place( self, scene, pos ):
        self.scene = scene
        scene.contents.append( self )
        if scene.on_the_map( *pos ):
            self.pos = pos
            if self.TILE:
                if self.TILE.floor:
                    scene.map[pos[0]][pos[1]].floor = self.TILE.floor
                if self.TILE.wall:
                    scene.map[pos[0]][pos[1]].wall = self.TILE.wall
                if self.TILE.decor:
                    scene.map[pos[0]][pos[1]].decor = self.TILE.decor
        else:
            self.pos = (0,0)

    def bump( self, explo ):
        # Perform this waypoint's special action.
        pass

class Bookshelf( Waypoint ):
    TILE = maps.Tile( None, None, maps.BOOKSHELF )
    ATTACH_TO_WALL = True
    LIBRARY = services.Library()
    def bump( self, explo ):
        self.LIBRARY( explo )

class GateDoor( Waypoint ):
    TILE = maps.Tile( None, maps.CLOSED_DOOR, None )
    destination = None
    otherside = None
    def bump( self, explo ):
        if self.destination and self.otherside:
            explo.camp.destination = self.destination
            explo.camp.entrance = self.otherside
        else:
            explo.alert( "This door doesn't seem to go anywhere." )

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

class StairsUp( SpiralStairsUp ):
    TILE = maps.Tile( None, maps.STAIRS_UP, None )
    ATTACH_TO_WALL = True

class StairsDown( SpiralStairsUp ):
    TILE = maps.Tile( None, maps.STAIRS_DOWN, None )
    ATTACH_TO_WALL = True

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

class PuzzleDoor( Waypoint ):
    TILE = maps.Tile( None, maps.CLOSED_DOOR, None )
    ATTACH_TO_WALL = True
    def bump( self, explo ):
        explo.alert( "This door is impassable." )
    def activate( self, explo ):
        self.scene.map[self.pos[0]][self.pos[1]].wall = maps.OPEN_DOOR
        if explo.scene is self.scene:
            explo.alert( "You hear a rumbling noise in the distance..." )
        else:
            explo.alert( "You get the feeling that new possibilities have been opened up." )

class PuzzleSwitch( Waypoint ):
    TILE = maps.Tile( None, None, maps.SWITCH_UP )
    ATTACH_TO_WALL = True
    CALL = None
    RECALL = None
    UP = True
    def bump( self, explo ):
        if self.UP:
            if self.CALL:
                self.CALL( explo )
                self.scene.map[self.pos[0]][self.pos[1]].decor = maps.SWITCH_DOWN
                self.UP = False
            else:
                explo.alert( "This lever is stuck." )
        else:
            if self.RECALL:
                self.RECALL( explo )
                self.scene.map[self.pos[0]][self.pos[1]].decor = maps.SWITCH_UP
                self.UP = True
            else:
                explo.alert( "This lever is stuck." )

class SmallChest( Waypoint ):
    TILE = maps.Tile( None, None, maps.SMALL_CHEST )
    gold = 0
    ALT_DECOR = maps.SMALL_CHEST_OPEN
    trap = None
    HOARD_AMOUNT = 50
    def bump( self, explo ):
        if self.trap:
            disarm = self.trap.trigger( explo, self.pos )
            if disarm:
                self.trap = None
                self.get_the_stuff( explo )
        else:
            self.get_the_stuff( explo )
    def get_the_stuff( self, explo ):
        self.scene.map[self.pos[0]][self.pos[1]].decor = self.ALT_DECOR
        if self.gold:
            explo.alert( "You find {0} gold pieces.".format( self.gold ) )
            explo.camp.gold += self.gold
            self.gold = 0
        ix = exploration.InvExchange( explo.camp.party, self.contents, explo.view )
        ix( explo.screen )
    def stock( self, hoard_rank=3 ):
        self.gold,hoard = items.generate_hoard(hoard_rank,self.HOARD_AMOUNT)
        self.contents += hoard
        if random.randint(1,500) < self.HOARD_AMOUNT:
            self.trap = traps.choose_trap( hoard_rank )

class MediumChest( SmallChest ):
    TILE = maps.Tile( None, None, maps.MEDIUM_CHEST )
    ALT_DECOR = maps.MEDIUM_CHEST_OPEN
    HOARD_AMOUNT = 100

class LargeChest( SmallChest ):
    TILE = maps.Tile( None, None, maps.LARGE_CHEST )
    ALT_DECOR = maps.LARGE_CHEST_OPEN
    HOARD_AMOUNT = 200


