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

class LowStandards( Plot ):
    """Creates a NPC who will date the TARGET if TARGET sent invitation."""
    LABEL = "PB_DATE"
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET to exist."""
        return pstate.elements.get("TARGET")

    def custom_init( self, nart ):
        """Create the NPC, add the two puzzle subplots."""
        sp = self.add_sub_plot( nart, "RESOURCE_LOVEINTEREST" )
        npc1 = self.elements[ "TARGET" ]
        npc2 = sp.elements[ "RESOURCE" ]
        self.invited = False
        self.register_element( "_MYNPC", npc2 )

        self.add_sub_plot( nart, "PB_DATEINVITE", PlotState( elements={"TARGET":npc2, "ORIGIN":npc1} ).based_on( self ) )

        return True

    def _MYNPC_DATEINVITE( self, explo ):
        self.invited = True

    def _MYNPC_offers( self ):
        ol = list()
        return ol

###   *********************
###   ***  PB_LOVELORN  ***
###   *********************

class LL_LonelyPlanet( Plot ):
    """TARGET will express the desire to meet someone."""
    LABEL = "PB_LOVELORN"
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET to exist."""
        return pstate.elements.get("TARGET")

    def desire_expressed( self, explo ):
        explo.check_trigger( "LOVELORN", self.elements[ "TARGET" ] )
        self.active = False

    def TARGET_offers( self ):
        ol = list()
        ol.append( dialogue.Offer( "It's a lonely life out here... I wish I had someone to do fun things with." ,
         context = context.ContextTag([context.HELLO,]), effect=self.desire_expressed ) )
        return ol


###   ***********************
###   ***  PB_DATEINVITE  ***
###   ***********************

class MysteryDate( Plot ):
    """ORIGIN will send invitation to TARGET if TARGET is lovelorn."""
    LABEL = "PB_DATEINVITE"
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET to exist."""
        return pstate.elements.get("TARGET") and pstate.elements.get("ORIGIN")

    def custom_init( self, nart ):
        """Create the NPC, add the two puzzle subplots."""
        self.add_sub_plot( nart, "PB_LOVELORN", PlotState().based_on( self ) )
        self._interested = False
        return True

    def TARGET_LOVELORN( self, explo ):
        self._interested = True

    def ORIGIN_offers( self ):
        ol = list()
        ol.append( dialogue.Offer( "I would like to ask someone to the festival dance, but I don't know anyone..." ,
         context = context.ContextTag([context.HELLO,]) ) )
        return ol




