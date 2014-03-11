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

        # Connect all the levels.
        prev = None
        for next in self.levels:
            pass
        return True

