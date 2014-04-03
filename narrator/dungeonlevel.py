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

class BasicCave( Plot ):
    # This is the basic dungeon outline on which other classes will be based.
    LABEL = "DUNGEON_LEVEL"
    TAGS = set( (context.HAB_CAVE,) )
    @classmethod
    def matches( self, pstate ):
        """Requires the dungeon type to have all the needed tags."""
        return self.TAGS.issuperset( pstate.elements.get( "DUNGEON_TYPE" ) )
    def custom_init( self, nart ):
        myscene = maps.Scene( min( 70 + self.rank * 5, 129 ), min( 70 + self.rank * 5, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_cave.png", maps.SPRITE_GROUND: "terrain_ground_cthonic.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png"},
            biome=context.HAB_CAVE, setting=self.setting,
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN) )
        mymapgen = mapgen.CaveScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )

        for t in range( random.randint(4,8) ):
            self.add_sub_plot( nart, "ENCOUNTER" )

        return True

class SewerLevel( BasicCave ):
    LABEL = "DUNGEON_LEVEL"
    TAGS = set( (context.HAB_TUNNELS,context.DES_WATER) )
    def custom_init( self, nart ):
        myscene = maps.Scene( min( 70 + self.rank * 5, 129 ), min( 70 + self.rank * 5, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_darkstone.png", maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png"},
            biome=context.HAB_TUNNELS, setting=self.setting,
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.DES_WATER) )
        mymapgen = mapgen.OpenTunnelScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )

        for t in range( random.randint(4,8) ):
            self.add_sub_plot( nart, "ENCOUNTER" )

        return True

