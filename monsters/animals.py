import base
import stats
import items
import dialogue
import context
import invocations
import effects
import animobs
import targetarea

#  *******************************
#  ***   ENCOUNTER  LEVEL  1   ***
#  *******************************

class GiantBat( base.Monster ):
    name = "Giant Bat"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 6, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 1, stats.PIETY: 9, stats.CHARISMA: 8 }
    SPRITENAME = "monster_animals.png"
    FRAME = 0
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY, context.SET_RENFAN,
     context.DES_LUNAR, context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 1

    ATTACK = items.Attack( (1,4,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 1, self ) )

class GiantRat( base.Monster ):
    name = "Giant Rat"
    statline = { stats.STRENGTH: 8, stats.TOUGHNESS: 8, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 4, stats.PIETY: 9, stats.CHARISMA: 3 }
    SPRITENAME = "monster_animals.png"
    FRAME = 2
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_CAVE, context.HAB_BUILDING, context.SET_EVERY,
    context.DES_LUNAR, context.DES_CIVILIZED,
     context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 1

    ATTACK = items.Attack( (1,4,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 1, self ) )

class DireNewt( base.Monster ):
    name = "Dire Newt"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 9, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 2, stats.CHARISMA: 1 }
    SPRITENAME = "monster_animals.png"
    FRAME = 5
    TEMPLATES = (stats.REPTILE,)
    MOVE_POINTS = 8
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.HAB_CAVE,
     context.SET_RENFAN, context.DES_WATER, 
     context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 1

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 1, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  2   ***
#  *******************************

class MadDog( base.Monster ):
    name = "Mad Dog"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 8, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 1, stats.PIETY: 9, stats.CHARISMA: 1 }
    SPRITENAME = "monster_animals.png"
    FRAME = 7
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.DES_CIVILIZED,
     context.MTY_BEAST, context.GEN_CHAOS )
    ENC_LEVEL = 2

    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )

class CaveAnt( base.Monster ):
    name = "Cave Ant"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 1, stats.PIETY: 1, stats.CHARISMA: 1 }
    SPRITENAME = "monster_bugs.png"
    FRAME = 0
    TEMPLATES = (stats.BUG,)
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY, context.DES_EARTH, \
     context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 2

    ATTACK = items.Attack( (1,6,1), element = stats.RESIST_ACID )

    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )

class WoodBeetle( base.Monster ):
    name = "Wood Beetle"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 14, stats.REFLEXES: 8, \
        stats.INTELLIGENCE: 1, stats.PIETY: 1, stats.CHARISMA: 1 }
    SPRITENAME = "monster_bugs.png"
    FRAME = 11
    TEMPLATES = (stats.BUG,)
    MOVE_POINTS = 8
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY,
     context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 2

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )

class FireBeetle( base.Monster ):
    name = "Fire Beetle"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 9, stats.REFLEXES: 8, \
        stats.INTELLIGENCE: 1, stats.PIETY: 1, stats.CHARISMA: 1 }
    SPRITENAME = "monster_bugs.png"
    FRAME = 8
    TEMPLATES = (stats.BUG,stats.FIRE)
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.DES_FIRE,
     context.MTY_BEAST )
    ENC_LEVEL = 2

    ATTACK = items.Attack( (1,3,0), element = stats.RESIST_PIERCING,
     extra_effect=effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion ))

    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )

class Jackal( base.Monster ):
    name = "Jackal"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 3, stats.PIETY: 6, stats.CHARISMA: 5 }
    SPRITENAME = "monster_animals.png"
    FRAME = 25
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY,
     context.MTY_BEAST, context.DES_LUNAR, context.GEN_NATURE )
    ENC_LEVEL = 2

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  3   ***
#  *******************************

class Wolf( base.Monster ):
    name = "Wolf"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 13, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 4, stats.PIETY: 11, stats.CHARISMA: 12 }
    SPRITENAME = "monster_animals.png"
    FRAME = 11
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 3

    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 3, self ) )

class GiantFrog( base.Monster ):
    name = "Giant Frog"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 15, stats.REFLEXES: 11, \
        stats.INTELLIGENCE: 1, stats.PIETY: 5, stats.CHARISMA: 1 }
    SPRITENAME = "monster_animals.png"
    FRAME = 13
    TEMPLATES = (stats.REPTILE,)
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY, context.DES_WATER, context.MTY_BEAST, \
     context.GEN_NATURE )
    ENC_LEVEL = 3

    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 3, self ) )

