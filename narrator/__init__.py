
from plots import Plot
import collections
import random
import inspect
import campaign


class Narrative( object ):
    """The builder class which constructs a campaign."""
    def __init__( self, pstate ):
        self.camp = campaign.Campaign()
        self.generators = list()
        # Add the seed plot.
        self.story = self.generate_sub_plot( pstate, "INTRO_1" )

    def generate_sub_plot( self, pstate, label ):
        """Locate a plot which matches the request, init it, and return it."""
        # Create a list of potential plots.
        candidates = list()
        for sp in PLOT_LIST[label]:
            if sp.matches( pstate ):
                candidates.append( sp )
        if candidates:
            cp = None
            while candidates and not cp:
                cpc = random.choice( candidates )
                candidates.remove( cpc )
                try:
                    cp = cpc(self,pstate)
                except plots.PlotError:
                    cp = None
            return cp

    def build( self ):
        """Build finished campaign from this narrative."""
        for g in self.generators:
            g.make()
        self.story.install( self )

# The list of plots will be stored as a dictionary based on label.
PLOT_LIST = collections.defaultdict( list )
def harvest( mod ):
    for name in dir( mod ):
        o = getattr( mod, name )
        if inspect.isclass( o ) and issubclass( o , Plot ) and o is not Plot:
            PLOT_LIST[ o.LABEL ].append( o )

import citystuff
import intros
harvest( citystuff )
harvest( intros )

