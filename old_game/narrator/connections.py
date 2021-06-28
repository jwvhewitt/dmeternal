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

""" A CONNECT subplot connects two levels, which are passed via the plotstate
    as elements PREV and NEXT.
"""

class AbandonedMineEntrance( Plot ):
    LABEL = "CONNECT"
    @classmethod
    def matches( self, pstate ):
        """Requires PREV and NEXT to exist, to not be wilderness, and for NEXT to not go up."""
        return ( pstate.elements.get( "PREV" ) and pstate.elements.get( "NEXT" )
         and context.MAP_WILDERNESS in pstate.elements["PREV"].desctags
         and context.DES_CIVILIZED in pstate.elements["PREV"].desctags
         and context.HAB_CAVE == pstate.elements["NEXT"].biome )

    def custom_init( self, nart ):
        prev = self.elements[ "PREV" ]
        next = self.elements[ "NEXT" ]
        self.move_element( next, prev )

        myzone1 = self.register_element( "_P_ROOM", randmaps.rooms.MountainRoom(tags=(context.GOAL,context.CIVILIZED,)), "PREV" )
        myzone2 = self.register_element( "_N_ROOM", randmaps.rooms.SharpRoom(tags=(context.ENTRANCE,)), "NEXT" )

        stairs_1 = waypoints.MineEntrance()
        stairs_2 = waypoints.GateDoor()

        stairs_1.destination = next
        stairs_1.otherside = stairs_2
        stairs_2.destination = prev
        stairs_2.otherside = stairs_1

        if hasattr( next, "dname" ):
            stairs_1.mini_map_label = next.dname
        else:
            stairs_1.mini_map_label = next.name
        stairs_2.mini_map_label = "Exit"

        myzone1.special_c["door"] = stairs_1
        myzone2.contents.append( stairs_2 )
        return True


class DefaultDungeonEntrance( Plot ):
    LABEL = "CONNECT"
    @classmethod
    def matches( self, pstate ):
        """Requires PREV and NEXT to exist as wilderness and dungeon."""
        return ( pstate.elements.get( "PREV" ) and pstate.elements.get( "NEXT" )
         and context.MAP_WILDERNESS in pstate.elements["PREV"].desctags
         and context.MAP_DUNGEON in pstate.elements["NEXT"].desctags )
    def custom_init( self, nart ):
        prev = self.elements[ "PREV" ]
        next = self.elements[ "NEXT" ]
        self.move_element( next, prev )

        myzone1 = self.register_element( "_P_ROOM", randmaps.rooms.MountainRoom(tags=(context.GOAL,)), "PREV" )
        myzone2 = self.register_element( "_N_ROOM", nart.get_map_generator( next ).DEFAULT_ROOM(tags=(context.ENTRANCE,)), "NEXT" )

        stairs_1 = waypoints.DungeonEntrance()
        if context.MAP_GOUP in next.desctags:
            if isinstance( myzone2, randmaps.rooms.SharpRoom ):
                stairs_2 = waypoints.StairsDown()
            else:
                stairs_2 = waypoints.SpiralStairsDown()
        else:
            if isinstance( myzone2, randmaps.rooms.SharpRoom ):
                stairs_2 = waypoints.StairsUp()
            else:
                stairs_2 = waypoints.SpiralStairsUp()

        stairs_1.destination = next
        stairs_1.otherside = stairs_2
        stairs_2.destination = prev
        stairs_2.otherside = stairs_1

        if hasattr( next, "dname" ):
            stairs_1.mini_map_label = next.dname
        else:
            stairs_1.mini_map_label = next.name

        myzone1.special_c["door"] = stairs_1
        myzone2.contents.append( stairs_2 )
        return True


