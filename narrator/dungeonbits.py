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


#  **************************
#  ***   DUNGEON_ARMORY   ***
#  **************************


class GenericArmory( Plot ):
    LABEL = "DUNGEON_ARMORY"
    @classmethod
    def matches( self, pstate ):
        """Requires the SCENE to exist."""
        return pstate.elements.get("LOCALE")
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
          strength=150, habitat=scene.get_encounter_request() ) )
        room.contents.append( maps.WALL_WEAPON_RACK )
        room.contents.append( maps.WALL_WEAPON_RACK )
        for t in range( random.randint(2,4) ):
            mychest = waypoints.MediumChest()
            mychest.stock(self.rank)
            weapon = items.choose_item( random.choice( items.WEAPON_TYPES ), self.rank )
            items.make_item_magic( weapon, self.rank + 2 )
            weapon.identified = False
            mychest.contents.append( weapon )
            room.contents.append( mychest )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True

