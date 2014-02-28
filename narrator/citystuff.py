
from plots import Plot,PlotError
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

#  ************************
#  ***   CITY_LIBRARY   ***
#  ************************

class GenericLibrary( Plot ):
    LABEL = "CITY_LIBRARY"
    active = True
    scope = "_INTERIOR"
    def custom_init( self, nart ):
        exterior = mapgen.BuildingRoom( tags=(context.CIVILIZED,) )
        exterior.special_c[ "window" ] = maps.SMALL_WINDOW
        exterior.special_c[ "sign1" ] = maps.BOOK_SIGN
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
        int_mainroom.contents.append( waypoints.Bookshelf() )
        gate_2.anchor = mapgen.south
#        int_mainroom.decorate = mapgen.WeaponShopDec()

        if random.randint(1,100) == 23:
            npc = monsters.generate_npc( job=characters.Ninja )
        else:
            npc = monsters.generate_npc( job=random.choice((characters.Mage,characters.Mage,characters.Necromancer,
                characters.Mage,characters.Mage,characters.Necromancer,characters.Bard) ))
        int_mainroom.contents.append( npc )
        self.register_element( "SHOPKEEPER", npc )

        self.shop = services.Library()

        return True

    def SHOPKEEPER_offers( self ):
        # Return list of shopkeeper offers.
        ol = list()
        ol.append( dialogue.Offer( "Knowledge is power. Some knowledge is more powerful than others." ,
         context = context.ContextTag([context.SERVICE,context.LIBRARY]), effect=self.shop ) )
        return ol


#  ***************************
#  ***   CITY_WEAPONSHOP   ***
#  ***************************

class GenericWeaponShop( Plot ):
    LABEL = "CITY_WEAPONSHOP"
    active = True
    scope = "_INTERIOR"
    def custom_init( self, nart ):
        exterior = mapgen.BuildingRoom( tags=(context.CIVILIZED,) )
        exterior.special_c[ "window" ] = maps.SMALL_WINDOW
        exterior.special_c[ "sign1" ] = maps.WEAPONS_SIGN
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
#        int_mainroom.contents.append( waypoints.Anvil() )
        gate_2.anchor = mapgen.south
        int_mainroom.decorate = mapgen.WeaponShopDec()

        npc = monsters.generate_npc( job=monsters.base.Merchant )
        int_mainroom.contents.append( npc )
        self.register_element( "SHOPKEEPER", npc )

        self.shop = services.Shop( rank=self.level+2 )

        return True

    def SHOPKEEPER_offers( self ):
        # Return list of shopkeeper offers.
        ol = list()
        ol.append( dialogue.Offer( "This is my shop. There is not much here yet." ,
         context = context.ContextTag([context.SHOP,context.WEAPON]), effect=self.shop ) )
        return ol

