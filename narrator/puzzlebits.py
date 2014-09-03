from plots import Plot,PlotError,PlotState
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
import random

""" PuzzleBits are atomic actions which can be used to generate random puzzles.
    Generation happens backwards, starting with the end state and stringing
    along actions until the causality chain terminates.

    A PB request will include an element TARGET, which is the thing to be
    affected by the action. When the action is performed, a script trigger
    will be sprung with a trigger ID equal to the action name (minus "PB_")
    and thing set to the target item.
"""


#  *******************
#  ***   PB_OPEN   ***
#  *******************

class OPEN_HintAndSearch( Plot ):
    """The PC will learn there's a secret door in the waypoint, and can then search."""
    LABEL = "PB_OPEN"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET to exist and be a waypoint."""
        # Probably not the best way to do this... probably not important anyhow.
        return pstate.elements.get("TARGET") and isinstance( pstate.elements["TARGET"], waypoints.Waypoint )
    def custom_init( self, nart ):
        """Create the hint, call a get secret subplot."""
        self._learned = False
        target = self.elements["TARGET"]
        if not hasattr( target, "mini_map_label" ):
            target.mini_map_label = "Thingamajig"
        secret = self.register_element( "_MYSECRET", "There's a {0} around here with a secret panel in it.".format( target.mini_map_label ) )
        self.add_sub_plot( nart, "GET_SECRET", PlotState( elements={"TARGET":secret} ).based_on( self ) )
        return True
    def _MYSECRET_SECRET( self, explo ):
        self._learned = True
    def TARGET_menu( self, thingmenu ):
        if self._learned:
            thingmenu.add_item( "Look for the secret panel.", self.use_panel )
    def use_panel( self, explo ):
        explo.alert( "You find the secret panel and open a passageway." )
        explo.check_trigger( "OPEN", self.elements[ "TARGET" ] )
        self.active = False

class OPEN_Lever( Plot ):
    """Pull a switch, open the whatever."""
    LABEL = "PB_OPEN"
    UNIQUE = False
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET to exist."""
        return pstate.elements.get("TARGET")
    def custom_init( self, nart ):
        """Create the lever, call a getter subplot."""
        lever = self.register_element( "_LEVER", waypoints.PuzzleSwitch() )
        self.add_sub_plot( nart, "GET_THING", PlotState( elements={"TARGET":lever} ).based_on( self ) )
        return True
    def _LEVER_USE( self, explo ):
        explo.alert( "You hear a grinding sound in the distance." )
        explo.check_trigger( "OPEN", self.elements[ "TARGET" ] )
        self.active = False


class OPEN_SecretKnock( Plot ):
    """The PC will learn there's a secret knock to open the waypoint."""
    LABEL = "PB_OPEN"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET to exist and be a waypoint."""
        # Probably not the best way to do this... probably not important anyhow.
        return pstate.elements.get("TARGET") and isinstance( pstate.elements["TARGET"], waypoints.Waypoint )
    def custom_init( self, nart ):
        """Create the hint, call a get secret subplot."""
        self._learned = False
        target = self.elements["TARGET"]
        if not hasattr( target, "mini_map_label" ):
            target.mini_map_label = "Thingamajig"
        secret = self.register_element( "_MYSECRET", "To open the {0}, knock three times.".format( target.mini_map_label ) )
        self.add_sub_plot( nart, "GET_SECRET", PlotState( elements={"TARGET":secret} ).based_on( self ) )
        return True
    def _MYSECRET_SECRET( self, explo ):
        self._learned = True
    def TARGET_menu( self, thingmenu ):
        if self._learned:
            thingmenu.add_item( "Knock three times.", self.use_panel )
    def use_panel( self, explo ):
        explo.alert( "You knock on the {0}. Moments later, a secret passageway creaks open.".format( self.elements["TARGET"].mini_map_label) )
        explo.check_trigger( "OPEN", self.elements[ "TARGET" ] )
        self.active = False



