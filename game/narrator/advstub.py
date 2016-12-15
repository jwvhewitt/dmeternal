
from plots import Plot,PlotError,Chapter,PlotState
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
from .. import worlds


#
# This unit contains the one and only ADVSTUB plot. This is the first plot
# initialized in the adventure, and its only purpose is to load all of the other
# adventure components. Yay ADVSTUB!
#

class NewStyleStub( Plot ):
    LABEL = "ADVENTURE_STUB"
    # Creates a city with upgradeable services and a roadsign to adventure.

    def custom_init( self, nart ):
        """Create the world + starting scene."""
        w = worlds.World()
        nart.camp.contents.append( w )
        self.register_element( "WORLD", w )
        self.chapter = Chapter( world=w )
        self.add_first_locale_sub_plot( nart, locale_type="START_CITY" )

        #for job in characters.PC_CLASSES:
        #    self.add_sub_plot( nart, "RESOURCE_JOBTRAINER", PlotState( elements={"JOB":job} ) )

        return True



