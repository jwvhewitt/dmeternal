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

""" SocialBits are atomic actions which can be used to generate random puzzles.
    Unlike the PuzzleBits, these all involve conversations with NPCs.
    Generation happens backwards, starting with the end state and stringing
    along actions until the causality chain terminates.

    A SB request will include an element TARGET, which is the thing to be
    affected by the action. When the action is performed, a script trigger
    will be sprung with a trigger ID equal to the action name (minus "SB_")
    and thing set to the target item.
"""

###   *****************
###   ***  SB_DATE  ***
###   *****************

class DATE_LowStandards( Plot ):
    """Creates a NPC who will date the TARGET if TARGET sent invitation."""
    LABEL = "SB_DATE"
    UNIQUE = True
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
        self.add_sub_plot( nart, "SB_DATEINVITE", PlotState( elements={"TARGET":npc2, "ORIGIN":npc1} ).based_on( self ) )
        return True
    def _MYNPC_DATEINVITE( self, explo ):
        self.invited = True
    def accept_invitation( self, explo ):
        explo.check_trigger( "DATE", self.elements[ "TARGET" ] )
        self.active = False
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

class DATE_WaitingForAnInvitation( Plot ):
    """Creates a NPC who will date the TARGET if TARGET sent invitation."""
    LABEL = "SB_DATE"
    UNIQUE = True
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
        self.register_element( "ORIGIN", npc2 )
        self.add_sub_plot( nart, "SB_DATEINVITE", PlotState().based_on( self ) )
        return True
    def TARGET_DATEINVITE( self, explo ):
        self.invited = True
    def accept_invitation( self, explo ):
        explo.check_trigger( "DATE", self.elements[ "TARGET" ] )
        self.active = False
    def TARGET_offers( self ):
        ol = list()
        if self.invited:
            npc = self.elements[ "ORIGIN" ]
            r1 = dialogue.Reply( "Would you like to go out with {0}?".format(npc),
             destination=dialogue.Offer( "{0}? Yes, you may tell {1} that I would like that very much!".format(npc,npc.object_pronoun()),
             effect=self.accept_invitation ) )
            ol.append( dialogue.Offer( "Yes, what is it?" ,
             context = context.ContextTag([context.BRINGMESSAGE,context.QUESTION]),
             replies = [r1,] ) )
        return ol


###   ***********************
###   ***  SB_DATEINVITE  ***
###   ***********************

class DI_Admirer( Plot ):
    """ORIGIN will send invitation to TARGET because TARGET is awesome."""
    LABEL = "SB_DATEINVITE"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET to exist."""
        return pstate.elements.get("TARGET") and pstate.elements.get("ORIGIN")
    def ask_invitation( self, explo ):
        explo.check_trigger( "DATEINVITE", self.elements[ "TARGET" ] )
        self.active = False
    def ORIGIN_offers( self ):
        ol = list()
        npc = self.elements.get("TARGET")
        ol.append( dialogue.Offer( "{0} is cute and awesome, and I don't care who knows! I'd tell {1} myself, but I'm too scared...".format( npc, npc.object_pronoun() ),
         context = context.ContextTag([context.INFO,context.PERSONAL]),
         effect=self.ask_invitation ) )
        return ol

class DI_MysteryDate( Plot ):
    """ORIGIN will send invitation to TARGET if TARGET is lovelorn."""
    LABEL = "SB_DATEINVITE"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET to exist."""
        return pstate.elements.get("TARGET") and pstate.elements.get("ORIGIN")
    def custom_init( self, nart ):
        """Create the NPC, add the two puzzle subplots."""
        self.add_sub_plot( nart, "SB_LOVELORN", PlotState().based_on( self ) )
        self._interested = False
        self._told_problem = False
        return True
    def TARGET_LOVELORN( self, explo ):
        self._interested = True
    def ask_invitation( self, explo ):
        explo.check_trigger( "DATEINVITE", self.elements[ "TARGET" ] )
        self.active = False
    def tell_problem( self, explo ):
        self._told_problem = True
    def ORIGIN_offers( self ):
        ol = list()
        npc = self.elements.get("TARGET")
        if self._interested and self._told_problem:
            r1 = dialogue.Reply( "{0} would like to go out with you.".format(npc),
             destination=dialogue.Offer( "Really? Great! Could you bring {0} my invitation?".format(npc.object_pronoun()),
             effect=self.ask_invitation ) )
            ol.append( dialogue.Offer( "Yes, what is it?" ,
             context = context.ContextTag([context.BRINGMESSAGE,context.GOODNEWS]),
             replies = [r1,] ) )
        else:
            myoffer = dialogue.Offer( "I would like to ask someone to the festival dance, but I don't know anyone..." ,
             context = context.ContextTag([context.PROBLEM,context.PERSONAL]), effect=self.tell_problem )
            ol.append( myoffer )
            if self._interested:
                myoffer.replies.append( dialogue.Reply( "Why don't you ask {0}?".format(npc),
                 destination=dialogue.Offer( "Would {0} be interested in going with me? I cannot leave here right now; could you deliver my invitation?".format(npc.subject_pronoun()),
                 effect=self.ask_invitation ) ) )
        return ol

###   *********************
###   ***  SB_LOVELORN  ***
###   *********************

class LL_LonelyPlanet( Plot ):
    """TARGET will express the desire to meet someone."""
    LABEL = "SB_LOVELORN"
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





