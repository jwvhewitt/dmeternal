import context

class PlotError( Exception ):
    """Plot init will call this if initialization impossible."""
    pass

class PlotState( object ):
    """For passing state information to subplots."""
    def __init__( self, propp=0, setting=None, chapter=None, level=None, elements={} ):
        self.propp = propp
        self.setting = setting
        self.chapter = chapter
        self.level = level
        self.elements = elements
    def based_on( self, oplot ):
        self.propp = self.propp or oplot.propp
        self.setting = self.setting or oplot.setting
        self.chapter = self.chapter or oplot.chapter
        self.level = self.level or oplot.level
        # Only copy over the elements not marked as private.
        for k,v in oplot.elements.iteritems():
            if isinstance( k, str ) and len(k)>0 and k[0]!="_":
                self.elements[k] = v

        

class Plot( object ):
    """The building block of the adventure."""
    LABEL = ""
    propp = 0
    setting = False
    chapter = 1
    level = 1
    def __init__( self, nart, pstate ):
        """Initialize + install this plot, or raise PlotError"""
        # nart = The Narrative object
        # pstate = The current plot state

        # Inherit the plot state.
        self.propp = self.propp or pstate.propp
        self.setting = self.setting or pstate.setting
        self.chapter = pstate.chapter or self.chapter
        self.level = pstate.level or self.level
        self.elements = pstate.elements.copy()
        self.subplots = dict()

        # Do the custom initialization
        allok = self.custom_init( nart )

        # If failure, delete currently added subplots + raise error.
        if not allok:
            raise PlotError

    def custom_init( self, nart ):
        """Return True if everything ok, or False otherwise."""
        return True

    def remove( self ):
        """Remove this plot, including subplots and new elements, from campaign."""

    @classmethod
    def matches( self, pstate ):
        """Returns True if this plot matches the current plot state."""
        return False




