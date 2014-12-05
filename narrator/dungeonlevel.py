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
    COMMON = True
    MIN_RANK = 0
    @classmethod
    def matches( self, pstate ):
        """Requires the dungeon type to have all the needed tags."""
        return self.TAGS.issuperset( pstate.elements.get( "DUNGEON_TYPE" ) ) and pstate.rank >= self.MIN_RANK and not self.antagonist_conflicts( pstate )
    @classmethod
    def antagonist_conflicts( self, pstate ):
        """Check to make sure that the antagonist doesn't conflict with this dungeon type."""
        # A conflict is caused by:
        # - an existing antagonist
        # - with an opposing element
        efac = pstate.elements.get( "ANTAGONIST" )
        if efac:
            ptag,stag = self.CONFLICTING_TAGS.get(efac.primary),self.CONFLICTING_TAGS.get(efac.secondary)
            if ptag and ptag in self.TAGS:
                return True
            elif stag and stag in self.TAGS:
                return True
    CONFLICTING_TAGS = {
        context.DES_FIRE: context.DES_WATER, context.DES_WATER: context.DES_FIRE,
        context.DES_AIR: context.DES_EARTH, context.DES_EARTH: context.DES_AIR,
        context.DES_LUNAR: context.DES_SOLAR, context.DES_SOLAR: context.DES_LUNAR
    }
    def custom_init( self, nart ):
        myscene = maps.Scene( min( 70 + self.rank * 5, 129 ), min( 70 + self.rank * 5, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_cave.png", maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png"},
            biome=context.HAB_CAVE, setting=self.setting, fac=self.elements.get("ANTAGONIST"),
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN) )
        mymapgen = randmaps.CaveScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )
        self.add_custom_decor( myscene, mymapgen )

        for t in range( random.randint(4+min(self.rank//3,6),8+min(self.rank//2,6)) ):
            self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "SPECIAL_FEATURE" )
        self.add_sub_plot( nart, "SPECIAL_ENCOUNTER" )

        return True

    CUSTOM_DECOR_TYPES = {
        context.GEN_GOBLIN: (randmaps.decor.GoblinHomeDec,{"fill_factor": 200}),
    }
    def add_custom_decor( self, myscene, mymapgen ):
        if myscene.fac and not mymapgen.DECORATE:
            if myscene.fac.primary in self.CUSTOM_DECOR_TYPES.keys():
                a,b = self.CUSTOM_DECOR_TYPES[ myscene.fac.primary ]
                mymapgen.DECORATE = a(**b)
            elif myscene.fac.secondary in self.CUSTOM_DECOR_TYPES.keys():
                a,b = self.CUSTOM_DECOR_TYPES[ myscene.fac.secondary ]
                mymapgen.DECORATE = a(**b)


class WaterCave( BasicCave ):
    # First of the elemental caves.
    LABEL = "DUNGEON_LEVEL"
    TAGS = set( (context.HAB_CAVE,context.DES_WATER) )
    def custom_init( self, nart ):
        myscene = maps.Scene( min( 70 + self.rank * 5, 129 ), min( 70 + self.rank * 5, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_cave.png", maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png"},
            biome=context.HAB_CAVE, setting=self.setting, fac=self.elements.get("ANTAGONIST"),
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.DES_WATER) )
        mymapgen = randmaps.OpenCaveScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )
        self.add_custom_decor( myscene, mymapgen )

        for t in range( random.randint(4+min(self.rank//3,6),8+min(self.rank//2,6)) ):
            self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "SPECIAL_FEATURE" )
        self.add_sub_plot( nart, "SPECIAL_ENCOUNTER" )

        return True

class WaterBridgeCave( BasicCave ):
    LABEL = "DUNGEON_LEVEL"
    TAGS = set( (context.HAB_CAVE,context.DES_WATER) )
    UNIQUE = True
    MIN_RANK = 2
    def custom_init( self, nart ):
        myscene = maps.Scene( 120, 120, 
            sprites={maps.SPRITE_WALL: "terrain_wall_cave.png", maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png"},
            biome=context.HAB_CAVE, setting=self.setting, fac=self.elements.get("ANTAGONIST"),
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.DES_WATER) )
        mymapgen = randmaps.DividedIslandScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )
        self.add_custom_decor( myscene, mymapgen )

        self.add_sub_plot( nart, "DIVIDED_ISLAND_COMPLICATION" )
        for t in range( random.randint(7,12) ):
            self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "SPECIAL_ENCOUNTER" )

        return True

class FireCave( BasicCave ):
    LABEL = "DUNGEON_LEVEL"
    TAGS = set( (context.HAB_CAVE,context.DES_FIRE) )
    def custom_init( self, nart ):
        myscene = maps.Scene( min( 70 + self.rank * 5, 129 ), min( 70 + self.rank * 5, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_cave.png", maps.SPRITE_GROUND: "terrain_ground_cthonic.png",
             maps.SPRITE_FLOOR: "terrain_floor_gravel.png",maps.SPRITE_CHEST: "terrain_chest_metal.png"},
            biome=context.HAB_CAVE, setting=self.setting, fac=self.elements.get("ANTAGONIST"),
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.DES_FIRE) )
        mymapgen = randmaps.OpenCaveScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )
        self.add_custom_decor( myscene, mymapgen )

        for t in range( random.randint(4+min(self.rank//3,6),8+min(self.rank//2,6)) ):
            self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "SPECIAL_FEATURE" )
        self.add_sub_plot( nart, "SPECIAL_ENCOUNTER" )

        return True

class FireBridgeCave( BasicCave ):
    LABEL = "DUNGEON_LEVEL"
    TAGS = set( (context.HAB_CAVE,context.DES_FIRE) )
    UNIQUE = True
    MIN_RANK = 2
    def custom_init( self, nart ):
        myscene = maps.Scene( 120, 120, 
            sprites={maps.SPRITE_WALL: "terrain_wall_cave.png", maps.SPRITE_GROUND: "terrain_ground_cthonic.png",
             maps.SPRITE_FLOOR: "terrain_floor_gravel.png",maps.SPRITE_CHEST: "terrain_chest_metal.png"},
            biome=context.HAB_CAVE, setting=self.setting, fac=self.elements.get("ANTAGONIST"),
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.DES_FIRE) )
        mymapgen = randmaps.DividedIslandScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )
        self.add_custom_decor( myscene, mymapgen )

        self.add_sub_plot( nart, "DIVIDED_ISLAND_COMPLICATION" )
        for t in range( random.randint(7,12) ):
            self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "SPECIAL_ENCOUNTER" )

        return True


