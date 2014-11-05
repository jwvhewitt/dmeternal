from plots import Plot,PlotError
import context
import items
import maps
import waypoints
import monsters
import dialogue
import services
import teams
import characters
import random
import randmaps

#  ***************************************
#  ***   DIVIDED_ISLAND_COMPLICATION   ***
#  ***************************************
#
# Stick a complication in the bridge of a divided island scene- a boss monster,
# a locked door, or wotnot.
#

class DIC_LockedDoor( Plot ):
    LABEL = "DIVIDED_ISLAND_COMPLICATION"
    active = True
    scope = "LOCALE"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist."""
        return pstate.elements.get("LOCALE")
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )

        bridge_room = randmaps.rooms.BottleneckRoom()
        self._bridge_door = waypoints.PuzzleDoor()
        bridge_room.special_c[ "door" ] = self._bridge_door
        mygen.special_c[ "bridge" ] = bridge_room
        self.register_element( "_BRIDGE_ROOM", bridge_room, dident="LOCALE" )

        lever_room = randmaps.rooms.SharpRoom( tags = (context.ENTRANCE,) )
        lever_room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
          strength=150, habitat=scene.get_encounter_request() ) )
        self.register_element( "_LEVER_ROOM", lever_room, dident="LOCALE" )

        lever = waypoints.PuzzleSwitch()
        self.register_element( "_LEVER", lever, dident="_LEVER_ROOM" )

        return True

    def _LEVER_USE( self, explo ):
        self._bridge_door.activate( explo )
        self.active = False



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
        room.contents.append( teams.Team(default_reaction=-999, rank=self.rank+1, 
          strength=120, habitat=scene.get_encounter_request() ) )
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

