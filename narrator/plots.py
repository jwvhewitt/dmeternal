import context

class PlotState( object ):
    """For passing state information to subplots."""
    def __init__( self, propp=0, setting=context.SET_EVERY, chapter=1, level=1, elements={} ):
        self.propp = propp
        self.setting = setting
        self.chapter = chapter
        self.level = level
        self.elements = elements

class Plot( object ):
    """The building block of the adventure."""
    LABEL = ""
    REQUIRES = dict()
    def __init__( self, nart, pstate ):
        """Initialize + install this plot, or set self.ok to False"""
        # nart = The Narrative object
        # parel = The parent elements

        # Confirm/locate all requested elements.
        self.elements = pstate.elements.copy()


        # Create new elements, do custom manipulations.

        # Add needed subplots.

        # If failure, delete currently added subplots.


    def remove( self ):
        """Remove this plot, including subplots and new elements, from campaign."""






