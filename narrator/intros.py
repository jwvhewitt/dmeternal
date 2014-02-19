
from plots import Plot
import context

class LightOfTheMacguffin( Plot ):
    LABEL = "INTRO_1"
    @classmethod
    def matches( self, pstate ):
        """Requires the setting to be None of RenFan."""
        if pstate.setting in (context.SET_EVERY,context.SET_RENFAN):
            return True


