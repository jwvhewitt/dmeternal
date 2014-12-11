

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


class SmallTreasureEncounter( Plot ):
    LABEL = "ENCOUNTER"
    @classmethod
    def matches( self, pstate ):
        """Requires the SCENE to exist."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
          strength=100, habitat=scene.get_encounter_request(), fac=scene.fac ) )
        mychest = waypoints.SmallChest()
        mychest.stock(self.rank)
        room.contents.append( mychest )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True

class MediumTreasureEncounter( Plot ):
    LABEL = "ENCOUNTER"
    @classmethod
    def matches( self, pstate ):
        """Requires the SCENE to exist."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
          strength=125, habitat=scene.get_encounter_request(), fac=scene.fac ) )
        mychest = waypoints.MediumChest()
        mychest.stock(self.rank)
        room.contents.append( mychest )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True

class LargeTreasureEncounter( Plot ):
    LABEL = "ENCOUNTER"
    @classmethod
    def matches( self, pstate ):
        """Requires the SCENE to exist."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
          strength=160, habitat=scene.get_encounter_request(), fac=scene.fac ) )
        mychest = waypoints.LargeChest()
        mychest.stock(self.rank)
        room.contents.append( mychest )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True

class WildEncounter( Plot ):
    LABEL = "ENCOUNTER"
    active = True
    @classmethod
    def matches( self, pstate ):
        """Requires the SCENE to exist and be wilderness."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_WILDERNESS in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        # Add an encounter, monsters must be MTY_BEAST, favoring GEN_NATURE.
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myhabitat=scene.get_encounter_request()
        myhabitat[ context.MTY_BEAST ] = context.PRESENT
        myhabitat[ context.GEN_NATURE ] = context.MAYBE
        room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
          strength=random.randint(90,120), habitat=myhabitat ) )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True