class DefaultGoUp( Plot ):
    LABEL = "CONNECT"
    @classmethod
    def matches( self, pstate ):
        """Requires PREV and NEXT to exist, to not be wilderness, and for NEXT to not go up."""
        return ( pstate.elements.get( "PREV" ) and pstate.elements.get( "NEXT" )
         and context.MAP_WILDERNESS not in pstate.elements["PREV"].desctags
         and context.MAP_WILDERNESS not in pstate.elements["NEXT"].desctags
         and context.MAP_GODOWN not in pstate.elements["NEXT"].desctags )

    def custom_init( self, nart ):
        prev = self.elements[ "PREV" ]
        next = self.elements[ "NEXT" ]
        self.move_element( next, prev )

        myzone1 = self.register_element( "_P_ROOM", nart.get_map_generator( prev ).DEFAULT_ROOM(tags=(context.GOAL,)), "PREV" )
        myzone2 = self.register_element( "_N_ROOM", nart.get_map_generator( next ).DEFAULT_ROOM(tags=(context.ENTRANCE,)), "NEXT" )

        # Depending on whether we're going to a sharp room (with a guaranteed
        # border wall) or another room type, either go with the wall-mounted
        # default stairs or the free-standing spiral stairs.
        if isinstance( myzone1, randmaps.rooms.SharpRoom ):
            stairs_1 = waypoints.StairsUp()
        else:
            stairs_1 = waypoints.SpiralStairsUp()

        if isinstance( myzone2, randmaps.rooms.SharpRoom ):
            stairs_2 = waypoints.StairsDown()
        else:
            stairs_2 = waypoints.SpiralStairsDown()

        stairs_1.destination = next
        stairs_1.otherside = stairs_2
        stairs_2.destination = prev
        stairs_2.otherside = stairs_1

        myzone1.contents.append( stairs_1 )
        myzone2.contents.append( stairs_2 )
        return True


class DefaultGoDown( Plot ):
    LABEL = "CONNECT"
    @classmethod
    def matches( self, pstate ):
        """Requires PREV and NEXT to exist, to not be wilderness, and for NEXT to not go up."""
        return ( pstate.elements.get( "PREV" ) and pstate.elements.get( "NEXT" )
         and context.MAP_WILDERNESS not in pstate.elements["PREV"].desctags
         and context.MAP_WILDERNESS not in pstate.elements["NEXT"].desctags
         and context.MAP_GOUP not in pstate.elements["NEXT"].desctags )

    def custom_init( self, nart ):
        prev = self.elements[ "PREV" ]
        next = self.elements[ "NEXT" ]

        self.move_element( next, prev )

        myzone1 = self.register_element( "_P_ROOM", nart.get_map_generator( prev ).DEFAULT_ROOM(tags=(context.GOAL,)), "PREV" )
        myzone2 = self.register_element( "_N_ROOM", nart.get_map_generator( next ).DEFAULT_ROOM(tags=(context.ENTRANCE,)), "NEXT" )

        # Depending on whether we're going to a sharp room (with a guaranteed
        # border wall) or another room type, either go with the wall-mounted
        # default stairs or the free-standing spiral stairs.
        if isinstance( myzone1, randmaps.rooms.SharpRoom ):
            stairs_1 = waypoints.StairsDown()
        else:
            stairs_1 = waypoints.SpiralStairsDown()

        if isinstance( myzone2, randmaps.rooms.SharpRoom ):
            stairs_2 = waypoints.StairsUp()
        else:
            stairs_2 = waypoints.SpiralStairsUp()

        stairs_1.destination = next
        stairs_1.otherside = stairs_2
        stairs_2.destination = prev
        stairs_2.otherside = stairs_1

        myzone1.contents.append( stairs_1 )
        myzone2.contents.append( stairs_2 )
        return True

class WildsToWilds( Plot ):
    LABEL = "CONNECT"
    @classmethod
    def matches( self, pstate ):
        """Requires PREV and NEXT to exist, to both be wilderness."""
        return ( pstate.elements.get( "PREV" ) and pstate.elements.get( "NEXT" )
         and context.MAP_WILDERNESS in pstate.elements["PREV"].desctags
         and context.MAP_WILDERNESS in pstate.elements["NEXT"].desctags )

    def custom_init( self, nart ):
        prev = self.elements[ "PREV" ]
        next = self.elements[ "NEXT" ]

        self.move_element( next, prev )

        myzone1 = self.register_element( "_P_ROOM",
         nart.get_map_generator( prev ).DEFAULT_ROOM(tags=(context.GOAL,context.CIVILIZED,context.MAP_ON_EDGE)), "PREV" )
        myzone2 = self.register_element( "_N_ROOM",
         nart.get_map_generator( next ).DEFAULT_ROOM(tags=(context.ENTRANCE,context.CIVILIZED,context.MAP_ON_EDGE)), "NEXT" )

        stairs_1 = waypoints.RoadSignForward()
        stairs_2 = waypoints.RoadSignBack()

        stairs_1.destination = next
        stairs_1.otherside = stairs_2
        stairs_2.destination = prev
        stairs_2.otherside = stairs_1

        myzone1.contents.append( stairs_1 )
        myzone2.contents.append( stairs_2 )
        return True

###   **************************
###   ***   PREFAB_CONNECT   ***
###   **************************
###
### Connect PREV to NEXT, but the doorway in PREV already exists. Just connect
### the provided OTHERSIDE waypoint to a gateway on this side.

