
from plots import Plot,PlotError
import context
import items
import maps
import mapgen
import waypoints
import monsters

class LightOfTheMacguffin( Plot ):
    LABEL = "INTRO_1"
    propp = context.PROPP_INTERDICTION
    setting = context.SET_RENFAN
    @classmethod
    def matches( self, pstate ):
        """Requires the setting to be None or RenFan."""
        if pstate.setting in (None,context.SET_RENFAN):
            return True
    def custom_init( self, nart ):
        """Load *INTRO_2, create MACGUFFIN"""
        self.register_element( "MACGUFFIN", items.choose_item() )
        self.add_sub_plot( nart, "INTRO_2", ident="next" )
        return True

class OurMacguffinIsGone( Plot ):
    LABEL = "INTRO_2"
    @classmethod
    def matches( self, pstate ):
        """Requires the propp to be INTERDICTION, MACGUFFIN to exist."""
        return pstate.propp == context.PROPP_INTERDICTION and pstate.elements.get( "MACGUFFIN" )
    def custom_init( self, nart ):
        sp = self.add_sub_plot( nart, "CITY_SCENE" )
        if sp:
            nart.camp.scene = sp.elements.get( "SCENE" )
            nart.camp.entrance = sp.elements.get( "ENTRANCE" )
            return True

class CityOnEdgeOfCiv( Plot ):
    LABEL = "CITY_SCENE"
    def custom_init( self, nart ):
        """Create map, fill with city + services."""
        myscene = maps.Scene( 102, 102, sprites={maps.SPRITE_WALL: "terrain_wall_lightbrick.png"},
            biome=context.HAB_FOREST, setting=self.setting, desctags=(context.DES_CIVILIZED,) )
        mymapgen = mapgen.EdgeOfCivilization( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="SCENE" )

        castle = self.register_element( "CITY", mapgen.CastleRoom( width=35,height=35,tags=(context.CIVILIZED,), parent=myscene ) )
        myroom = mapgen.FuzzyRoom( tags=(context.ENTRANCE,), parent=castle )
        myent = waypoints.Waypoint()
        myroom.contents.append( myent )
        self.register_element( "ENTRANCE", myent )

        self.add_sub_plot( nart, "CITY_WEAPONSHOP" )

        return True

class GenericWeaponShop( Plot ):
    LABEL = "CITY_WEAPONSHOP"
    def custom_init( self, nart ):
        city = self.elements.get( "CITY" )

        exterior = mapgen.BuildingRoom( tags=(context.CIVILIZED,) )
        exterior.special_c[ "window" ] = maps.SMALL_WINDOW
        exterior.special_c[ "sign1" ] = maps.SWORD_SIGN
        self.register_element( "_EXTERIOR", exterior, dident="CITY" )

        interior = maps.Scene( 50,50, sprites={maps.SPRITE_FLOOR: "terrain_floor_wood.png" },
            biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.DES_CIVILIZED,) )
        igen = mapgen.BuildingScene( interior )

        gate_1 = waypoints.GateDoor()
        gate_2 = waypoints.GateDoor()
        gate_1.destination = interior
        gate_1.otherside = gate_2
        gate_2.destination = self.elements.get( "SCENE" )
        gate_2.otherside = gate_1

        self.register_scene( nart, interior, igen, ident="_INTERIOR", dident="SCENE" )

        exterior.special_c[ "door" ] = gate_1
        int_mainroom = mapgen.SharpRoom( tags=(context.CIVILIZED,), anchor=mapgen.south, parent=interior )
        int_mainroom.contents.append( gate_2 )
        gate_2.anchor = mapgen.south
        int_mainroom.decorate = mapgen.BuildingDec()
        int_mainroom.debug = True

        npc = monsters.generate_npc( job=monsters.base.Merchant )
        int_mainroom.contents.append( npc )
        self.register_element( "SHOPKEEPER", npc )

        return True


