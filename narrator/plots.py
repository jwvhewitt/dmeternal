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
        # Why return self? Because this function will often be called straight
        # from the generator.
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

        # The move_records are stored in case this plot gets removed.
        self.move_records = list()

        # Do the custom initialization
        allok = self.custom_init( nart )

        # If failure, delete currently added subplots + raise error.
        if hasattr( self, "fail" ) or not allok:
            self.remove( nart )
            raise PlotError

    def get_element_idents( self, ele ):
        """Return list of element idents assigned to this object."""
        return [key for key,value in self.elements.items() if value is ele]

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

    def move_element( self, ele, dest ):
        # Record when a plot places an element; if this plot is removed, the
        # element will be removed from its location as well.
        if hasattr( ele, "container" ) and ele.container:
            ele.container.remove( ele )
        dest.contents.append( ele )
        self.move_records.append( (ele,dest.contents) )

    def register_element( self, ident, ele, dident=None ):
        # dident is an element itent for this element's destination.
        self.elements[ident] = ele
        if dident:
            mydest = self.elements.get(dident)
            if mydest:
                self.move_element( ele, mydest )
        return ele

    def register_scene( self, nart, myscene, mygen, ident=None, dident=None ):
        self.register_element( ident, myscene, dident )
        nart.camp.scenes.append( myscene )
        self.move_records.append( (myscene,nart.camp.scenes) )
        nart.generators.append( mygen )
        self.move_records.append( (mygen,nart.generators) )
        return myscene

    def custom_init( self, nart ):
        """Return True if everything ok, or False otherwise."""
        return True

    def remove( self, nart ):
        """Remove this plot, including subplots and new elements, from campaign."""
        # First, remove all subplots.
        for sp in self.subplots.itervalues():
            sp.remove( nart )
        # Next, remove any elements created by this plot.
        for e,d in self.move_records:
            if e in d:
                d.remove( e )

    def cleanup( self ):
        """Plot generation complete. Remove temporary data."""
        for sp in self.subplots.itervalues():
            sp.cleanup()
        del self.move_records

    def display( self, lead="" ):
        print lead + str( self.__class__ )
        for sp in self.subplots.itervalues():
            sp.display(lead+" ")

    def get_dialogue_offers( self, npc ):
        """Get any dialogue offers this plot has for npc."""
        ofrz = list()
        npc_ids = self.get_element_idents( npc )
        for i in npc_ids:
            ogen = getattr( self, "{0}_offers".format(i), None )
            if ogen:
                ofrz += ogen()
        return ofrz


    @classmethod
    def matches( self, pstate ):
        """Returns True if this plot matches the current plot state."""
        return True




