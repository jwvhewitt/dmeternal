
from plots import Plot,PlotError,Chapter,PlotState
import context
import items
import maps
import waypoints
import monsters
import dialogue
import services
import teams
import characters
import namegen
import worlds


#
# This unit contains the one and only ADVSTUB plot. This is the first plot
# initialized in the adventure, and its only purpose is to load all of the other
# adventure components. Yay ADVSTUB!
#

class BardicStub( Plot ):
    LABEL = "STUB_BARDIC"
    # Creates a simple, plot-free dungeon adventure.

    def custom_init( self, nart ):
        """Create the world + chapter + city, then load INTRO_2"""
        w = worlds.World()
        nart.camp.contents.append( w )
        self.register_element( "WORLD", w )
        self.chapter = Chapter( world=w )
        self.add_first_locale_sub_plot( nart )

        sp = self.add_sub_plot( nart, "INTRO_1" )

        for job in characters.PC_CLASSES:
            self.add_sub_plot( nart, "RESOURCE_JOBTRAINER", PlotState( elements={"JOB":job} ) )

        self.add_sub_plot( nart, "TESTPLOT", spstate=PlotState().based_on(sp), necessary=False )

        return True


class AdventureStub( Plot ):
    LABEL = "ADVSTUB"

    def custom_init( self, nart ):
        """Create the world + chapter + city, then load INTRO_2"""
        w = worlds.World()
        nart.camp.contents.append( w )
        self.register_element( "WORLD", w )
        self.chapter = Chapter( world=w )
        self.add_first_locale_sub_plot( nart )

        sp = self.add_sub_plot( nart, "INTRO_1" )

        for job in characters.PC_CLASSES:
            self.add_sub_plot( nart, "RESOURCE_JOBTRAINER", PlotState( elements={"JOB":job} ) )

        self.add_sub_plot( nart, "TESTPLOT", spstate=PlotState().based_on(sp), necessary=False )

        return True