class SwampDragonfly( base.Monster ):
    name = "Swamp Dragonfly"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 9, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 1, stats.PIETY: 7, stats.CHARISMA: 1, \
        stats.RESIST_ACID: 150 }
    SPRITENAME = "monster_bugs.png"
    FRAME = 2
    TEMPLATES = (stats.BUG,)
    MOVE_POINTS = 14
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY, context.DES_EARTH,
     context.MTY_BEAST, context.GEN_DRAGON )
    ENC_LEVEL = 3

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING )

    TECHNIQUES = ( invocations.MPInvocation( "Acid Breath",
      effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, att_modifier=10, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(), shot_anim=animobs.GreenSpray, ai_tar=invocations.vs_enemy, mp_cost=3
    ), )

    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  4   ***
#  *******************************

class BlackBear( base.Monster ):
    name = "Black Bear"
    statline = { stats.STRENGTH: 18, stats.TOUGHNESS: 16, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 3, stats.PIETY: 8, stats.CHARISMA: 6 }
    SPRITENAME = "monster_animals.png"
    FRAME = 14
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 4

    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING )

    def init_monster( self ):
        self.levels.append( base.Beast( 4, self ) )

class FireBat( base.Monster ):
    name = "Fire Bat"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 6, stats.PIETY: 9, stats.CHARISMA: 3, }
    SPRITENAME = "monster_animals.png"
    FRAME = 26
    TEMPLATES = (stats.FIRE,)
    MOVE_POINTS = 14
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY, context.DES_FIRE,
     context.DES_LUNAR, context.MTY_BEAST )
    ENC_LEVEL = 4

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING )

    TECHNIQUES = ( invocations.MPInvocation( "Fire Breath",
      effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, att_modifier=10, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,10,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(), shot_anim=animobs.Fireball, ai_tar=invocations.vs_enemy, mp_cost=3
    ), )

    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  5   ***
#  *******************************

class DireWolf( base.Monster ):
    name = "Dire Wolf"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 13, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 5, stats.PIETY: 9, stats.CHARISMA: 12 }
    SPRITENAME = "monster_animals.png"
    FRAME = 12
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_BEAST, context.GEN_NATURE, 
     context.GEN_GOBLIN )
    ENC_LEVEL = 5

    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 5, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  6   ***
#  *******************************

class Lion( base.Monster ):
    name = "Lion"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 10, stats.REFLEXES: 16, \
        stats.INTELLIGENCE: 3, stats.PIETY: 10, stats.CHARISMA: 9 }
    SPRITENAME = "monster_animals.png"
    FRAME = 17
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.SET_EVERY, context.DES_SOLAR, context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 6

    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )

    def init_monster( self ):
        self.levels.append( base.Beast( 6, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  7   ***
#  *******************************

class GrizzlyBear( base.Monster ):
    name = "Grizzly Bear"
    statline = { stats.STRENGTH: 18, stats.TOUGHNESS: 18, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 3, stats.PIETY: 8, stats.CHARISMA: 6 }
    SPRITENAME = "monster_animals.png"
    FRAME = 15
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 7

    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING )

    def init_monster( self ):
        self.levels.append( base.Beast( 7, self ) )

class GiantEagle( base.Monster ):
    name = "Giant Eagle"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 18, \
        stats.INTELLIGENCE: 12, stats.PIETY: 14, stats.CHARISMA: 13 }
    SPRITENAME = "monster_animals.png"
    FRAME = 21
    TEMPLATES = ()
    MOVE_POINTS = 16
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_BEAST, context.GEN_NATURE,
     context.DES_AIR, context.DES_SOLAR )
    ENC_LEVEL = 7

    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 7, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  8   ***
#  *******************************

class GreatStag( base.Monster ):
    name = "Great Stag"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 15, stats.REFLEXES: 17, \
        stats.INTELLIGENCE: 3, stats.PIETY: 19, stats.CHARISMA: 16 }
    SPRITENAME = "monster_animals.png"
    FRAME = 20
    TEMPLATES = ()
    MOVE_POINTS = 14
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 8

    ATTACK = items.Attack( (1,12,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 8, self ) )

class Crocodile( base.Monster ):
    name = "Crocodile"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 18, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 1, stats.PIETY: 10, stats.CHARISMA: 1 }
    SPRITENAME = "monster_animals.png"
    FRAME = 24
    TEMPLATES = (stats.REPTILE,)
    MOVE_POINTS = 8
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.SET_EVERY,
     context.DES_WATER, context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 8

    ATTACK = items.Attack( (1,12,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 9, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  9   ***
#  *******************************


#  ********************************
#  ***   ENCOUNTER  LEVEL  10   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  11   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  12   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  13   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  14   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  15   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  16   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  17   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  18   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  19   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  20   ***
#  ********************************


