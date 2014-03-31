from plots import Plot,PlotError,PlotState
import context
import items
import maps
import mapgen
import waypoints
import monsters
import dialogue
import services
import teams
import characters
import namegen

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

        myzone1 = self.register_element( "_P_ROOM", mapgen.MountainRoom(tags=(context.GOAL,context.CIVILIZED,)), "PREV" )
        myzone2 = self.register_element( "_N_ROOM", mapgen.SharpRoom(tags=(context.ENTRANCE,)), "NEXT" )

        stairs_1 = waypoints.MineEntrance()
        stairs_2 = waypoints.GateDoor()

        stairs_1.destination = next
        stairs_1.otherside = stairs_2
        stairs_2.destination = prev
        stairs_2.otherside = stairs_1

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

        myzone1 = self.register_element( "_P_ROOM", mapgen.MountainRoom(tags=(context.GOAL,)), "PREV" )
        myzone2 = self.register_element( "_N_ROOM", nart.get_map_generator( next ).DEFAULT_ROOM(tags=(context.ENTRANCE,)), "NEXT" )

        stairs_1 = waypoints.DungeonEntrance()
        if context.MAP_GOUP in next.desctags:
            if isinstance( myzone2, mapgen.SharpRoom ):
                stairs_2 = waypoints.StairsDown()
            else:
                stairs_2 = waypoints.SpiralStairsDown()
        else:
            if isinstance( myzone2, mapgen.SharpRoom ):
                stairs_2 = waypoints.StairsUp()
            else:
                stairs_2 = waypoints.SpiralStairsUp()

        stairs_1.destination = next
        stairs_1.otherside = stairs_2
        stairs_2.destination = prev
        stairs_2.otherside = stairs_1

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

        myzone1 = self.register_element( "_P_ROOM", nart.get_map_generator( prev ).DEFAULT_ROOM(tags=(context.GOAL,)), "PREV" )
        myzone2 = self.register_element( "_N_ROOM", nart.get_map_generator( next ).DEFAULT_ROOM(tags=(context.ENTRANCE,)), "NEXT" )

        # Depending on whether we're going to a sharp room (with a guaranteed
        # border wall) or another room type, either go with the wall-mounted
        # default stairs or the free-standing spiral stairs.
        if isinstance( myzone1, mapgen.SharpRoom ):
            stairs_1 = waypoints.StairsUp()
        else:
            stairs_1 = waypoints.SpiralStairsUp()

        if isinstance( myzone2, mapgen.SharpRoom ):
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

        myzone1 = self.register_element( "_P_ROOM", nart.get_map_generator( prev ).DEFAULT_ROOM(tags=(context.GOAL,)), "PREV" )
        myzone2 = self.register_element( "_N_ROOM", nart.get_map_generator( next ).DEFAULT_ROOM(tags=(context.ENTRANCE,)), "NEXT" )

        # Depending on whether we're going to a sharp room (with a guaranteed
        # border wall) or another room type, either go with the wall-mounted
        # default stairs or the free-standing spiral stairs.
        if isinstance( myzone1, mapgen.SharpRoom ):
            stairs_1 = waypoints.StairsDown()
        else:
            stairs_1 = waypoints.SpiralStairsDown()

        if isinstance( myzone2, mapgen.SharpRoom ):
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


###   **************************
###   ***   SECRET_CONNECT   ***
###   **************************
###  A secret connection works like above, but the entrance isn't obvious.
###  Usually some kind of puzzle needs to be solved before the entrance can be
###  used.

class ThroughTheWell( Plot ):
    LABEL = "SECRET_CONNECT"
    UNIQUE = True
    active = True
    scope = True
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
        return isinstance( thing, mapgen.Room ) and context.ENTRANCE in thing.tags
    def custom_init( self, nart ):
        prev = self.elements[ "PREV" ]
        next = self.elements[ "NEXT" ]
        well = self.seek_element( nart, "_WELL", self.seek_well, scope=prev, check_subscenes=False )
        well.plot_locked = True
        myzone2 = self.seek_element( nart, "_N_ROOM", self.seek_entrance_room, scope=next, check_subscenes=False, must_find=False )
        if not myzone2:
            myzone2 = self.register_element( "_N_ROOM", mapgen.SharpRoom(tags=(context.ENTRANCE,)), "NEXT" )
        stairs_2 = waypoints.GateDoor()
        well.destination = next
        well.otherside = stairs_2
        stairs_2.destination = prev
        stairs_2.otherside = well
        self.register_element( "_EXIT", stairs_2, "_N_ROOM" )
        return True
    def use_well( self, explo ):
        explo.camp.destination = self.elements[ "NEXT" ]
        explo.camp.entrance = self.elements[ "_EXIT" ]
    def _WELL_menu( self, thingmenu ):
        thingmenu.desc = "{0} There is a ladder inside, descending into darkness.".format( thingmenu.desc )
        thingmenu.add_item( "Climb down the well.", self.use_well )
        thingmenu.add_item( "Leave it alone.", None )


