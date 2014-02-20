
from plots import Plot
import context

class LightOfTheMacguffin( Plot ):
    LABEL = "INTRO_1"
    @classmethod
    def matches( self, pstate ):
        """Requires the setting to be None or RenFan."""
        if pstate.setting in (context.SET_EVERY,context.SET_RENFAN):
            return True


class OurMacguffinIsGone( Plot ):
    LABEL = "INTRO_2"
    @classmethod
    def matches( self, pstate ):
        """Requires the setting to be None or RenFan."""
        if pstate.setting in (context.SET_EVERY,context.SET_RENFAN):
            return True

