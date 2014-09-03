from plots import Plot,PlotError,PlotState
import context
import items
import maps
import randmaps
import waypoints
import monsters
import dialogue
import services
import teams
import characters
import namegen
import random
import stats

###   *****************************
###   ***  RESOURCE_JOBTRAINER  ***
###   *****************************
###
### Needs an element JOB. Will stick a person with that job somewhere in the adventure.
###

class RJT_Default( Plot ):
    LABEL = "RESOURCE_JOBTRAINER"
    def seek_room( self, thing ):
        # We need a room that is marked as CIVILIZED and PUBLIC.
        return isinstance( thing, randmaps.Room ) and context.CIVILIZED in thing.tags and context.ROOM_PUBLIC in thing.tags
    def seek_npc( self, thing ):
        # We need a NPC.
        return isinstance( thing, characters.Character ) and context.CHAR_NPC in thing.tags and isinstance( thing.mr_level, self.elements[ "JOB" ] )
    def custom_init( self, nart ):
        # Find a public room. Stick the generated NPC there.
        if not self.seek_element( nart, "_PREMADE", self.seek_npc, must_find=False ):
            room = self.seek_element( nart, "_ROOM", self.seek_room )
            npc = monsters.generate_npc( job=self.elements[ "JOB" ] )
            self.register_element( "_NPC", npc, dident="_ROOM" )
        return True

class RJT_DungeonShop( Plot ):
    LABEL = "RESOURCE_JOBTRAINER"
    active = True
    scope = True
    UNIQUE = True
    NAME_PATTERNS = ( "{0}'s Dungeon Shop", "{0}'s Adventure Store" )
    def seek_scene( self, thing ):
        # We need a scene that is MAP_DUNGEON.
        return isinstance( thing, maps.Scene ) and context.MAP_DUNGEON in thing.desctags
    def custom_init( self, nart ):
        locale = self.seek_element( nart, "_LOCALE", self.seek_scene )
        exterior = randmaps.BuildingRoom( tags=(context.CIVILIZED,) )
        exterior.special_c[ "window" ] = maps.CASTLE_WINDOW
        exterior.special_c[ "sign1" ] = maps.SWORD_SIGN
        exterior.special_c[ "sign2" ] = maps.SHIELD_SIGN
        self.register_element( "_EXTERIOR", exterior, dident="_LOCALE" )
        interior = maps.Scene( 50,50, sprites={maps.SPRITE_WALL: "terrain_wall_darkbrick.png", maps.SPRITE_FLOOR: "terrain_floor_stone.png" },
            biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.DES_CIVILIZED,) )
        igen = randmaps.BuildingScene( interior )
        gate_1 = waypoints.GateDoor()
        gate_2 = waypoints.GateDoor()
        gate_1.destination = interior
        gate_1.otherside = gate_2
        gate_2.destination = self.elements.get( "_LOCALE" )
        gate_2.otherside = gate_1
        self.register_scene( nart, interior, igen, ident="BUILDING_INT", dident="_LOCALE" )
        exterior.special_c[ "door" ] = gate_1
        int_mainroom = randmaps.SharpRoom( tags=(context.CIVILIZED,context.ROOM_PUBLIC), anchor=randmaps.anchors.south, parent=interior )
        int_mainroom.contents.append( gate_2 )
        int_mainroom.contents.append( maps.PILED_GOODS )
        int_mainroom.contents.append( maps.PILED_GOODS )
        gate_2.anchor = randmaps.anchors.south
        int_mainroom.decorate = randmaps.decor.GeneralStoreDec(win=maps.CASTLE_WINDOW)
        npc = monsters.generate_npc( job=self.elements["JOB"] )
        npc.tags.append( context.CHAR_SHOPKEEPER )
        interior.name = random.choice( self.NAME_PATTERNS ).format( npc )
        gate_1.mini_map_label = "Dungeon Shop"
        int_mainroom.contents.append( npc )
        self.register_element( "SHOPKEEPER", npc )
        self.shop = self.register_element( "SHOPSERVICE", services.Shop( rank=locale.rank+3, allow_magic=True ) )
        self.first_time = True
        return True
    def SpeakFirstTime( self, explo ):
        self.first_time = False
    def SHOPKEEPER_offers( self, explo ):
        # Return list of shopkeeper offers.
        ol = list()
        ol.append( dialogue.Offer( "[SHOP_GENERAL]" ,
         context = context.ContextTag([context.SHOP,context.GENERALSTORE]), effect=self.shop ) )
        if self.first_time:
            ol.append( dialogue.Offer( "Welcome to [scene]. I know this seems like a weird place to build a shop, but you just can't beat the rent!",
             context = context.ContextTag([context.HELLO,context.SHOP,context.GENERALSTORE]), effect=self.SpeakFirstTime ) )
        return ol


###   *******************************
###   ***  RESOURCE_LOVEINTEREST  ***
###   *******************************
###
### Creates a NPC for romantic involvement with the TARGET element.
### Store NPC as element RESOURCE.

class RLI_VillagePerson( Plot ):
    """Creates a NPC to be a love interest of element TARGET."""
    LABEL = "RESOURCE_LOVEINTEREST"
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET and LOCALE to exist."""
        return pstate.elements.get("TARGET") and pstate.elements.get("LOCALE")

    def custom_init( self, nart ):
        w = random.randint(7,10)
        exterior = randmaps.BuildingRoom(w,17-w,tags=(context.CIVILIZED,) )
        exterior.special_c[ "window" ] = maps.SMALL_WINDOW
        self.register_element( "_EXTERIOR", exterior, dident="LOCALE" )

        interior = maps.Scene( 50,50, sprites={maps.SPRITE_FLOOR: "terrain_floor_wood.png" },
            biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.DES_CIVILIZED,) )
        igen = randmaps.BuildingScene( interior )

        gate_1 = waypoints.GateDoor()
        gate_2 = waypoints.GateDoor()
        gate_1.destination = interior
        gate_1.otherside = gate_2
        gate_2.destination = self.elements.get( "LOCALE" )
        gate_2.otherside = gate_1

        self.register_scene( nart, interior, igen, ident="_INTERIOR", dident="LOCALE" )
        exterior.special_c[ "door" ] = gate_1

        int_mainroom = randmaps.SharpRoom( tags=(context.CIVILIZED,), anchor=randmaps.anchors.south, parent=interior )
        int_mainroom.contents.append( gate_2 )
        gate_2.anchor = randmaps.anchors.south
        int_mainroom.decorate = randmaps.decor.BedroomDec()

        npc = monsters.generate_npc()
        interior.name = "{0}'s Home".format( npc )
        gate_1.mini_map_label = interior.name
        suitor = self.elements.get("TARGET")
        # Assume a heteronormativity rate of 50%.
        if random.randint(1,2) == 1:
            if suitor.gender == stats.MALE:
                npc.gender = stats.FEMALE
            elif suitor.gender == stats.FEMALE:
                npc.gender = stats.MALE
        int_mainroom.contents.append( npc )
        self.register_element( "RESOURCE", npc )

        return True




