
from plots import Plot
import collections



class Narrative( object ):
    """The builder class which constructs a campaign."""
    def __init__( self, camp ):
        self.camp = camp
        # Add the seed plot.

    def generate_sub_plot( self, pstate, label ):
        """Locate a plot which matches the request, init it, and return it."""

    def build( self ):
        """Build finished campaign from this narrative."""


# The list of plots will be stored as a dictionary based on label.
PLOT_LIST = collections.defaultdict( list )
def harvest( mod ):
    for name in dir( mod ):
        o = getattr( mod, name )
        if inspect.isclass( o ) and issubclass( o , Plot ) and o is not Plot:
            PLOT_LIST[ o.LABEL ].append( o )

