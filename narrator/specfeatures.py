from plots import Plot,PlotError
import context
import items
import maps
import waypoints
import monsters
import dialogue
import services
import teams
import characters
import random
import randmaps
import effects
import stats
import animobs

#  ***************************
#  ***   SPECIAL_FEATURE   ***
#  ***************************
#
# One special feature gets placed in most scenes. It's not necessarily an
# encounter, not necessarily a treasure... just something to make life more
# interesting.

class Barracks( Plot ):
    # Find where the enemy sleeps.
    LABEL = "SPECIAL_FEATURE"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist, be a dungeon, and have a faction."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags
                and pstate.elements["LOCALE"].fac )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        room = randmaps.rooms.SharpRoom(random.randint(9,15),random.randint(9,15))
        room.DECORATE = randmaps.decor.BedroomDec()
        room.contents.append( teams.Team(default_reaction=0, rank=self.rank, 
          strength=120, habitat=scene.get_encounter_request(), fac=scene.fac ) )
        for t in range( random.randint(1,3) ):
            mychest = waypoints.SmallChest()
            mychest.stock(self.rank)
            room.contents.append( mychest )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True

class BoringLevel( Plot ):
    # This level gets a boring decoration of some type.
    LABEL = "SPECIAL_FEATURE"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        room.contents.append( random.choice( self.DECOR_OPTIONS ) )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True
    DECOR_OPTIONS = ( maps.SKULL,maps.BONE,maps.KEG,maps.PILED_GOODS,
        maps.LIGHT_STAND,maps.PUDDLE,maps.ROCKS )

class CheaterChest( Plot ):
    LABEL = "SPECIAL_FEATURE"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        room.DECORATE = randmaps.decor.MonsterDec()
        mychest = waypoints.LargeChest()
        mychest.TILE = maps.Tile( None, None, maps.LARGE_CHEST_OPEN )
        mychest.gold = 1
        room.contents.append( mychest )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True


class DungeonPoem( Plot ):
    LABEL = "SPECIAL_FEATURE"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        mysign = waypoints.Signpost()
        mysign.desc = '"Dark and foreboding, the final rest of many: eaten by a grue."'
        room.contents.append( mysign )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True


class FountainOfDeath( Plot ):
    LABEL = "SPECIAL_FEATURE"
    active = True
    scope = "LOCALE"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon of > rank 1."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags
                and self.rank > 1 )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myfountain = waypoints.Fountain( plot_locked = True )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        self.register_element( "FOUNTAIN", myfountain, dident="_ROOM" )
        return True
    def FOUNTAIN_menu( self, thingmenu ):
        thingmenu.desc = "{0} Do you want to take a drink?".format( thingmenu.desc )
        thingmenu.add_item( "Take a drink.", self.use_fountain )
        thingmenu.add_item( "Leave it alone.", None )
    FOUNTAIN_FX = effects.HealthDamage( att_dice=(1,8,0), element=stats.RESIST_POISON,
        anim=animobs.PoisonCloud )
    def use_fountain( self, explo ):
        fountain = self.elements[ "FOUNTAIN" ]
        explo.alert( "The water is poison!" )
        targets = list()
        for pc in explo.camp.party:
            if pc.is_alright():
                targets.append( pc.pos )
        explo.invoke_effect( self.FOUNTAIN_FX, None, targets )
        fountain.plot_locked = False
        fountain.desc = "You don't want to try drinking from this fountain again."
        self.active = False

class FountainOfHealing( Plot ):
    LABEL = "SPECIAL_FEATURE"
    active = True
    scope = "LOCALE"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()

        myfountain = waypoints.HealingFountain( plot_locked = True )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        self.register_element( "FOUNTAIN", myfountain, dident="_ROOM" )
        return True
    def FOUNTAIN_menu( self, thingmenu ):
        thingmenu.desc = "{0} Do you want to take a drink?".format( thingmenu.desc )
        thingmenu.add_item( "Take a drink.", self.use_fountain )
        thingmenu.add_item( "Leave it alone.", None )
    def use_fountain( self, explo ):
        fountain = self.elements[ "FOUNTAIN" ]
        explo.alert( "The refreshing water heals your wounds." )
        fountain.unlocked_use( explo )
        fountain.plot_locked = False
        self.active = False

class FountainOfDoubt( Plot ):
    LABEL = "SPECIAL_FEATURE"
    active = True
    scope = "LOCALE"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myfountain = waypoints.Fountain( plot_locked = True )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        self.register_element( "FOUNTAIN", myfountain, dident="_ROOM" )
        return True
    def FOUNTAIN_menu( self, thingmenu ):
        thingmenu.desc = "{0} Do you want to take a drink?".format( thingmenu.desc )
        thingmenu.add_item( "Take a drink.", self.use_fountain )
        thingmenu.add_item( "Leave it alone.", None )
    def use_fountain( self, explo ):
        fountain = self.elements[ "FOUNTAIN" ]
        explo.alert( "This fountain doesn't seem to do anything. Perhaps it's the Fountain of Doubt." )
        fountain.plot_locked = False
        self.active = False

class RedHerringsChest( Plot ):
    # Just an unguarded chest in the dungeon... to make the players worry.
    LABEL = "SPECIAL_FEATURE"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        mychest = waypoints.SmallChest()
        mychest.stock(self.rank)
        room.contents.append( mychest )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True



