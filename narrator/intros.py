
from plots import Plot,PlotError
import context
import items

class LightOfTheMacguffin( Plot ):
    LABEL = "INTRO_1"
    propp = context.PROPP_INTERDICTION
    setting = context.SET_RENFAN
    @classmethod
    def matches( self, pstate ):
        """Requires the setting to be None or RenFan."""
        if pstate.setting in (None,context.SET_RENFAN):
            return True
    def custom_init( self, nart ):
        """Load *INTRO_2, create MACGUFFIN"""
        self.register_element( "MACGUFFIN", items.choose_item() )
        self.add_sub_plot( nart, "INTRO_2", ident="next" )
        return True

class OurMacguffinIsGone( Plot ):
    LABEL = "INTRO_2"
    @classmethod
    def matches( self, pstate ):
        """Requires the propp to be INTERDICTION, MACGUFFIN to exist."""
        print pstate.propp
        print pstate.elements
        return pstate.propp == context.PROPP_INTERDICTION and pstate.elements.get( "MACGUFFIN" )


