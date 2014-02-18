
from plots import Plot
import context

class LightOfTheMacguffin( Plot ):
    LABEL = "INTRO_1"
    @classmethod
    def matches( self, spreq ):
        """Requires the setting to be None of RenFan."""
