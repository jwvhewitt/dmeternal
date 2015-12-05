import context
import converter
import mutator
import maps
import prep
import random
import decor

# An Architecture gear is used to automatically modify a scene/scenegen combo
# to ensure a consistent environment across multiple subplots.
#
# Up to two architectures can be specified: one for the natural environment,
# and a separate one for the built environment.
#
# An interior architecture will typically define the following spritesheets:
#   SPRITE_WALL, SPRITE_FLOOR, SPRITE_INTERIOR, SPRITE_CHEST
# An exterior architecture will typically define the following spritesheets:
#   SPRITE_GROUND, SPRITE_CHEST

class Architecture( object ):
    def __init__( self, sprites=None, biome=None, desctags=None, gapfill=None,
      mutate=None, decorate=None, wall_filter=None, prepare=None ):
        if not sprites:
            sprites = dict()
        self.sprites = sprites
        self.biome = biome
        if not desctags:
            desctags = list()
        self.desctags = desctags
        self.gapfill = gapfill
        self.mutate = mutate
        self.decorate = decorate
        self.wall_filter = wall_filter
        self.prepare = prepare
    def __call__( self, scene, scenegen, primary=False ):
        # First, copy the sprite sheets.
        for k,v in self.sprites.iteritems():
            scene.sprites[k] = v
        # Second, if this is the primary, copy over environmental info.
        if primary:
            scene.biome = self.biome or scene.biome
            scene.desctags = list( self.desctags ) + list( scene.desctags )
            scenegen.GAPFILL = self.gapfill or scenegen.GAPFILL
            scenegen.MUTATE = self.mutate or scenegen.MUTATE
            scenegen.DECORATE = self.decorate or scenegen.DECORATE
            scenegen.WALL_FILTER = self.wall_filter or scenegen.WALL_FILTER
            scenegen.PREPARE = self.prepare or scenegen.PREPARE

class Forest( Architecture ):
    def __init__( self ):
        super(Forest, self).__init__(biome=context.HAB_FOREST,
          desctags=(context.MAP_WILDERNESS,),wall_filter=converter.ForestConverter(),
          mutate=mutator.CellMutator())
        #self.sprites[maps.SPRITE_WALL] = "terrain_wall_woodfort.png"
        self.sprites[maps.SPRITE_GROUND] = "terrain_ground_forest.png"
        #self.sprites[maps.SPRITE_FLOOR] = "terrain_floor_gravel.png"
        self.sprites[maps.SPRITE_CHEST] = "terrain_chest_wood.png"

class Desert( Architecture ):
    def __init__( self ):
        super(Desert, self).__init__(biome=context.HAB_DESERT,
          desctags=(context.MAP_WILDERNESS,),wall_filter=converter.DesertConverter(),
          mutate=mutator.CellMutator(),prepare=prep.HeightfieldPrep( loground=0.05, higround=0.15 ))
        #self.sprites[maps.SPRITE_WALL] = "terrain_wall_woodfort.png"
        self.sprites[maps.SPRITE_GROUND] = "terrain_ground_desert.png"
        #self.sprites[maps.SPRITE_FLOOR] = "terrain_floor_gravel.png"
        self.sprites[maps.SPRITE_CHEST] = "terrain_chest_wood.png"

class CavernDungeon( Architecture ):
    WALL_OPTIONS = ["terrain_wall_cave.png","terrain_wall_mine.png",
        "terrain_wall_rocks.png"]
    CUSTOM_DECOR_TYPES = {
        context.GEN_GOBLIN: (decor.GoblinHomeDec,{}),
        context.GEN_UNDEAD: (decor.CarnageDec,{}),
        context.GEN_KINGDOM: (decor.BarracksDec,{}),
        context.MTY_FIGHTER: (decor.BarracksDec,{}),
    }
    def __init__( self, fac=None ):
        super(CavernDungeon, self).__init__(biome=context.HAB_CAVE,
          desctags=[context.MAP_DUNGEON,context.MAP_GODOWN],
          wall_filter=converter.BasicConverter(),
          mutate=mutator.CellMutator())
        self.sprites[maps.SPRITE_WALL] = random.choice(self.WALL_OPTIONS)
        self.sprites[maps.SPRITE_GROUND] = "terrain_ground_under.png"
        self.sprites[maps.SPRITE_FLOOR] = "terrain_floor_gravel.png"
        self.sprites[maps.SPRITE_CHEST] = "terrain_chest_wood.png"
        # Do the custom decorating now.
        if fac:
            if fac.primary in self.CUSTOM_DECOR_TYPES.keys():
                a,b = self.CUSTOM_DECOR_TYPES[ fac.primary ]
                self.decorate = a(**b)
            elif fac.secondary in self.CUSTOM_DECOR_TYPES.keys():
                a,b = self.CUSTOM_DECOR_TYPES[ fac.secondary ]
                self.decorate = a(**b)

