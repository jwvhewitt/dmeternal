
from plots import Plot,PlotError
import context

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
        """Load *INTRO_2"""


class OurMacguffinIsGone( Plot ):
    LABEL = "INTRO_2"
    @classmethod
    def matches( self, pstate ):
        """Requires the setting to be None or RenFan."""
        if pstate.propp == context.PROPP_INTERDICTION:
            return True

