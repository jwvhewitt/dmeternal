from .plots import Plot,PlotError,PlotState
from .. import context
from .. import items
from .. import maps
from .. import randmaps
from .. import waypoints
from .. import monsters
from .. import dialogue
from .. import services
from .. import teams
from .. import characters
from .. import namegen
import random

###   ********************
###   ***  GET_SECRET  ***
###   ********************
#
# This subplot will be passed a secret string as element TARGET.
# When the secret is revealed to the PC, a trigger will be invoked
# based on this element and the trigger ID "SECRET".

class GS_BarbarianGraffiti( Plot ):
    """Learn the secret by reading it on a sign."""
    LABEL = "GET_SECRET"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET and LOCALE to exist."""
        return pstate.elements.get("TARGET") and pstate.elements.get("LOCALE")
    def custom_init( self, nart ):
        """Create the encounter."""
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myhabitat=scene.get_encounter_request()
        myhabitat[ context.GEN_GIANT ] = context.PRESENT
        room.contents.append( teams.Team(default_reaction=0, rank=self.rank, 
          strength=100, habitat=myhabitat, respawn=False ) )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        signpost = waypoints.Signpost()
        self.register_element( "_SIGN", signpost, dident="_ROOM" )
        signpost.plot_locked = True
        signpost.mini_map_label = "Signpost"
        return True
    def _SIGN_menu( self, thingmenu ):
        thingmenu.desc = "The writing on this sign is really bad. It was probably written by ogres."
        thingmenu.add_item( "Attempt to decipher it.", self.use_sign )
    def use_sign( self, explo ):
        explo.alert( '"{0}"'.format(self.elements["TARGET"]))
        explo.check_trigger( "SECRET", self.elements[ "TARGET" ] )
        self.active = False

class GS_HintFromSomebodyCivilized( Plot ):
    """Learn the secret by hearing it from an NPC."""
    LABEL = "GET_SECRET"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET and LOCALE to exist."""
        return pstate.elements.get("TARGET") and pstate.elements.get("LOCALE")
    def seek_room( self, thing ):
        # We need a room that is marked as CIVILIZED and PUBLIC.
        return isinstance( thing, randmaps.Room ) and context.CIVILIZED in thing.tags and context.ROOM_PUBLIC in thing.tags
    def seek_npc( self, thing ):
        # We need a NPC.
        return isinstance( thing, characters.Character ) and context.CHAR_NPC in thing.tags
    def custom_init( self, nart ):
        # Locate a room within LOCALE scope which is CIVILIZED and ROOM_PUBLIC
        room = self.seek_element( nart, "_ROOM", self.seek_room, scope=self.elements["LOCALE"] )
        # Locate a NPC within this room.
        npc = self.seek_element( nart, "_NPC", self.seek_npc, scope=room, check_subscenes=False )
        return True
    def hear_secret( self, explo ):
        explo.check_trigger( "SECRET", self.elements[ "TARGET" ] )
        self.active = False
    OFFER_PATTERNS = ( "{0}", "{0} At least, that is what I heard.", "Not many people know this. {0}",
        "{0} That is all I will say." )
    def _NPC_offers( self, explo ):
        # Return list of NPC offers.
        ol = list()
        ol.append( dialogue.Offer( random.choice( self.OFFER_PATTERNS ).format( self.elements["TARGET"] ) ,
         context = context.ContextTag([context.INFO,context.HINT]), effect=self.hear_secret ) )
        return ol

###   *******************
###   ***  GET_THING  ***
###   *******************
#
# This subplot will be passed a thing as element TARGET.
# Put this thing somewhere that the PC can get to it.
#

class GT_HauntedHouse( Plot ):
    """The thing is inside a haunted house."""
    LABEL = "GET_THING"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET and LOCALE to exist, and LOCALE to be wilderness."""
        return ( pstate.elements.get("TARGET") and pstate.elements.get("LOCALE")
            and context.MAP_WILDERNESS in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        exterior = randmaps.rooms.BuildingRoom( tags=(context.CIVILIZED,) )
        exterior.special_c[ "window" ] = maps.DARK_WINDOW
        self.register_element( "_EXTERIOR", exterior, dident="LOCALE" )
        locale = self.elements.get( "LOCALE" )
        interior = maps.Scene( 50,50, sprites={maps.SPRITE_WALL: "terrain_wall_dungeon.png", 
            maps.SPRITE_FLOOR: "terrain_floor_dungeon.png", maps.SPRITE_CHEST: "terrain_chest_metal.png",
            maps.SPRITE_INTERIOR: "terrain_int_temple.png" },
            biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.MAP_DUNGEON,context.GEN_UNDEAD,context.DES_LUNAR,context.MTY_UNDEAD) )
        igen = randmaps.SubtleMonkeyTunnelScene( interior )
        interior.name = "{0} Manor".format( namegen.ELDRITCH.gen_word() )
        gate_1 = waypoints.OpenGateDoor()
        gate_2 = waypoints.GateDoor()
        gate_1.destination = interior
        gate_1.otherside = gate_2
        gate_1.mini_map_label = "Haunted House"
        gate_2.destination = locale
        gate_2.otherside = gate_1
        self.register_scene( nart, interior, igen, ident="BUILDING_INT", dident="LOCALE" )
        exterior.special_c[ "door" ] = gate_1
        int_mainroom = randmaps.rooms.SharpRoom( tags=(context.ENTRANCE,), anchor=randmaps.anchors.south, parent=interior )
        int_mainroom.contents.append( gate_2 )
        int_mainroom.contents.append( maps.SKULL_ALTAR )
        gate_2.anchor = randmaps.anchors.south

        # Add the goal room, move the target there.
        int_goalroom = randmaps.rooms.SharpRoom( tags=(context.GOAL,), parent=interior )
        target = self.elements[ "TARGET" ]
        if isinstance( target, items.Item ):
            dest = waypoints.SmallChest()
            dest.stock( self.rank )
            int_goalroom.contents.append( dest )
        else:
            dest = int_goalroom
        self.move_element( ele=target,dest=dest )

        # Add some encounters. Mostly for the treasure chests.
        pstate = PlotState( elements={"LOCALE":interior} ).based_on( self )
        for t in range( random.randint(1,3) ):
            self.add_sub_plot( nart, "ENCOUNTER", pstate )
        return True









