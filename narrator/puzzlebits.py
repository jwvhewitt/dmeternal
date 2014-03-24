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

""" PuzzleBits are atomic actions which can be used to generate random puzzles.
    Generation happens backwards, starting with the end state and stringing
    along actions until the causality chain terminates.

    A PB request will include an element TARGET, which is the thing to be
    affected by the action. When the action is performed, a script trigger
    will be sprung with a trigger ID equal to the action name (minus "PB_")
    and thing set to the target item.
"""

###   *****************
###   ***  PB_DATE  ***
###   *****************

class HighStandards( Plot ):
    """Creates a NPC who will date the TARGET if TARGET sent invitation and has
       had a makeover."""
    LABEL = "PB_DATE"
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET to exist."""
        return pstate.elements.get("TARGET")

    def custom_init( self, nart ):
        """Create the chapter + city, then load INTRO_2"""
        self.chapter = Chapter()
        self.add_first_locale_sub_plot( nart )
        self.add_sub_plot( nart, "INTRO_2", ident="next" )
        return True





