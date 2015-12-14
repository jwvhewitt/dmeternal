

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

import stats
import spells
import aibrain
class EarthbindTester( monsters.base.Monster ):
    name = "Earthbind Tester"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 12, stats.REFLEXES: 17, \
        stats.INTELLIGENCE: 80, stats.PIETY: 80, stats.CHARISMA: 4,
        stats.PHYSICAL_ATTACK: 5, stats.NATURAL_DEFENSE: 5 }
    SPRITENAME = "monster_animals.png"
    FRAME = 9
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = None
    HABITAT = ( context.HAB_BUILDING, context.HAB_TUNNELS,
     context.SET_EVERY,
     context.DES_EARTH, context.DES_CIVILIZED,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
    ENC_LEVEL = 1
    TECHNIQUES = ( spells.earthspells.EARTHBIND, )
    COMBAT_AI = aibrain.BasicTechnicalAI()

    ATTACK = items.Attack( (1,4,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( monsters.base.Beast( 1, self ) )


class TestEncounter( Plot ):
    LABEL = "zTEST_FEATURE"
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myteam = teams.Team(default_reaction=-999, rank=self.rank, 
          strength=0, habitat=scene.get_encounter_request(), fac=scene.fac )
        room.contents.append( myteam )
        monster = monsters.ignan.Spark( myteam )
        room.contents.append( monster )
        room.contents.append( waypoints.HealingFountain() )
        mychest = waypoints.MediumChest()
        mychest.stock(20)
        room.contents.append( mychest )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True


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
        return ( pstate.elements.get("LOCALE") and pstate.rank > 1
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

class WildAntagonists( Plot ):
    LABEL = "ENCOUNTER"
    @classmethod
    def matches( self, pstate ):
        """Requires the SCENE to exist."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_WILDERNESS in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myhabitat=scene.get_encounter_request()
        myhabitat[ context.MTY_HUMANOID ] = context.MAYBE
        room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
          strength=100, habitat=scene.get_encounter_request(), fac=scene.fac ) )
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


