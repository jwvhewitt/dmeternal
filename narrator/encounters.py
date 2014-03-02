

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

class BasicEncounter( Plot ):
    LABEL = "ENCOUNTER"
    active = True
    @classmethod
    def matches( self, pstate ):
        """Requires the SCENE to exist."""
        return pstate.elements.get("SCENE")
    def custom_init( self, nart ):
        scene = self.elements.get("SCENE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        room.contents.append( teams.Team(default_reaction=-999, rank=self.level, 
          habitat=scene.get_encounter_request() ) )
        self.register_element( "_ROOM", room, dident="SCENE" )
        return True

