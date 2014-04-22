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

### CityStories are added to cities to provide extra things to do other than the 
### main dungeon. They will generally result in a big reward/resource for the
### player.




class TheBlackMarket( Plot ):
    """There's a black market in town, but it's hidden."""
    LABEL = "CITY_STORY"
    UNIQUE = True
    active = True
    scope = True
    NAME_PATTERNS = ( "{0}'s Black Market", "{0}'s Contraband" )
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist."""
        return pstate.elements.get("LOCALE")
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
        npc.tags.append( context.CHAR_SHOPKEEPER )
        interior.name = random.choice( self.NAME_PATTERNS ).format( npc )
        int_mainroom.contents.append( npc )
        self.register_element( "BMKEEPER", npc )
        self.shop = services.Shop( rank=self.rank+3, allow_magic=True )
        self.add_sub_plot( nart, "SECRET_CONNECT", PlotState( elements={"PREV":locale,"NEXT":interior} ).based_on( self ) )
        self._still_looking = True
        return True
    def BMKEEPER_offers( self, explo ):
        # Return list of shopkeeper offers.
        ol = list()
        ol.append( dialogue.Offer( "If anyone asks, you did not get this stuff from me, understand?",
         context = context.ContextTag([context.SHOP,context.BLACKMARKET]), effect=self.shop ) )
        return ol
    def t_START( self, explo ):
        # Once the black market has been found, the local shopkeepers can cut
        # out the hint-giving.
        if explo.scene is self.elements["BUILDING_INT"]:
            self._still_looking = False
    def get_generic_offers( self, npc, explo ):
        # Return list of shopkeeper offers.
        ol = list()
        if self._still_looking and random.randint(1,4)==1 and npc is not self.elements["BMKEEPER"] and explo.camp.current_root_scene() is self.elements["LOCALE"]:
            ol.append( dialogue.Offer( "If you are unhappy with the selection in my store, you can always try the black market. Good luck finding it, though." ,
             context = context.ContextTag([context.HELLO,context.SHOP,context.GENERALSTORE]),
             replies = [ dialogue.Reply( "I will just look at your wares, thanks." , destination = dialogue.Cue( context.ContextTag( [context.SHOP] ) ) ), ]
             ) )
        return ol


