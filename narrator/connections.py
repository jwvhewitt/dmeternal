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

class DefaultGoDown( Plot ):
    LABEL = "CONNECT"
    def custom_init( self, nart ):
        prev = self.elements[ "PREV" ]
        next = self.elements[ "NEXT" ]

        myzone1 = self.register_element( "_P_ROOM", nart.get_map_generator( prev ).DEFAULT_ROOM(), "PREV" )
        myzone2 = self.register_element( "_N_ROOM", nart.get_map_generator( next ).DEFAULT_ROOM(), "NEXT" )

        stairs_1 = waypoints.SpiralStairsDown()
        stairs_2 = waypoints.SpiralStairsUp()
        stairs_1.destination = next
        stairs_1.otherside = stairs_2
        stairs_2.destination = prev
        stairs_2.otherside = stairs_1

        myzone1.contents.append( stairs_1 )
        myzone2.contents.append( stairs_2 )
        return True


