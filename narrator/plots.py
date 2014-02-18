
class PlotRequest( object ):
    def __init__( self, label, pdata ):
        self.label = label
        self.pdata = pdata
    def matches( self, plot ):
        all_ok = True
        if self.label == plot.LABEL:
            # This is a plot of the correct type. See what else checks out.
            for k,v in plot.REQUIRES:

            return all_ok

class Plot( object ):
    """The building block of the adventure."""
    LABEL = ""
    REQUIRES = dict()
    def __init__( self, nart, parel ):
        """Initialize + install this plot, or set self.ok to False"""
        # nart = The Narrative object
        # parel = The parent elements

        # Confirm/locate all requested elements.
        self.elements = parel.copy()


        # Create new elements, do custom manipulations.

        # Add needed subplots.

        # If failure, delete currently added subplots.


    def remove( self ):
        """Remove this plot, including subplots and new elements, from campaign."""