class BuildingDungeon( Architecture ):
    CUSTOM_DECOR_TYPES = {
        context.GEN_GOBLIN: (decor.GoblinHomeDec,{}),
        context.GEN_UNDEAD: (decor.CarnageDec,{}),
        context.GEN_KINGDOM: (decor.BarracksDec,{}),
        context.MTY_FIGHTER: (decor.BarracksDec,{}),
    }
    WALL_OPTIONS = [ "terrain_wall_darkbrick.png","terrain_wall_darkstone.png",
        "terrain_wall_dungeon.png","terrain_wall_woodfort.png"
    ]
    def __init__( self, fac=None ):
        super(BuildingDungeon, self).__init__(biome=context.HAB_BUILDING,
          desctags=[context.MAP_DUNGEON,context.MAP_GOUP,context.MTY_HUMANOID],
          wall_filter=converter.BasicConverter())
        self.sprites[maps.SPRITE_WALL] = random.choice(self.WALL_OPTIONS)
        self.sprites[maps.SPRITE_GROUND] = "terrain_ground_under.png"
        self.sprites[maps.SPRITE_FLOOR] = "terrain_floor_dungeon.png"
        self.sprites[maps.SPRITE_CHEST] = "terrain_chest_wood.png"
        if fac:
            if fac.primary in self.CUSTOM_DECOR_TYPES.keys():
                a,b = self.CUSTOM_DECOR_TYPES[ fac.primary ]
                self.decorate = a(**b)
            elif fac.secondary in self.CUSTOM_DECOR_TYPES.keys():
                a,b = self.CUSTOM_DECOR_TYPES[ fac.secondary ]
                self.decorate = a(**b)

class TunnelDungeon( Architecture ):
    CUSTOM_DECOR_TYPES = {
        context.GEN_GOBLIN: (decor.GoblinHomeDec,{}),
        context.GEN_UNDEAD: (decor.CarnageDec,{}),
        context.GEN_KINGDOM: (decor.BarracksDec,{}),
        context.MTY_FIGHTER: (decor.BarracksDec,{}),
    }
    WALL_OPTIONS = [ "terrain_wall_darkbrick.png","terrain_wall_darkstone.png",
        "terrain_wall_dungeon.png","terrain_wall_rocks.png"
    ]
    def __init__( self, fac=None ):
        super(TunnelDungeon, self).__init__(biome=context.HAB_TUNNELS,
          desctags=[context.MAP_DUNGEON,context.MAP_GODOWN,],
          wall_filter=converter.BasicConverter())
        self.sprites[maps.SPRITE_WALL] = random.choice(self.WALL_OPTIONS)
        self.sprites[maps.SPRITE_GROUND] = "terrain_ground_under.png"
        self.sprites[maps.SPRITE_FLOOR] = "terrain_floor_dungeon.png"
        self.sprites[maps.SPRITE_CHEST] = "terrain_chest_wood.png"
        if fac:
            if fac.primary in self.CUSTOM_DECOR_TYPES.keys():
                a,b = self.CUSTOM_DECOR_TYPES[ fac.primary ]
                self.decorate = a(**b)
            elif fac.secondary in self.CUSTOM_DECOR_TYPES.keys():
                a,b = self.CUSTOM_DECOR_TYPES[ fac.secondary ]
                self.decorate = a(**b)


class Village( Architecture ):
    DEFAULT_WALL_OPTIONS = ["terrain_wall_lightbrick.png",]
    CUSTOM_WALL_OPTIONS = {
        context.HAB_FOREST: ["terrain_wall_wood.png","terrain_wall_logcabin.png"],
        context.HAB_DESERT: ["terrain_wall_lightstone.png","terrain_wall_adobe.png"],
        context.HAB_CAVE: ["terrain_wall_lightstone.png","terrain_wall_rocks.png"],
    }
    FLOOR_OPTIONS = ["terrain_floor_wood.png","terrain_floor_tile.png","terrain_floor_stone.png"
    ]
    def __init__( self, biome=None, fac=None ):
        super(Village, self).__init__(biome=context.HAB_BUILDING,
          desctags=[context.CIVILIZED,context.MAP_GOUP],
          wall_filter=converter.BasicConverter())
        wall_options = self.DEFAULT_WALL_OPTIONS + self.CUSTOM_WALL_OPTIONS.get(biome,[])
        self.sprites[maps.SPRITE_WALL] = random.choice(wall_options)
        self.sprites[maps.SPRITE_FLOOR] = random.choice(self.FLOOR_OPTIONS)
        self.sprites[maps.SPRITE_CHEST] = "terrain_chest_wood.png"

class TempleArchitecture( Architecture ):
    WALL_OPTIONS = [ "terrain_wall_lightbrick.png","terrain_wall_lightstone.png",
        "terrain_wall_pillars.png","terrain_wall_purple.png"
    ]
    def __init__( self, fac=None ):
        super(TempleArchitecture, self).__init__(biome=context.HAB_BUILDING,
          desctags=[context.MAP_GOUP,context.MTY_PRIEST],
          wall_filter=converter.BasicConverter())
        self.sprites[maps.SPRITE_WALL] = random.choice(self.WALL_OPTIONS)
        self.sprites[maps.SPRITE_FLOOR] = "terrain_floor_diamond.png"
        self.sprites[maps.SPRITE_CHEST] = "terrain_chest_metal.png"
        self.sprites[maps.SPRITE_INTERIOR] = "terrain_int_temple.png"


WILDERNESS_TYPES = [Forest,Forest,Desert]
def make_wilderness():
    """A helper function to build a random wilderness architecture."""
    return random.choice(WILDERNESS_TYPES)()


def design_scene( width,height,mapgen,primary,setting=None,fac=None,secondary=None):
    """Return tuple of scene and scenegen for the requested stuff."""
    myscene = maps.Scene( width, height, setting=setting, fac=fac)
    mymapgen = mapgen( myscene )
    if secondary:
        secondary( myscene, mymapgen, False )
    primary( myscene, mymapgen, True )
    return (myscene,mymapgen)


