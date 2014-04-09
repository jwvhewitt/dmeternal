
from plots import Plot
import collections
import random
import inspect
import campaign
import worlds


class Narrative( object ):
    """The builder class which constructs a campaign."""
    def __init__( self, pstate ):
        self.camp = campaign.Campaign()
        self.generators = list()
        self.errors = list()
        self.uniques = set()
        # Add the seed plot.
        self.story = self.generate_sub_plot( pstate, "INTRO_1" )

    def generate_sub_plot( self, pstate, label ):
        """Locate a plot which matches the request, init it, and return it."""
        # Create a list of potential plots.
        candidates = list()
        for sp in PLOT_LIST[label]:
            if sp.matches( pstate ):
                if not sp.UNIQUE or sp not in self.uniques:
                    candidates.append( sp )
        if candidates:
            cp = None
            while candidates and not cp:
                cpc = random.choice( candidates )
                candidates.remove( cpc )
                try:
                    cp = cpc(self,pstate)
                    if cpc.UNIQUE:
                        self.uniques.add( cpc )
                except plots.PlotError:
                    cp = None
            if not cp:
                self.errors.append( "No plot accepted for {0}".format( label ) )
            return cp
        else:
            self.errors.append( "No plot found for {0}".format( label ) )

    def get_map_generator( self, gb ):
        mygen = None
        for mg in self.generators:
            if mg.gb == gb:
                mygen = mg
                break
        return mygen

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
import complication
import connections
import dungeonlevel
import encounters
import intros
import puzzlebits
import resources
import rewards
import sidestories
import socialbits
harvest( citystuff )
harvest( complication )
harvest( connections )
harvest( dungeonlevel )
harvest( encounters )
harvest( intros )
harvest( puzzlebits )
harvest( resources )
harvest( rewards )
harvest( sidestories )
harvest( socialbits )


