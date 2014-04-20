from plots import Plot,PlotError,PlotState
import context
import items
import maps
import mapgen
import waypoints
import monsters
import dialogue
import services
import teams
import characters
import random

### Sidestories get added to buildings in cities to flesh them out and to
### provide some things for the PC to do other than clearing the main dungeon.

class DateMyCousinPlease( Plot ):
    """The cousin of the shopkeeper must be removed from the house."""
    LABEL = "SIDE_STORY"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the SHOPKEEPER, SHOPKEEPER.species, and BUILDING_INT to exist."""
        return pstate.elements.get("SHOPKEEPER") and pstate.elements.get("SHOPKEEPER").species and pstate.elements.get("BUILDING_INT")
    def room_seeker( self, thing ):
        return isinstance( thing, mapgen.Room ) and context.ROOM_PUBLIC in thing.tags
    def custom_init( self, nart ):
        """Create the cousin, add puzzle subplot."""
        npc = self.elements["SHOPKEEPER"]
        the_room = self.seek_element( nart, "_THE_ROOM", self.room_seeker, scope=self.elements.get("BUILDING_INT") )
        the_cousin = monsters.generate_npc(species=npc.species.__class__)
        self.register_element( "TARGET", the_cousin )
        self.started = False
        self.dated = False
        self.add_sub_plot( nart, "SB_DATE", PlotState().based_on( self ) )
        self.add_sub_plot( nart, "REWARD", PlotState(elements={"ORIGIN":npc}).based_on( self ), ident="next" )
        return True
    def TARGET_DATE( self, explo ):
        self.dated = True
        self.subplots["next"].active = True
    def tell_problem( self, explo ):
        # Move the cousin into the room.
        scene = self.elements["BUILDING_INT"]
        area = self.elements["_THE_ROOM"].area
        pos = scene.find_entry_point_in_rect(area)
        if pos:
            the_cousin = self.elements["TARGET"]
            the_cousin.place( scene, pos )
            self.started = True

    def TARGET_offers( self, explo ):
        ol = list()
        if self.dated:
            myoffer = dialogue.Offer( "Thanks for helping me out.",
             context = context.ContextTag([context.HELLO]) )
            ol.append( myoffer )
        return ol

    def SHOPKEEPER_offers( self, explo ):
        ol = list()
        the_cousin = self.elements["TARGET"]
        if self.dated and self.subplots["next"].active:
            myoffer = dialogue.Offer( msg = "Thanks for getting {0} out of my hair; {1} still hangs around here too much but it's better than it used to be.".format(the_cousin, the_cousin.subject_pronoun()) ,
             context = context.ContextTag( [context.HELLO,context.REWARD] ) ,
             replies = [ dialogue.Reply( "You're welcome." ,
                    destination = dialogue.Cue( context.ContextTag( [context.REWARD] ) ) ) ]
             )
            ol.append( myoffer )
        elif not self.started:
            myoffer = dialogue.Offer( "It's my cousin {0}... {1} hangs out here all day bothering me.".format(the_cousin,the_cousin.subject_pronoun()),
             context = context.ContextTag([context.PROBLEM,context.PERSONAL]), effect=self.tell_problem )
            ol.append( myoffer )
        return ol


class TheBlackMarket( Plot ):
    """There's a black market in town, but it's hidden."""
    LABEL = "SIDE_STORY"
    UNIQUE = True
    active = True
    scope = True
    NAME_PATTERNS = ( "{0}'s Black Market", "{0}'s Contraband" )
    @classmethod
    def matches( self, pstate ):
        """Requires the SHOPKEEPER and LOCALE to exist."""
        return pstate.elements.get("SHOPKEEPER") and pstate.elements.get("LOCALE")
    def custom_init( self, nart ):
        """Create the black market, add secret connection."""
        locale = self.elements["LOCALE"]
        interior = maps.Scene( 50,50, sprites={maps.SPRITE_WALL: "terrain_wall_darkbrick.png", maps.SPRITE_FLOOR: "terrain_floor_wood.png" },
            biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.DES_CIVILIZED,) )
        igen = mapgen.BuildingScene( interior )
        self.register_scene( nart, interior, igen, ident="BUILDING_INT", dident="LOCALE" )
        int_mainroom = mapgen.SharpRoom( tags=(context.CIVILIZED,context.ENTRANCE), anchor=mapgen.northwest, parent=interior )
        int_mainroom.contents.append( maps.PILED_GOODS )
        int_mainroom.contents.append( maps.PILED_GOODS )
        int_mainroom.decorate = mapgen.GeneralStoreDec()
        npc = monsters.generate_npc( job=monsters.base.Merchant )
        interior.name = random.choice( self.NAME_PATTERNS ).format( npc )
        int_mainroom.contents.append( npc )
        self.register_element( "BMKEEPER", npc )
        self.shop = services.Shop( rank=self.rank+3, allow_magic=True )
        self.add_sub_plot( nart, "SECRET_CONNECT", PlotState( elements={"PREV":locale,"NEXT":interior} ).based_on( self ) )
        return True
    def BMKEEPER_offers( self, explo ):
        # Return list of shopkeeper offers.
        ol = list()
        ol.append( dialogue.Offer( "If anyone asks, you did not get this stuff from me, understand?",
         context = context.ContextTag([context.SHOP,context.BLACKMARKET]), effect=self.shop ) )
        return ol
    def SHOPKEEPER_offers( self, explo ):
        # Return list of shopkeeper offers.
        ol = list()
        if random.randint(1,4)==1:
            ol.append( dialogue.Offer( "If you are unhappy with the selection in my store, you can always try the black market. Good luck finding it, though." ,
             context = context.ContextTag([context.HELLO,context.SHOP,context.GENERALSTORE]),
             replies = [ dialogue.Reply( "I will just look at your wares, thanks." , destination = dialogue.Cue( context.ContextTag( [context.SHOP] ) ) ), ]
             ) )
        return ol


