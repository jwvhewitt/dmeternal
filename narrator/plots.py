import context
import namegen
import random

class PlotError( Exception ):
    """Plot init will call this if initialization impossible."""
    pass

class Chapter( object ):
    """ Contains basic information about this chapter."""
    def __init__( self, num=1, start_rank=1, end_rank=5, follows=None ):
        if follows:
            num = follows.num + 1
            start_rank = follows.end_rank
            end_rank = start_rank + random.randint( 3,5 )
        self.num = num
        self.start_rank = start_rank
        self.end_rank = end_rank

class PlotState( object ):
    """For passing state information to subplots."""
    def __init__( self, propp=0, setting=None, chapter=None, rank=None, elements=None ):
        self.propp = propp
        self.setting = setting
        self.chapter = chapter
        self.rank = rank
        if elements:
            self.elements = elements.copy()
        else:
            self.elements = dict()
    def based_on( self, oplot ):
        self.propp = self.propp or oplot.propp
        self.setting = self.setting or oplot.setting
        self.chapter = self.chapter or oplot.chapter
        self.rank = self.rank or oplot.rank
        # Only copy over the elements not marked as private.
        for k,v in oplot.elements.iteritems():
            if isinstance( k, str ) and len(k)>0 and k[0]!="_":
                if k not in self.elements:
                    self.elements[k] = v
        # Why return self? Because this function will often be called straight
        # from the generator.
        return self

def all_contents( thing ):
    """Iterate over this thing and all of its descendants."""
    yield thing
    if hasattr( thing, "contents" ):
        for t in thing.contents:
            for tt in all_contents( t ):
                yield tt

class Plot( object ):
    """The building block of the adventure."""
    LABEL = ""
    UNIQUE = False
    propp = 0
    setting = False
    chapter = 1
    rank = 1
    active = False
    # Set scope to the scene identifier of the scene this plot's scripts are
    # attached to, or True for this plot to have global scope.
    scope = None
    def __init__( self, nart, pstate ):
        """Initialize + install this plot, or raise PlotError"""
        # nart = The Narrative object
        # pstate = The current plot state

        # Inherit the plot state.
        self.propp = self.propp or pstate.propp
        self.setting = self.setting or pstate.setting
        self.chapter = pstate.chapter or self.chapter
        self.rank = pstate.rank or self.rank
        self.elements = pstate.elements.copy()
        self.subplots = dict()

        # The move_records are stored in case this plot gets removed.
        self.move_records = list()

        # Do the custom initialization
        allok = self.custom_init( nart )

        # If failure, delete currently added subplots + raise error.
        if not allok:
            self.fail(nart)

    def fail( self, nart ):
        self.remove( nart )
        raise PlotError( str( self.__class__ ) )

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
            self.fail( nart )
        else:
            self.subplots[ident] = sp
        return sp

    def add_first_locale_sub_plot( self, nart ):
        # Utility function for a frequently used special case.
        sp = self.add_sub_plot( nart, "CITY_SCENE" )
        if sp:
            nart.camp.scene = sp.elements.get( "LOCALE" )
            self.register_element( "LOCALE", sp.elements.get( "LOCALE" ) )
            nart.camp.entrance = sp.elements.get( "ENTRANCE" )
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

    def seek_element( self, nart, ident, seek_func, dident=None, scope=None, must_find=True ):
        """Check scope and all children for a gear that seek_func returns True"""
        if not scope:
            scope = nart.camp
        candidates = list()
        for e in all_contents( scope ):
            if seek_func( e ):
                candidates.append( e )
        if candidates:
            e = random.choice( candidates )
            self.register_element( ident, e, dident )
            return e
        elif must_find:
            self.fail( nart )

    def register_scene( self, nart, myscene, mygen, ident=None, dident=None, rank=None ):
        if not myscene.name:
            myscene.name = namegen.DEFAULT.gen_word()
        self.register_element( ident, myscene, dident )
        nart.camp.contents.append( myscene )
        self.move_records.append( (myscene,nart.camp.contents) )
        nart.generators.append( mygen )
        self.move_records.append( (mygen,nart.generators) )
        myscene.rank = rank or self.rank
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
        # Remove self from the uniques set, if necessary.
        if self.UNIQUE and self.__class__ in nart.uniques:
            nart.uniques.remove( self.__class__ )

    def install( self, nart ):
        """Plot generation complete. Mesh plot with campaign."""
        for sp in self.subplots.itervalues():
            sp.install( nart )
        del self.move_records
        if self.scope:
            dest = self.elements.get( self.scope )
            if dest and hasattr( dest, "scripts" ):
                dest.scripts.append( self )
            else:
                nart.camp.scripts.append( self )

    def display( self, lead="" ):
        print lead + str( self.__class__ )
        for sp in self.subplots.itervalues():
            sp.display(lead+" ")

    def handle_trigger( self, explo, trigger, thing=None ):
        """A trigger has been tripped; make this plot react if appropriate."""
        # The trigger handler will be a method of this plot. If a thing is
        # involved, and that thing is an element, the handler's id will be
        # "[element ident]_[trigger type]". If no thing is involved, the
        # trigger handler will be "t_[trigger type]".
        # Trigger handler methods take the Exploration as a parameter.
        if thing:
            idlist = self.get_element_idents( thing )
            for label in idlist:
                handler = getattr( self, "{0}_{1}".format( label, trigger ), None )
                if handler:
                    handler( explo )
        else:
            handler = getattr( self, "t_{0}".format( trigger ), None )
            if handler:
                handler( explo )

    def get_dialogue_offers( self, npc ):
        """Get any dialogue offers this plot has for npc."""
        # Method [ELEMENTID]_offers will be called. This method should return a
        # list of offers to be built into the conversation.
        ofrz = self.get_generic_offers( npc )
        npc_ids = self.get_element_idents( npc )
        for i in npc_ids:
            ogen = getattr( self, "{0}_offers".format(i), None )
            if ogen:
                ofrz += ogen()
        return ofrz

    def modify_puzzle_menu( self, thing, thingmenu ):
        """Modify the thingmenu based on this plot."""
        # Method [ELEMENTID]_menu will be called with the menu as parameter.
        # This method should modify the menu as needed- typically by altering
        # the "desc" property (menu caption) and adding menu items.
        thing_ids = self.get_element_idents( thing )
        for i in thing_ids:
            ogen = getattr( self, "{0}_menu".format(i), None )
            if ogen:
                ogen( thingmenu )

    def get_generic_offers( self, npc ):
        """Get any offers that could apply to non-element NPCs."""
        return list()


    @classmethod
    def matches( self, pstate ):
        """Returns True if this plot matches the current plot state."""
        return True




