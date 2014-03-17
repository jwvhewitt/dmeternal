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

        myzone1 = self.register_element( "_P_ROOM", mapgen.MountainRoom(tags=(context.CIVILIZED,)), "PREV" )
        myzone2 = self.register_element( "_N_ROOM", mapgen.SharpRoom(), "NEXT" )

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

        myzone1 = self.register_element( "_P_ROOM", mapgen.MountainRoom(), "PREV" )
        myzone2 = self.register_element( "_N_ROOM", nart.get_map_generator( next ).DEFAULT_ROOM(), "NEXT" )

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

        myzone1 = self.register_element( "_P_ROOM", nart.get_map_generator( prev ).DEFAULT_ROOM(), "PREV" )
        myzone2 = self.register_element( "_N_ROOM", nart.get_map_generator( next ).DEFAULT_ROOM(), "NEXT" )

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

        myzone1 = self.register_element( "_P_ROOM", nart.get_map_generator( prev ).DEFAULT_ROOM(), "PREV" )
        myzone2 = self.register_element( "_N_ROOM", nart.get_map_generator( next ).DEFAULT_ROOM(), "NEXT" )

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


