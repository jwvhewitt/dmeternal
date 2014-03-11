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


class CaveLevel( Plot ):
    LABEL = "DUNGEON_LEVEL"
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the dungeon level to be a cave."""
        return pstate.elements.get( "DUNGEON_TYPE" ) == context.HAB_CAVE
    def custom_init( self, nart ):

        return True

