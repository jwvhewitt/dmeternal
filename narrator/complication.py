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

""" The complication is the main part of the chapter, taking the setup from the
    INTRO and leading into the difficulties separating the pcs from the
    conclusion.
"""

class CaveDungeon( Plot ):
    LABEL = "COMPLICATION"
    active = True
    scope = True
    def custom_init( self, nart ):
        """Load dungeon levels, dungeon entrance, CONCLUSION."""
        self.levels = list()
        pstate = PlotState( rank = self.chapter.start_rank, elements={"DUNGEON_TYPE":context.HAB_CAVE} ).based_on( self )
        for l in range( self.chapter.start_rank, self.chapter.end_rank+1 ):
            sp = self.add_sub_plot( nart, "DUNGEON_LEVEL", pstate )
            if sp:
                pstate = PlotState( rank = l ).based_on( sp )
                dunglev = sp.elements[ "SCENE" ]
                self.levels.append( dunglev )

        # Connect all the levels.
        prev = self.elements[ "LOCALE" ]
        for next in self.levels:
            myzone1 = nart.get_map_generator( prev ).DEFAULT_ROOM()
            myzone2 = nart.get_map_generator( next ).DEFAULT_ROOM()

            stairs_1 = waypoints.SpiralStairsDown()
            stairs_2 = waypoints.SpiralStairsUp()
            stairs_1.destination = next
            stairs_1.otherside = stairs_2
            stairs_2.destination = prev
            stairs_2.otherside = stairs_1

            myzone1.contents.append( stairs_1 )
            myzone2.contents.append( stairs_2 )
            prev.contents.append( myzone1 )
            next.contents.append( myzone2 )

            prev = next

        return True

