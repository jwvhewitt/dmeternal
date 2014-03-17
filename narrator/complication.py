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
            pstate = PlotState( rank = next.rank, elements={"PREV":prev,"NEXT":next} ).based_on( self )
            sp = self.add_sub_plot( nart, "CONNECT", pstate )
            prev = next

        return True

