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
import random

### Sidestories get added to buildings in cities to flesh them out and to
### provide some things for the PC to do other than clearing the main dungeon.


class DateMyCousinPlease( Plot ):
    """The cousin of the shopkeeper must be removed from the house."""
    LABEL = "SIDE_STORY"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the SHOPKEEPER and BUILDING_INT to exist."""
        return pstate.elements.get("SHOPKEEPER") and pstate.elements.get("SHOPKEEPER").species and pstate.elements.get("BUILDING_INT")
    def custom_init( self, nart ):
        """Create the cousin, add puzzle subplot."""
        the_cousin = monsters.generate_npc(species=self.elements.get("SHOPKEEPER").species.__class__)
        self.register_element( "TARGET", the_cousin )
        self.dated = False
        self.add_sub_plot( nart, "SB_DATE", PlotState().based_on( self ) )
        return True
    def TARGET_DATE( self, explo ):
        self.dated = True

    def _MYNPC_offers( self ):
        ol = list()
        if self.invited:
            npc = self.elements[ "TARGET" ]
            r1 = dialogue.Reply( "Would you like to go out with {0}?".format(npc),
             destination=dialogue.Offer( "{0}? Yes, you may tell {1} that I would like that very much!".format(npc,npc.object_pronoun()),
             effect=self.accept_invitation ) )
            ol.append( dialogue.Offer( "Yes, what is it?" ,
             context = context.ContextTag([context.BRINGMESSAGE,context.QUESTION]),
             replies = [r1,] ) )
        return ol

