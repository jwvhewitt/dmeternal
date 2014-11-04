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

# BARDIC_DUNGEON
#  This subplot will generate a dungeon of a given type. All these subplots
#  should be unique in order to prevent dungeon types from repeating.
#  - Generate dungeon
#  - Generate connection to previous dungeon
#    - Install dungeon
#  - Add chapter resources, as appropriate

class BardicCaves( Plot ):
    LABEL = "BARDIC_DUNGEON"
    NAME_PATTERNS = ( "Caverns of {0}", "Caves of {0}", "{0} Grotto", "{0} Chasm" )
    DUNGEON_PATTERN = (context.HAB_CAVE,)
    UNIQUE = True
    scope = True
    active = True
    def custom_init( self, nart ):
        """Load dungeon levels, and connect this dungeon to the adventure."""
        # Generate the levels
        self.levels = self.get_dungeon_levels( nart, self.DUNGEON_PATTERN, self.chapter.start_rank, self.chapter.end_rank )
        # Decide on a good name.
        self.dname = random.choice( self.NAME_PATTERNS ).format( namegen.random_style_name() )

        # Connect all the levels, and name them.
        self.add_sub_plot( nart, "BARDIC_CONNECTION",
         PlotState(elements={"LEVELS":self.levels,"DNAME":self.dname}).based_on( self ) )

        # Set the PREV_DUNGEON element, for use by the next dungeon.
        self.register_element( "PREV_DUNGEON", self.levels[-1] )

        return True


# BARDIC_CONNECTION
#  This subplot will add a connection for the new bardic dungeon from the
#  previous one. If no dungeons have yet been added, it will just connect to
#  the city scene. Otherwise, it will likely add a boss encounter to the
#  previous dungeon and a new set of resources (shops, etc) for the new level.

class BC_DirectConnection( Plot ):
    """The first dungeon gets directly connected to the LOCALE scene."""
    LABEL = "BARDIC_CONNECTION"
    @classmethod
    def matches( self, pstate ):
        """Requires LOCALE to exist, but no PREV_DUNGEON."""
        return pstate.elements.get( "LOCALE" ) and not pstate.elements.get( "PREV_DUNGEON" )
    def custom_init( self, nart ):
        """Install the dungeon."""
        self.install_dungeon( nart, self.elements[ "LEVELS" ], self.elements[ "LOCALE" ], self.elements["DNAME"] )
        return True




