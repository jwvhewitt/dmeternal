from .plots import Plot,PlotError,PlotState
from .. import context
from .. import items
from .. import maps
from .. import waypoints
from .. import monsters
from .. import dialogue
from .. import services
from .. import teams
from .. import characters
from .. import namegen
import random

""" The complication is the main part of the chapter, taking the setup from the
    INTRO and leading into the difficulties separating the pcs from the
    conclusion.
"""

class CaveDungeon( Plot ):
    LABEL = "COMPLICATION"
    NAME_PATTERNS = ( "Caverns of {0}", "Caves of {0}", "{0} Grotto", "{0} Chasm" )
    scope = True
    active = True
    @classmethod
    def matches( self, pstate ):
        """Requires the propp to be INTERDICTION, MACGUFFIN to exist."""
        return pstate.propp in ( context.PROPP_NONE, context.PROPP_ABSENTATION, context.PROPP_VIOLATION,
            context.PROPP_RECONNAISSANCE, context.PROPP_COMPLICITY, context.PROPP_COUNTERACT,
            context.PROPP_GUIDANCE, context.PROPP_STRUGGLE, context.PROPP_VICTORY )
    def custom_init( self, nart ):
        """Load dungeon levels, dungeon entrance, CONCLUSION."""
        # Generate the levels
        self.levels = self.get_dungeon_levels( nart, (context.HAB_CAVE,), self.chapter.start_rank, self.chapter.end_rank )
        # Decide on a good name.
        self.dname = random.choice( self.NAME_PATTERNS ).format( namegen.random_style_name() )
        # Connect all the levels, and name them.
        self.install_dungeon( nart, self.levels, self.elements[ "LOCALE" ], self.dname )

        # Load the conclusion.
        self.add_sub_plot( nart, "CONCLUSION", PlotState(rank=self.chapter.end_rank,elements={"FINAL_DUNGEON":self.levels[-1]}).based_on( self ) )

        return True
    def get_dialogue_grammar( self, npc, explo ):
        if self.chapter.active and explo.camp.current_root_scene() is self.elements["LOCALE"]:
            mygram = {
                "[RUMOUR]": ["[rumourleadin] the [monsters] are coming from the {0}.".format( self.dname )],
            }
            return mygram