class AirCave( BasicCave ):
    LABEL = "DUNGEON_LEVEL"
    TAGS = set( (context.HAB_CAVE,context.DES_AIR) )
    def custom_init( self, nart ):
        myscene = maps.Scene( min( 70 + self.rank * 5, 129 ), min( 70 + self.rank * 5, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_cave.png", maps.SPRITE_GROUND: "terrain_ground_canyon.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png"},
            biome=context.HAB_CAVE, setting=self.setting, fac=self.elements.get("ANTAGONIST"),
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.DES_AIR) )
        mymapgen = randmaps.OpenCaveScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )
        self.add_custom_decor( myscene, mymapgen )

        for t in range( random.randint(4+min(self.rank//3,6),8+min(self.rank//2,6)) ):
            self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "SPECIAL_FEATURE" )
        self.add_sub_plot( nart, "SPECIAL_ENCOUNTER" )

        return True

class EarthCave( BasicCave ):
    LABEL = "DUNGEON_LEVEL"
    TAGS = set( (context.HAB_CAVE,context.DES_EARTH) )
    def custom_init( self, nart ):
        myscene = maps.Scene( min( 70 + self.rank * 5, 129 ), min( 70 + self.rank * 5, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_cave.png", maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png"},
            biome=context.HAB_CAVE, setting=self.setting, fac=self.elements.get("ANTAGONIST"),
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.DES_EARTH) )
        mymapgen = randmaps.CaveScene( myscene, decorate = randmaps.decor.RockyDec() )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )
        self.add_custom_decor( myscene, mymapgen )

        for t in range( random.randint(4+min(self.rank//3,6),8+min(self.rank//2,6)) ):
            self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "SPECIAL_FEATURE" )
        self.add_sub_plot( nart, "SPECIAL_ENCOUNTER" )

        return True

class EarthMushroomCave( BasicCave ):
    LABEL = "DUNGEON_LEVEL"
    TAGS = set( (context.HAB_CAVE,context.DES_EARTH) )
    UNIQUE = True
    MIN_RANK = 2
    def custom_init( self, nart ):
        myscene = maps.Scene( min( 90 + self.rank * 3, 129 ), min( 90 + self.rank * 3, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_cave.png", maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png"},
            biome=context.HAB_CAVE, setting=self.setting, fac=self.elements.get("ANTAGONIST"),
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.DES_EARTH,context.MTY_PLANT) )
        mymapgen = randmaps.WalledForestScene( myscene, decorate = randmaps.decor.RockyDec() )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )
        self.add_custom_decor( myscene, mymapgen )

        for t in range( random.randint(4+min(self.rank//3,6),8+min(self.rank//2,6)) ):
            self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "SPECIAL_ENCOUNTER" )

        return True


class SewerLevel( BasicCave ):
    LABEL = "DUNGEON_LEVEL"
    TAGS = set( (context.HAB_TUNNELS,context.DES_WATER) )
    def custom_init( self, nart ):
        myscene = maps.Scene( min( 70 + self.rank * 5, 129 ), min( 70 + self.rank * 5, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_darkstone.png", maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png"},
            biome=context.HAB_TUNNELS, setting=self.setting, fac=self.elements.get("ANTAGONIST"),
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.DES_WATER) )
        mymapgen = randmaps.OpenTunnelScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )
        self.add_custom_decor( myscene, mymapgen )

        for t in range( random.randint(4+min(self.rank//3,6),8+min(self.rank//2,6)) ):
            self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "SPECIAL_FEATURE" )
        self.add_sub_plot( nart, "SPECIAL_ENCOUNTER" )

        return True


class BasicCryptLevel( BasicCave ):
    LABEL = "DUNGEON_LEVEL"
    TAGS = set( (context.HAB_TUNNELS,context.GEN_UNDEAD) )
    def custom_init( self, nart ):
        myscene = maps.Scene( min( 70 + self.rank * 5, 129 ), min( 70 + self.rank * 5, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_bone.png", maps.SPRITE_GROUND: "terrain_ground_under.png",
             maps.SPRITE_FLOOR: "terrain_floor_tile.png", maps.SPRITE_CHEST: "terrain_chest_metal.png" },
            biome=context.HAB_TUNNELS, setting=self.setting, fac=self.elements.get("ANTAGONIST"),
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.GEN_UNDEAD) )
        mymapgen = randmaps.SubtleMonkeyTunnelScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )
        self.add_custom_decor( myscene, mymapgen )

        for t in range( random.randint(4+min(self.rank//3,6),8+min(self.rank//2,6)) ):
            self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "SPECIAL_FEATURE" )
        self.add_sub_plot( nart, "SPECIAL_ENCOUNTER" )

        return True

