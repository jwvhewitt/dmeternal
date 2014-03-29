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
import namegen
import random
import stats

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
        exterior = mapgen.BuildingRoom(w,17-w,tags=(context.CIVILIZED,) )
        exterior.special_c[ "window" ] = maps.SMALL_WINDOW
        self.register_element( "_EXTERIOR", exterior, dident="LOCALE" )

        interior = maps.Scene( 50,50, sprites={maps.SPRITE_FLOOR: "terrain_floor_wood.png" },
            biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.DES_CIVILIZED,) )
        igen = mapgen.BuildingScene( interior )

        gate_1 = waypoints.GateDoor()
        gate_2 = waypoints.GateDoor()
        gate_1.destination = interior
        gate_1.otherside = gate_2
        gate_2.destination = self.elements.get( "LOCALE" )
        gate_2.otherside = gate_1

        self.register_scene( nart, interior, igen, ident="_INTERIOR", dident="LOCALE" )
        exterior.special_c[ "door" ] = gate_1

        int_mainroom = mapgen.SharpRoom( tags=(context.CIVILIZED,), anchor=mapgen.south, parent=interior )
        int_mainroom.contents.append( gate_2 )
        gate_2.anchor = mapgen.south
        int_mainroom.decorate = mapgen.BedroomDec()

        npc = monsters.generate_npc()
        interior.name = "{0}'s Home".format( npc )
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