class PrefabToWilds( Plot ):
    LABEL = "PREFAB_CONNECT"
    @classmethod
    def matches( self, pstate ):
        """Requires PREV, NEXT, and OTHERSIDE to exist, to both be wilderness."""
        return ( pstate.elements.get( "PREV" ) and pstate.elements.get( "NEXT" )
         and pstate.elements.get( "OTHERSIDE" )
         and context.MAP_WILDERNESS in pstate.elements["PREV"].desctags
         and context.MAP_WILDERNESS in pstate.elements["NEXT"].desctags )

    def custom_init( self, nart ):
        prev = self.elements[ "PREV" ]
        next = self.elements[ "NEXT" ]

        self.move_element( next, prev )

        myzone2 = self.register_element( "_N_ROOM",
         nart.get_map_generator( next ).DEFAULT_ROOM(tags=(context.ENTRANCE,context.CIVILIZED,context.MAP_ON_EDGE)), "NEXT" )

        stairs_1 = self.elements[ "OTHERSIDE" ]
        stairs_2 = waypoints.RoadSignBack()

        stairs_1.destination = next
        stairs_1.otherside = stairs_2
        stairs_2.destination = prev
        stairs_2.otherside = stairs_1

        myzone2.contents.append( stairs_2 )
        return True



###   **************************
###   ***   SECRET_CONNECT   ***
###   **************************
###  A secret connection works like above, but the entrance isn't obvious.
###  Usually some kind of puzzle needs to be solved before the entrance can be
###  used.

