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
import random

""" The complication is the main part of the chapter, taking the setup from the
    INTRO and leading into the difficulties separating the pcs from the
    conclusion.
"""

class CaveDungeon( Plot ):
    LABEL = "COMPLICATION"
    NAME_PATTERNS = ( "Caverns of {0}", "Caves of {0}" )
    def custom_init( self, nart ):
        """Load dungeon levels, dungeon entrance, CONCLUSION."""
        self.levels = list()
        pstate = PlotState( rank = self.chapter.start_rank, elements={"DUNGEON_TYPE":(context.HAB_CAVE,)} ).based_on( self )
        for l in range( self.chapter.start_rank, self.chapter.end_rank+1 ):
            sp = self.add_sub_plot( nart, "DUNGEON_LEVEL", pstate )
            if sp:
                pstate.rank = l
                pstate.elements["DUNGEON_TYPE"] = sp.TAGS
                dunglev = sp.elements[ "LOCALE" ]
                self.levels.append( dunglev )

        # Decide on a good name.
        dname = random.choice( self.NAME_PATTERNS ).format( namegen.random_style_name() )

        # Connect all the levels, and name them.
        prev = self.elements[ "LOCALE" ]
        n = 1
        for next in self.levels:
            next.name = "{0}, Lvl{1}".format( dname, n )
            n += 1
            pstate = PlotState( rank = next.rank, elements={"PREV":prev,"NEXT":next} ).based_on( self )
            sp = self.add_sub_plot( nart, "CONNECT", pstate )
            prev = next

        return True

