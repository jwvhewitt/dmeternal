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

class BasicCave( Plot ):
    # This is the basic dungeon outline on which other classes will be based.
    LABEL = "DUNGEON_LEVEL"
    TAGS = set( (context.HAB_CAVE,) )
    MIN_RANK = 0
    @classmethod
    def matches( self, pstate ):
        """Requires the dungeon type to have all the needed tags."""
        return self.TAGS.issuperset( pstate.elements.get( "DUNGEON_TYPE" ) ) and pstate.rank >= self.MIN_RANK
    def custom_init( self, nart ):
        myscene = maps.Scene( min( 70 + self.rank * 5, 129 ), min( 70 + self.rank * 5, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_cave.png", maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png"},
            biome=context.HAB_CAVE, setting=self.setting,
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN) )
        mymapgen = randmaps.CaveScene( myscene )
#        mymapgen = randmaps.WalledForestScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )

        for t in range( random.randint(4+min(self.rank//3,6),8+min(self.rank//2,6)) ):
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
        mymapgen = randmaps.OpenTunnelScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )

        for t in range( random.randint(4+min(self.rank//3,6),8+min(self.rank//2,6)) ):
            self.add_sub_plot( nart, "ENCOUNTER" )

        return True

class GoblinMines( BasicCave ):
    LABEL = "DUNGEON_LEVEL"
    TAGS = set( (context.HAB_CAVE,context.GEN_GOBLIN) )
    def custom_init( self, nart ):
        myscene = maps.Scene( min( 70 + self.rank * 5, 129 ), min( 70 + self.rank * 5, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_rocks.png", maps.SPRITE_GROUND: "terrain_ground_canyon.png", maps.SPRITE_FLOOR: "terrain_floor_stone.png"},
            biome=context.HAB_CAVE, setting=self.setting,
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.GEN_GOBLIN) )
        mymapgen = randmaps.CaveScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )

        for t in range( random.randint(4+min(self.rank//3,6),8+min(self.rank//2,6)) ):
            self.add_sub_plot( nart, "ENCOUNTER" )

        return True


class BasicCryptLevel( BasicCave ):
    LABEL = "DUNGEON_LEVEL"
    TAGS = set( (context.HAB_TUNNELS,context.GEN_UNDEAD) )
    def custom_init( self, nart ):
        myscene = maps.Scene( min( 70 + self.rank * 5, 129 ), min( 70 + self.rank * 5, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_bone.png", maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_tile.png"},
            biome=context.HAB_TUNNELS, setting=self.setting,
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.GEN_UNDEAD) )
        mymapgen = randmaps.SubtleMonkeyTunnelScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )

        for t in range( random.randint(4+min(self.rank//3,6),8+min(self.rank//2,6)) ):
            self.add_sub_plot( nart, "ENCOUNTER" )

        return True

