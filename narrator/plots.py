import context

class PlotState( object ):
    """For passing state information to subplots."""
    def __init__( self, propp=0, setting=None, chapter=1, level=1, elements={} ):
        self.propp = propp
        self.setting = setting
        self.chapter = chapter
        self.level = level
        self.elements = elements

class Plot( object ):
    """The building block of the adventure."""
    LABEL = ""
    propp = 0
    setting = False
    chapter = False
    level = False
    def __init__( self, nart, pstate ):
        """Initialize + install this plot, or set self.ok to False"""
        # nart = The Narrative object
        # pstate = The current plot state
        self.failed = False

        # Inherit the plot state.
        self.propp = max( self.propp, pstate.propp )
        self.setting = self.setting or pstate.setting
        self.chapter = pstate.chapter
        self.level = pstate.level

        # Confirm/locate all requested elements.
        # Start with a copy of the plot state elements.
        self.elements = pstate.elements.copy()


        # Create new elements, do custom manipulations.

        # Add needed subplots.
        self.subplots = list()

        # If failure, delete currently added subplots.


    def remove( self ):
        """Remove this plot, including subplots and new elements, from campaign."""

    @classmethod
    def matches( self, pstate ):
        """Returns True if this plot matches the current plot state."""
        return False




