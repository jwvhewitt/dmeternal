
# A Waypoint is a special effect waiting on a tile. It is normally invisible,
# but can affect the terrain of the tile it is placed in. Walking onto the tile
# or bumping it will activate its effect.

import maps
import services
import exploration
import items
import traps
import random
import container
import rpgmenu
import pygame
import pygwrap
import effects
import charsheet
import charloader

class PuzzleMenu( rpgmenu.Menu ):
    WIDTH = 350
    HEIGHT = 250
    MENU_HEIGHT = 75

    def __init__( self, explo, wp ):
        x = explo.screen.get_width() // 2 - self.WIDTH // 2
        y = explo.screen.get_height() // 2 - self.HEIGHT // 2
        super(PuzzleMenu, self).__init__(explo.screen,x,y+self.HEIGHT-self.MENU_HEIGHT,self.WIDTH,self.MENU_HEIGHT,border=None,predraw=self.pre)
        self.full_rect = pygame.Rect( x,y,self.WIDTH,self.HEIGHT )
        self.text_rect = pygame.Rect( x, y, self.WIDTH, self.HEIGHT - self.MENU_HEIGHT - 16 )
        self.explo = explo
        self.desc = wp.desc

    def pre( self, screen ):
        self.explo.view( screen )
        pygwrap.default_border.render( screen , self.full_rect )
        pygwrap.draw_text( screen, pygwrap.SMALLFONT, self.desc, self.text_rect, justify = 0 )


class Waypoint( object ):
    TILE = None
    ATTACH_TO_WALL = False
    name = "Waypoint"
    desc = ""
    def __init__( self, scene=None, pos=(0,0), plot_locked=False, desc=None ):
        """Place this waypoint in a scene."""
        if scene:
            self.place( scene, pos )
        self.contents = container.ContainerList(owner=self)
        self.plot_locked = plot_locked
        if desc:
            self.desc = desc

    def place( self, scene, pos=None ):
        if hasattr( self, "container" ) and self.container:
            self.container.remove( self )
        self.scene = scene
        scene.contents.append( self )
        if pos and scene.on_the_map( *pos ):
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

    def unlocked_use( self, explo ):
        # Perform this waypoint's special action.
        if self.desc:
            explo.alert( self.desc )

    def bump( self, explo ):
        # If plot_locked, check plots for possible actions.
        # Otherwise, use the normal unlocked_use.
        if self.plot_locked:
            rpm = PuzzleMenu( explo, self )
            explo.expand_puzzle_menu( self, rpm )
            fx = rpm.query()
            if fx:
                fx( explo )
        else:
            self.unlocked_use( explo )


class Anvil( Waypoint ):
    TILE = maps.Tile( None, None, maps.ANVIL )
    desc = "You stand before an anvil."

class Bookshelf( Waypoint ):
    TILE = maps.Tile( None, None, maps.BOOKSHELF )
    ATTACH_TO_WALL = True
    desc = "You stand before a bookshelf."
    mini_map_label = "Bookshelf"

class Campsite( Waypoint ):
    TILE = maps.Tile( None, None, maps.CAULDRON )
    desc = "You stand before a fire."
    mini_map_label = "Campsite"


class Fountain( Waypoint ):
    TILE = maps.Tile( None, None, maps.FOUNTAIN )
    desc = "You stand before a fountain."
    mini_map_label = "Fountain"

class HealingFountain( Fountain ):
    HEAL_FX = effects.HealthRestore( dice=(1,6,9999), stat_bonus=None )
    def unlocked_use( self, explo ):
        # Perform this waypoint's special action.
        targets = list()
        for pc in explo.camp.party:
            if pc.is_alright():
                targets.append( pc.pos )
        explo.invoke_effect( self.HEAL_FX, None, targets )

class GateDoor( Waypoint ):
    TILE = maps.Tile( None, maps.CLOSED_DOOR, None )
    ATTACH_TO_WALL = True
    destination = None
    otherside = None
    desc = "You stand before a door."
    mini_map_label = "Door"
    def unlocked_use( self, explo ):
        if self.destination and self.otherside:
            explo.camp.destination = self.destination
            explo.camp.entrance = self.otherside
        else:
            explo.alert( "This door doesn't seem to go anywhere." )

class OpenGateDoor( Waypoint ):
    TILE = maps.Tile( None, maps.FAKE_OPEN_DOOR, None )
    ATTACH_TO_WALL = True
    destination = None
    otherside = None
    desc = "You stand before a door."
    mini_map_label = "Door"
    def unlocked_use( self, explo ):
        if self.destination and self.otherside:
            explo.camp.destination = self.destination
            explo.camp.entrance = self.otherside
        else:
            explo.alert( "This door doesn't seem to go anywhere." )

