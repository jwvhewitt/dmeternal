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


class CaveLevel( Plot ):
    LABEL = "DUNGEON_LEVEL"
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the dungeon level to be a cave."""
        return pstate.elements.get( "DUNGEON_TYPE" ) == context.HAB_CAVE
    def custom_init( self, nart ):
        myscene = maps.Scene( min( 70 + self.rank * 5, 129 ), min( 70 + self.rank * 5, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_cave.png", maps.SPRITE_GROUND: "terrain_ground_cthonic.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png"},
            biome=context.HAB_CAVE, setting=self.setting,
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.DES_EARTH) )
        mymapgen = mapgen.CaveScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="SCENE" )

        for t in range( random.randint(4,8) ):
            self.add_sub_plot( nart, "ENCOUNTER" )

        return True

