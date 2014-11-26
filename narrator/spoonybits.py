from plots import Plot,PlotError,PlotState
import context
import items
import maps
import randmaps
import waypoints
import monsters
import dialogue
import services
import teams
import characters
import namegen
import random
import cutscene

# SPOONY_CLIMAX
#  This is the first subplot generated, and so starts the ball rolling.
#  It contains a LOCALE element for the final challenge of a chapter, and
#  generates a CLIMAX trigger upon completion.

class CallingCthulu( Plot ):
    """The first dungeon gets directly connected to the LOCALE scene."""
    LABEL = "BARDIC_CONNECTION"
    @classmethod
    def matches( self, pstate ):
        """Requires NEXT_CLIMAX to not exist; this plot only loaded at end of game."""
        return not pstate.elements.get( "NEXT_CLIMAX" )
    def custom_init( self, nart ):
        """Create the climax level."""
        self.install_dungeon( nart, self.elements[ "LEVELS" ], self.elements[ "LOCALE" ], self.elements["DNAME"] )
        return True