class Pit( Waypoint ):
    TILE = maps.Tile( None, None, maps.PIT )
    ATTACH_TO_WALL = False
    destination = None
    otherside = None
    desc = "You stand before a pit."
    mini_map_label = "Pit"
    def unlocked_use( self, explo ):
        if self.destination and self.otherside:
            explo.camp.destination = self.destination
            explo.camp.entrance = self.otherside
        else:
            explo.alert( self.desc )

class RoadSignBack( Waypoint ):
    TILE = maps.Tile( None, None, maps.SIGN_BACK )
    ATTACH_TO_WALL = False
    destination = None
    otherside = None
    desc = "You stand before a road sign."
    mini_map_label = "Way Back"
    def unlocked_use( self, explo ):
        if self.destination and self.otherside:
            explo.camp.destination = self.destination
            explo.camp.entrance = self.otherside
        else:
            explo.alert( self.desc )

class RoadSignForward( Waypoint ):
    TILE = maps.Tile( None, None, maps.SIGN_FORWARD )
    ATTACH_TO_WALL = False
    destination = None
    otherside = None
    desc = "You stand before a road sign."
    mini_map_label = "Way Forward"
    def unlocked_use( self, explo ):
        if self.destination and self.otherside:
            explo.camp.destination = self.destination
            explo.camp.entrance = self.otherside
        else:
            explo.alert( self.desc )

class RoadSignToAdventure( Waypoint ):
    # This road sign will generate and start a new shortie adventure.
    TILE = maps.Tile( None, None, maps.SIGN_FORWARD )
    ATTACH_TO_WALL = False
    destination = None
    otherside = None
    desc = "You stand before a road sign which points the way to adventure."
    mini_map_label = "Way Forward"
    def unlocked_use( self, explo ):
        #print explo.camp.scripts
        ynmenu = PuzzleMenu( explo, self )
        ynmenu.add_item( "Go on an adventure.", True )
        ynmenu.add_item( "Stay here for now.", False )
        if ynmenu.query():
            adv = explo.camp.add_story( "SHORTIE" )
            if adv:
                adv.begin_adventure( explo, self.scene, self )


class PowerCrystal( Waypoint ):
    TILE = maps.Tile( None, None, maps.CRYSTAL_ORB )
    desc = "You stand before a large crystal."
    mini_map_label = "Power Crystal"
    HEAL_FX = effects.ManaRestore( dice=(1,6,9999), stat_bonus=None )
    def unlocked_use( self, explo ):
        # Perform this waypoint's special action.
        targets = list()
        for pc in explo.camp.party:
            if pc.is_alright():
                targets.append( pc.pos )
        explo.invoke_effect( self.HEAL_FX, None, targets )


class SpiralStairsUp( Waypoint ):
    TILE = maps.Tile( None, maps.SPIRAL_STAIRS_UP, None )
    destination = None
    otherside = None
    desc = "You stand before a staircase."
    mini_map_label = "Stairs Up"
    def unlocked_use( self, explo ):
        if self.destination and self.otherside:
            explo.camp.destination = self.destination
            explo.camp.entrance = self.otherside
        else:
            explo.alert( "You have just bumped the stairs. Woohoo!" )

class StairsUp( SpiralStairsUp ):
    TILE = maps.Tile( None, maps.STAIRS_UP, None )
    ATTACH_TO_WALL = True
    desc = "You stand before a staircase."
    mini_map_label = "Stairs Up"

class StairsDown( SpiralStairsUp ):
    TILE = maps.Tile( None, maps.STAIRS_DOWN, None )
    ATTACH_TO_WALL = True
    desc = "You stand before a staircase."
    mini_map_label = "Stairs Down"

class SpiralStairsDown( SpiralStairsUp ):
    TILE = maps.Tile( None, maps.SPIRAL_STAIRS_DOWN, None )
    desc = "You stand before a staircase."
    mini_map_label = "Stairs Down"

class MineEntrance( SpiralStairsUp ):
    TILE = maps.Tile( None, None, maps.MINE_ENTRANCE )
    desc = "You stand before a mine entrance."

class DungeonEntrance( SpiralStairsUp ):
    TILE = maps.Tile( None, None, maps.DUNGEON_ENTRANCE )
    desc = "You stand before a dark passageway."

