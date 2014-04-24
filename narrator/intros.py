
from plots import Plot,PlotError,Chapter
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
import worlds

""" The INTRO is divided into two parts. INTRO_1 sets the setting and maybe
    also changes the Propp state. INTRO_2 is the branch to the first chapter;
    it may further alter the story state, and is responsible for setting up the
    starting city + campaign entrance position via the LOCALE subplot.

    The INTRO creates the first chapter.

    The INTRO creates both the LOCALE and the COMPLICATION.
"""

class OurFineCity( Plot ):
    """After an age of war, this city is looking up."""
    LABEL = "INTRO_1"
    propp = context.PROPP_ABSENTATION
    setting = context.SET_RENFAN
    active = True
    scope = True
    do_message = True
    @classmethod
    def matches( self, pstate ):
        """Requires the setting to be None or RenFan."""
        if pstate.setting in (None,context.SET_RENFAN):
            return True
    def custom_init( self, nart ):
        """Create the world + chapter + city, then load INTRO_2"""
        w = worlds.World()
        self.chapter = Chapter( world=w )
        self.add_first_locale_sub_plot( nart )
        self.add_sub_plot( nart, "INTRO_2", ident="next" )
        return True
    def t_START( self, explo ):
        if self.do_message:
            city = self.elements["LOCALE"]
            explo.alert( "After centuries of war and darkness, the great city of {0} has risen as a beacon of peace and enlightenment.".format( city.name ) )
            self.subplots["next"].active = True
            self.subplots["next"].t_START( explo )
            self.do_message = False

class BalrogMovesIntoTown( Plot ):
    """The peace is shattered by a monster arriving."""
    LABEL = "INTRO_2"
    propp = context.PROPP_VIOLATION
    scope = True
    do_message = True
    @classmethod
    def matches( self, pstate ):
        """Requires the propp to be INTERDICTION, MACGUFFIN to exist."""
        return pstate.propp in ( context.PROPP_NONE, context.PROPP_ABSENTATION )
    def custom_init( self, nart ):
        # Create the monster, load the complication.
        # Make sure a LOCALE exists; if not, create one.
        if not nart.camp.scene:
            self.add_first_locale_sub_plot( nart )
        self.add_sub_plot( nart, "COMPLICATION", ident="next" )
        self._welcomed = False
        return True
    def t_START( self, explo ):
        if self.do_message:
            city = self.elements["LOCALE"]
            explo.alert( "Unfortunately, the arrival of a fearsome monster has shattered the peace. Now the people of {0} live in fear, waiting for a hero to deliver them from this terror.".format( city.name ) )
            self.do_message = False

    def get_generic_offers( self, npc, explo ):
        ol = list()
        city = self.elements["LOCALE"]
        if explo.camp.current_root_scene() is city and not self._welcomed:
            ol.append( dialogue.Offer( msg = "Welcome to {0}, but you have picked a ".format( city ),
                     context = context.ContextTag( [context.HELLO,context.LOCAL] )))
        return ol