class SecretTreeStumpEntrance( Plot ):
    # There's a secret door in a tree stump. However, the player needs a way to
    # open it...
    LABEL = "SECRET_CONNECT"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires PREV and NEXT to exist, and for PREV to be forest."""
        return ( pstate.elements.get( "PREV" ) and pstate.elements.get( "NEXT" )
         and context.HAB_FOREST is pstate.elements["PREV"].biome )
    def seek_entrance_room( self, thing ):
        # We need a room that is marked as an entrance.
        return isinstance( thing, randmaps.Room ) and context.ENTRANCE in thing.tags
    def custom_init( self, nart ):
        prev = self.elements[ "PREV" ]
        next = self.elements[ "NEXT" ]
        self.move_element( next, prev )
        myzone1 = self.register_element( "_P_ROOM", nart.get_map_generator( prev ).DEFAULT_ROOM(tags=(context.GOAL,)), "PREV" )
        myzone2 = self.seek_element( nart, "_N_ROOM", self.seek_entrance_room, scope=next, check_subscenes=False, must_find=False )
        if not myzone2:
            myzone2 = self.register_element( "_N_ROOM", randmaps.rooms.SharpRoom(tags=(context.ENTRANCE,)), "NEXT" )
        stairs_1 = waypoints.TreeStump()
        stairs_1.mini_map_label = "Tree Stump"
        stairs_1.plot_locked = True
        stairs_2 = waypoints.GateDoor()
        stairs_2.mini_map_label = "Exit"
        self.stump_destination = next
        self.stump_otherside = stairs_2
        stairs_2.destination = prev
        stairs_2.otherside = stairs_1
        self.register_element( "TARGET", stairs_1, "_P_ROOM" )
        self.register_element( "_EXIT", stairs_2, "_N_ROOM" )
        self._stump_unlocked = False
        self.add_sub_plot( nart, "PB_OPEN", PlotState().based_on( self ) )
        return True
    def use_stump( self, explo ):
        explo.camp.destination = self.stump_destination
        explo.camp.entrance = self.stump_otherside
    def TARGET_OPEN( self, explo ):
        self._stump_unlocked = True
    def TARGET_menu( self, thingmenu ):
        if self._stump_unlocked:
            thingmenu.desc = "{0} There's a secret door in it.".format( thingmenu.desc )
            thingmenu.add_item( "Enter the stump.", self.use_stump )
            thingmenu.add_item( "Leave it alone.", None )
        else:
            thingmenu.desc = "{0} There's something odd about it.".format( thingmenu.desc )
    def get_dialogue_grammar( self, npc, explo ):
        """Generate a rumour."""
        if not self._stump_unlocked:
            prev = self.elements["PREV"]
            if explo.scene == prev or explo.camp.current_root_scene() == prev:
                mygram = {
                    "[RUMOUR]": ["I saw a person disappear through a tree stump. Mysterious."],
                }
                return mygram

class ThroughTheWell( Plot ):
    LABEL = "SECRET_CONNECT"
    UNIQUE = True
    active = True
    scope = True
    NAME_PATTERNS = ( "{0} Undercity", "{0} Sewer", "Tunnels of {1}", "{0} Waterworks" )
    @classmethod
    def matches( self, pstate ):
        """Requires PREV and NEXT to exist, PREV to be wilderness."""
        return ( pstate.elements.get( "PREV" ) and pstate.elements.get( "NEXT" )
         and context.MAP_WILDERNESS in pstate.elements["PREV"].desctags )
    def seek_well( self, thing ):
        # We need a well that is not plot_locked.
        return isinstance( thing, waypoints.Well ) and not thing.plot_locked
    def seek_entrance_room( self, thing ):
        # We need a room that is marked as an entrance.
        return isinstance( thing, randmaps.Room ) and context.ENTRANCE in thing.tags
    def custom_init( self, nart ):
        prev = self.elements[ "PREV" ]
        next = self.elements[ "NEXT" ]
        well = self.seek_element( nart, "_WELL", self.seek_well, scope=prev, check_subscenes=False )
        well.plot_locked = True
        myzone2 = self.seek_element( nart, "_N_ROOM", self.seek_entrance_room, scope=next, check_subscenes=False, must_find=False )
        if not myzone2:
            myzone2 = self.register_element( "_N_ROOM", randmaps.rooms.SharpRoom(tags=(context.ENTRANCE,)), "NEXT" )
        stairs_2 = waypoints.GateDoor()
        self.register_element( "_EXIT", stairs_2, "_N_ROOM" )
        self._the_well_has_been_used = False
        if next.rank > prev.rank:
            # We're gonna add a dungeon.
            self.levels = list()
            pstate = PlotState( elements={"DUNGEON_TYPE":(context.HAB_TUNNELS,context.DES_WATER)} ).based_on( self )
            for l in range( prev.rank+1, next.rank+1 ):
                pstate.rank = l
                sp = self.add_sub_plot( nart, "DUNGEON_LEVEL", pstate )
                if sp:
                    self.levels.append( sp.elements[ "LOCALE" ] )

            # Decide on a good name.
            dname = random.choice( self.NAME_PATTERNS ).format( prev, namegen.random_style_name() )

            # Connect all the levels, and name them.
            prv = self.levels[0]
            prv.name = "{0}, Lvl{1}".format( dname, 1 )
            if len( self.levels ) > 1:
                n = 2
                for nxt in self.levels[1:]:
                    nxt.name = "{0}, Lvl{1}".format( dname, n )
                    n += 1
                    pstate = PlotState( rank = nxt.rank, elements={"PREV":prv,"NEXT":nxt} ).based_on( self )
                    sp = self.add_sub_plot( nart, "CONNECT", pstate )
                    prv = nxt

            # Connect to well and black market.
            stairs_3 = waypoints.StairsUp()
            stairs_4 = waypoints.StairsDown()
            myzone_3 = randmaps.rooms.SharpRoom(tags=(context.ENTRANCE,),parent=self.levels[0])
            myzone_4 = randmaps.rooms.SharpRoom(tags=(context.GOAL,),parent=self.levels[-1])
            myzone_3.contents.append( stairs_3 )
            myzone_4.contents.append( stairs_4 )

            self.well_destination = self.levels[0]
            self.well_otherside = stairs_3
            stairs_3.destination = prev
            stairs_3.otherside = well

            stairs_2.destination = self.levels[-1]
            stairs_2.otherside = stairs_4
            stairs_4.destination = next
            stairs_4.otherside = stairs_2
            self.move_element( next, self.levels[-1] )
            self.move_element( self.levels[0], prev )
        else:
            self.well_destination = next
            self.well_otherside = stairs_2
            stairs_2.destination = prev
            stairs_2.otherside = well
            self.move_element( next, prev )
        return True
    def use_well( self, explo ):
        explo.camp.destination = self.well_destination
        explo.camp.entrance = self.well_otherside
        self._the_well_has_been_used = True
    def _WELL_menu( self, thingmenu ):
        thingmenu.desc = "{0} There is a ladder inside, descending into darkness.".format( thingmenu.desc )
        thingmenu.add_item( "Climb down the well.", self.use_well )
        thingmenu.add_item( "Leave it alone.", None )
    def get_dialogue_grammar( self, npc, explo ):
        """Generate a rumour."""
        if not self._the_well_has_been_used:
            prev = self.elements["PREV"]
            if explo.scene == prev or explo.camp.current_root_scene() == prev:
                mygram = {
                    "[RUMOUR]": ["Sometimes I hear strange noises coming from the well."],
                }
                return mygram