class PuzzleDoor( Waypoint ):
    TILE = maps.Tile( None, maps.CLOSED_DOOR, None )
    ATTACH_TO_WALL = True
    desc = "You stand before a door."
    def unlocked_use( self, explo ):
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
    UP = True
    desc = "You stand before a lever."
    mini_map_label = "Lever"
    def unlocked_use( self, explo ):
        if self.UP:
            self.scene.map[self.pos[0]][self.pos[1]].decor = maps.SWITCH_DOWN
            self.UP = False
        else:
            self.scene.map[self.pos[0]][self.pos[1]].decor = maps.SWITCH_UP
            self.UP = True
        explo.check_trigger( "USE", self )

class SmallChest( Waypoint ):
    TILE = maps.Tile( None, None, maps.SMALL_CHEST )
    gold = 0
    ALT_DECOR = maps.SMALL_CHEST_OPEN
    trap = None
    HOARD_AMOUNT = 50
    desc = "You stand before a chest."
    def unlocked_use( self, explo ):
        if self.trap:
            disarm = self.trap.trigger( explo, self.pos )
            if disarm:
                self.trap = None
                self.get_the_stuff( explo )
        else:
            self.get_the_stuff( explo )
    def get_the_stuff( self, explo ):
        if self.ALT_DECOR:
            self.scene.map[self.pos[0]][self.pos[1]].decor = self.ALT_DECOR
        if self.gold:
            explo.alert( "You find {0} gold pieces.".format( self.gold ) )
            explo.camp.gold += self.gold
            self.gold = 0
        ix = exploration.InvExchange( explo.camp.party, self.contents, explo.view )
        ix( explo.screen )
    def stock( self, hoard_rank=3, item_types=items.PREMIUM_TYPES ):
        self.gold,hoard = items.generate_hoard(hoard_rank,self.HOARD_AMOUNT,item_types)
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

class Cart( SmallChest ):
    TILE = maps.Tile( None, None, maps.CART )
    ALT_DECOR = None
    HOARD_AMOUNT = 100
    def stock( self, hoard_rank=3, item_types=items.PREMIUM_TYPES ):
        self.gold,hoard = items.generate_hoard(hoard_rank,self.HOARD_AMOUNT,item_types)
        self.contents += hoard

class Well( Waypoint ):
    TILE = maps.Tile( None, None, maps.WELL )
    desc = "You stand before a well."
    mini_map_label = "Well"

class Signpost( Waypoint ):
    TILE = maps.Tile( None, None, maps.SIGNPOST )
    desc = "You stand before a sign."

class TreeStump( Waypoint ):
    TILE = maps.Tile( None, None, maps.TREE_STUMP )
    desc = "You stand before a tree stump."

class BookOfHeroes( Waypoint ):
    TILE = maps.Tile( None, None, maps.SIGNPOST )
    desc = "You stand before a book."
    caption = "Book of Heroes"
    def add_members( self, camp, screen, predraw ):
        charloader.load_characters( camp.party, screen, predraw )
        if camp.party:
            camp.remove_party_from_scene()
            camp.entrance = self
            camp.place_party()
    def remove_members( self, camp, screen, predraw ):
        charsheets = dict()
        for pc in camp.party:
            charsheets[ pc ] = charsheet.CharacterSheet( pc , screen=screen )
        psr = charsheet.PartySelectRedrawer( charsheets=charsheets,
         predraw=predraw, screen=screen, caption="Remove Party Members" )
        while camp.party:
            rpm = charsheet.RightMenu( screen, predraw=psr, add_desc=False )
            psr.menu = rpm
            for pc in camp.party:
                rpm.add_item( str( pc ), pc )
            rpm.sort()
            rpm.add_alpha_keys()
            pc = rpm.query()

            if pc:
                pc.save()
                camp.party.remove( pc )
                camp.scene.contents.remove( pc )
            else:
                break
    def open_menu( self, camp, screen, predraw=None ):
        # Save the most recently used adventurer's guild. If all characters die,
        # this is where the game restarts.
        camp.mru_advguild = (self.scene,self)
        mypartysheet = charsheet.PartySheet( camp.party , screen=screen, camp=camp )
        myredraw = charsheet.CharacterViewRedrawer( csheet=mypartysheet, screen=screen, predraw=predraw, caption=self.caption )

        while True:
            rpm = charsheet.RightMenu( screen, predraw=myredraw )

            rpm.add_item( "Add Members", self.add_members )
            rpm.add_item( "Remove Members", self.remove_members )
            rpm.add_item( "Exit {0}".format(self.caption), False, self.desc )
            rpm.add_alpha_keys()

            it = rpm.query()

            if it:
                it( camp, screen, predraw )
                mypartysheet.regenerate_avatars()
            else:
                break
        camp.save( screen )
    def no_explo_use( self, camp, screen ):
        self.open_menu( camp, screen )
    def unlocked_use( self, explo ):
        self.open_menu( explo.camp, explo.screen, explo.view )



