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
        # Generate the levels
        self.levels = self.get_dungeon_levels( nart, (context.HAB_CAVE,), self.chapter.start_rank, self.chapter.end_rank )
        # Decide on a good name.
        dname = random.choice( self.NAME_PATTERNS ).format( namegen.random_style_name() )
        # Connect all the levels, and name them.
        self.install_dungeon( nart, self.levels, self.elements[ "LOCALE" ], dname )
        return True

