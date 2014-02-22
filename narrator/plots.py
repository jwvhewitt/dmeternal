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
        return self



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
        if hasattr( self, "fail" ) or not allok:
            self.remove( nart )
            raise PlotError

    def add_sub_plot( self, nart, splabel, spstate=None, ident=None ):
        if not spstate:
            spstate = PlotState().based_on(self)
        if not ident:
            ident = "_autoident_{0}".format( len( self.subplots ) )
        sp = nart.generate_sub_plot( spstate, splabel )
        if not sp:
            self.fail = True
        else:
            self.subplots[ident] = sp
        return sp

    def register_element( self, ident, ele ):
        self.elements[ident] = ele
        if not hasattr( ele, "plot" ):
            ele.plot = self

    def custom_init( self, nart ):
        """Return True if everything ok, or False otherwise."""
        return True

    def remove( self, nart ):
        """Remove this plot, including subplots and new elements, from campaign."""
        # First, remove all subplots.
        for sp in self.subplots.itervalues():
            sp.remove( nart )
        # Next, remove any elements created by this plot.

    def display( self, lead="" ):
        print lead + str( self.__class__ )
        for sp in self.subplots.itervalues():
            sp.display(lead+" ")

    @classmethod
    def matches( self, pstate ):
        """Returns True if this plot matches the current plot state."""
        return False




