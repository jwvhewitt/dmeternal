from .plots import Plot,PlotError,PlotState
from .. import context
from .. import items
from .. import maps
from .. import randmaps
from .. import waypoints
from .. import monsters
from .. import dialogue
from .. import services
from .. import teams
from .. import characters
from .. import namegen
import random
from .. import monsters

# The aftermath of the conclusion. There are two types of resolution: If we
# are at the final rank, an "_E" resolution will be loaded. Otherwise, a "_C"
# continuation resolution will be loaded. This continuation serves a similar
# purpose to the INTRO- it creates and populates the next chapter of the story.



#   ***************************
#   ***   RESOLVE_FIGHT_C   ***
#   ***************************


#   ***************************
#   ***   RESOLVE_FIGHT_E   ***
#   ***************************

class DingDongTheBalrogIsDead( Plot ):
    """Now that this one enemy is dead, everything is going to be okay, right?"""
    LABEL = "RESOLVE_FIGHT_E"
    propp = context.PROPP_VICTORY
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the ENEMY to exist."""
        return pstate.elements.get( "ENEMY" )
    def activate( self, explo ):
        self.chapter.activate()
        explo.alert( "With {0} defeated, peace soon returns to the land.".format( self.elements["ENEMY"] ) )
        champs = list()
        losers = list()
        for pc in explo.camp.party:
            if pc.is_alright():
                champs.append( str(pc) )
            else:
                losers.append( str(pc) )
        explo.alert( "The legend of {0} shall live eternally!".format( ", ".join(champs) ) )
        if losers:
            if len( losers ) > 1:
                explo.alert( "Unlike the legend of {0}... who cares about those chumps?".format( ", ".join(losers) ) )
            else:
                explo.alert( "Unlike the legend of {0}... who cares about that chump?".format( losers[0] ) )
        explo.alert( "Thanks for playing Dungeon Monkey Eternal. You can follow development at www.gearheadrpg.com, or via @Pyrro12 on Twitter." )




