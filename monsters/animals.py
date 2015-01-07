import base
import stats
import items
import dialogue
import context
import invocations
import effects
import animobs
import targetarea
import enchantments
import treasuretype
import abilities

#  *******************************
#  ***   ENCOUNTER  LEVEL  1   ***
#  *******************************

class GiantBat( base.Monster ):
    name = "Giant Bat"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 1, stats.PIETY: 9, stats.CHARISMA: 8,
        stats.NATURAL_DEFENSE: 5 }
    SPRITENAME = "monster_animals.png"
    FRAME = 0
    TEMPLATES = ()
    MOVE_POINTS = 16
    VOICE = None
    HABITAT = ( context.HAB_CAVE, context.HAB_TUNNELS,
     context.SET_EVERY, context.SET_RENFAN,
     context.DES_LUNAR, context.DES_AIR,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
    ENC_LEVEL = 1

    ATTACK = items.Attack( (1,4,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 1, self ) )

class GiantRat( base.Monster ):
    name = "Giant Rat"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 12, stats.REFLEXES: 17, \
        stats.INTELLIGENCE: 2, stats.PIETY: 12, stats.CHARISMA: 4,
        stats.PHYSICAL_ATTACK: 5, stats.NATURAL_DEFENSE: 5 }
    SPRITENAME = "monster_animals.png"
    FRAME = 2
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = None
    HABITAT = ( context.HAB_BUILDING, context.HAB_TUNNELS,
     context.SET_EVERY,
     context.DES_EARTH, context.DES_CIVILIZED,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
    ENC_LEVEL = 1

    ATTACK = items.Attack( (1,4,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 1, self ) )

class DireNewt( base.Monster ):
    name = "Dire Newt"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 8, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 2, stats.CHARISMA: 1,
        stats.PHYSICAL_ATTACK: 10 }
    SPRITENAME = "monster_animals.png"
    FRAME = 5
    TEMPLATES = (stats.REPTILE,)
    MOVE_POINTS = 6
    VOICE = None
    HABITAT = ( context.HAB_FOREST, context.HAB_CAVE,
     context.SET_RENFAN, context.DES_WATER, 
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE, context.GEN_DRAGON )
    ENC_LEVEL = 1

    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 1, self ) )

class Chicken( base.Monster ):
    name = "Chicken"
    statline = { stats.STRENGTH: 9, stats.TOUGHNESS: 8, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 6, stats.CHARISMA: 4,
        stats.PHYSICAL_ATTACK: 15 }
    SPRITENAME = "monster_animals.png"
    FRAME = 23
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = None
    HABITAT = ( context.HAB_EVERY,
     context.DES_AIR,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
    ENC_LEVEL = 1

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING, skill_mod=stats.REFLEXES )

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
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.DES_CIVILIZED,
     context.MAP_WILDERNESS,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_CHAOS )
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
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY, context.DES_EARTH, \
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
    ENC_LEVEL = 2

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_ACID,
        hit_anim=animobs.GreenExplosion )

    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )

class WoodBeetle( base.Monster ):
    name = "Wood Beetle"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 12, stats.REFLEXES: 8, \
        stats.INTELLIGENCE: 1, stats.PIETY: 1, stats.CHARISMA: 1 }
    SPRITENAME = "monster_bugs.png"
    FRAME = 10
    TEMPLATES = (stats.BUG,)
    MOVE_POINTS = 8
    VOICE = None
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
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
    MOVE_POINTS = 8
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.DES_FIRE,
     context.MAP_DUNGEON,
     context.MTY_BEAST, context.MTY_CREATURE )
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
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY,
     context.MTY_BEAST, context.MTY_CREATURE, context.DES_LUNAR, context.GEN_NATURE )
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
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY, context.SET_RENFAN,
     context.MAP_WILDERNESS,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
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
    TREASURE = treasuretype.Swallowed()
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY, context.DES_WATER,
     context.MTY_BEAST, context.MTY_CREATURE,
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
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY, context.DES_EARTH,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_DRAGON )
    ENC_LEVEL = 3

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING )

    TECHNIQUES = ( invocations.MPInvocation( "Acid Breath",
      effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, att_modifier=10, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(), shot_anim=animobs.GreenSpray, ai_tar=invocations.TargetEnemy(), mp_cost=3
    ), )

    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )

class BoringBeetle( base.Monster ):
    name = "Boring Beetle"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 12, stats.REFLEXES: 8, \
        stats.INTELLIGENCE: 1, stats.PIETY: 1, stats.CHARISMA: 1 }
    SPRITENAME = "monster_bugs.png"
    FRAME = 11
    TEMPLATES = (stats.BUG,)
    MOVE_POINTS = 8
    VOICE = None
    HABITAT = ( context.HAB_CAVE, context.HAB_TUNNELS, context.SET_EVERY,
     context.DES_EARTH,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
    ENC_LEVEL = 3

    ATTACK = items.Attack( (1,4,0), element = stats.RESIST_PIERCING,
     extra_effect=effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion ))

    def init_monster( self ):
        self.levels.append( base.Beast( 3, self ) )

class WaterBeetle( base.Monster ):
    name = "Water Beetle"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 12, stats.REFLEXES: 8, \
        stats.INTELLIGENCE: 1, stats.PIETY: 1, stats.CHARISMA: 1 }
    SPRITENAME = "monster_bugs.png"
    FRAME = 12
    TEMPLATES = (stats.BUG,stats.WATER)
    MOVE_POINTS = 8
    VOICE = None
    HABITAT = ( context.HAB_TUNNELS, context.SET_EVERY,
     context.DES_WATER,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
    ENC_LEVEL = 3

    ATTACK = items.Attack( (1,4,0), element = stats.RESIST_PIERCING,
     extra_effect=effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ))

    def init_monster( self ):
        self.levels.append( base.Beast( 3, self ) )

class PlagueRat( base.Monster ):
    name = "Plague Rat"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 1, stats.PIETY: 9, stats.CHARISMA: 3 }
    SPRITENAME = "monster_animals.png"
    FRAME = 4
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = None
    HABITAT = ( context.HAB_CAVE, context.HAB_BUILDING, context.HAB_TUNNELS,
     context.SET_EVERY, context.SET_RENFAN,
     context.DES_LUNAR, context.DES_CIVILIZED,
     context.MTY_BEAST, context.GEN_CHAOS, context.GEN_UNDEAD )
    ENC_LEVEL = 3
    COMPANIONS = ( GiantRat, )

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING, extra_effect=
        effects.SavingThrow( roll_skill=stats.MAGIC_DEFENSE, roll_stat=stats.TOUGHNESS, roll_modifier=15, on_failure = (
            effects.StatDamage( stats.TOUGHNESS, anim=animobs.GreenBoom )
        ,))
    )

    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )

class Cow( base.Monster ):
    name = "Cow"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 12, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 1, stats.PIETY: 10, stats.CHARISMA: 4 }
    SPRITENAME = "monster_animals.png"
    FRAME = 22
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_EVERY,
     context.DES_EARTH,
     context.MTY_BEAST, context.MTY_CREATURE )
    ENC_LEVEL = 3

    ATTACK = items.Attack( (2,5,0), element = stats.RESIST_CRUSHING )

    def init_monster( self ):
        self.levels.append( base.Beast( 3, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  4   ***
#  *******************************

class BlackBear( base.Monster ):
    name = "Black Bear"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 16, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 3, stats.PIETY: 8, stats.CHARISMA: 6 }
    SPRITENAME = "monster_animals.png"
    FRAME = 14
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY, context.SET_RENFAN,
     context.MAP_WILDERNESS,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
    ENC_LEVEL = 4

    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING )

    def init_monster( self ):
        self.levels.append( base.Beast( 4, self ) )

class GiantLizard( base.Monster ):
    name = "Giant Lizard"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 13, stats.REFLEXES: 9, \
        stats.INTELLIGENCE: 1, stats.PIETY: 12, stats.CHARISMA: 1 }
    SPRITENAME = "monster_default.png"
    FRAME = 48
    TEMPLATES = (stats.REPTILE,)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY,
     context.MTY_BEAST, context.MTY_CREATURE,
     context.GEN_NATURE, context.GEN_DRAGON )
    ENC_LEVEL = 4

    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 4, self ) )


class FireBat( base.Monster ):
    name = "Fire Bat"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 2, stats.PIETY: 9, stats.CHARISMA: 3, }
    SPRITENAME = "monster_animals.png"
    FRAME = 26
    TEMPLATES = (stats.FIRE,)
    MOVE_POINTS = 14
    VOICE = None
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY, context.DES_FIRE,
     context.DES_LUNAR, context.MTY_BEAST )
    ENC_LEVEL = 4

    ATTACK = items.Attack( (2,4,0), element = stats.RESIST_PIERCING, extra_effect =
         effects.OpposedRoll( att_stat=stats.TOUGHNESS, att_modifier=-10, on_success = (
            effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion ),
            effects.Enchant( enchantments.BurnLowEn )
        ,) )
     )

    TECHNIQUES = ( invocations.MPInvocation( "Fire Breath",
      effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, att_modifier=-10, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion ),
        effects.Enchant( enchantments.BurnLowEn )
      ,), on_failure = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )
      ,) ), com_tar=targetarea.SingleTarget(), shot_anim=animobs.Fireball, ai_tar=invocations.TargetEnemy(), mp_cost=3
    ), )

    def init_monster( self ):
        self.levels.append( base.Beast( 3, self ) )

class IceFox( base.Monster ):
    name = "Ice Fox"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 13, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 3, stats.PIETY: 12, stats.CHARISMA: 15 }
    SPRITENAME = "monster_animals.png"
    FRAME = 27
    TEMPLATES = (stats.ICE,)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.DES_ICE,
     context.MTY_BEAST, context.MTY_CREATURE, context.MTY_BOSS,
     context.GEN_NATURE )
    ENC_LEVEL = 4

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING, extra_effect =
         effects.OpposedRoll( att_stat=None, att_modifier=5, on_success = (
            effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.SnowCloud ),
            effects.Paralyze( max_duration = 6 )
        ,) )
    )

    TECHNIQUES = ( invocations.MPInvocation( "Frost Breath",
        effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
            effects.HealthDamage( (1,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_COLD, anim=animobs.BlueCloud )
        ,), on_failure = (
            effects.HealthDamage( (1,3,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.BlueCloud )
        ,) ), com_tar=targetarea.Cone(reach=4), ai_tar=invocations.TargetEnemy(), mp_cost=3
      ), )

    def init_monster( self ):
        self.levels.append( base.Beast( 4, self ) )

class FireWeasel( base.Monster ):
    name = "Fire Weasel"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 3, stats.PIETY: 14, stats.CHARISMA: 9 }
    SPRITENAME = "monster_animals.png"
    FRAME = 29
    TEMPLATES = (stats.FIRE,)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.DES_FIRE,
     context.MTY_BEAST, context.MTY_CREATURE, context.MTY_BOSS,
     context.GEN_NATURE )
    ENC_LEVEL = 4

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING, extra_effect =
         effects.OpposedRoll( att_stat=None, att_modifier=5, on_success = (
            effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud ),
            effects.Enchant( enchantments.BurnLowEn )
        ,) )
    )

    TECHNIQUES = ( invocations.MPInvocation( "Fire Breath",
        effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
            effects.HealthDamage( (1,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
        ,), on_failure = (
            effects.HealthDamage( (1,3,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
        ,) ), com_tar=targetarea.Cone(reach=4), ai_tar=invocations.TargetEnemy(), mp_cost=3
      ), )

    def init_monster( self ):
        self.levels.append( base.Beast( 4, self ) )


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
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE, 
     context.GEN_GOBLIN )
    ENC_LEVEL = 5
    COMPANIONS = (Wolf,)

    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 5, self ) )

class LightningBug( base.Monster ):
    name = "Lightning Bug"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 13, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 12, stats.CHARISMA: 1, \
        stats.RESIST_LIGHTNING: 150 }
    SPRITENAME = "monster_bugs.png"
    FRAME = 13
    TEMPLATES = (stats.BUG,)
    MOVE_POINTS = 14
    VOICE = None
    HABITAT = ( context.HAB_FOREST, context.HAB_CAVE, context.SET_EVERY,
     context.DES_AIR,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
    ENC_LEVEL = 5

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING )

    TECHNIQUES = ( invocations.MPInvocation( "Zap",
      effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (2,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,) ), com_tar=targetarea.Line(reach=6), ai_tar=invocations.TargetEnemy(), mp_cost=5
    ), )

    def init_monster( self ):
        self.levels.append( base.Beast( 4, self ) )

class Ankheg( base.Monster ):
    # OGL monster http://www.d20srd.org/srd/monsters/ankheg.htm
    name = "Ankheg"
    statline = { stats.STRENGTH: 21, stats.TOUGHNESS: 17, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 1, stats.PIETY: 13, stats.CHARISMA: 6,
        stats.STEALTH: 30 }
    SPRITENAME = "monster_bugs.png"
    FRAME = 40
    TEMPLATES = (stats.BUG,)
    MOVE_POINTS = 10
    VOICE = None
    TREASURE = treasuretype.Swallowed( swag_chance = 35 )
    HABITAT = ( context.HAB_CAVE, context.HAB_TUNNELS, context.SET_EVERY,
     context.DES_EARTH, context.MTY_BOSS,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
    ENC_LEVEL = 5
    ATTACK = items.Attack( (2,6,3), element = stats.RESIST_SLASHING,
     extra_effect=effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion ))
    TECHNIQUES = ( invocations.MPInvocation( "Acid Breath",
      effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (4,4,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,), on_failure = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,) ), com_tar=targetarea.Line(reach=5), ai_tar=invocations.TargetEnemy(), mp_cost=10
    ), )
    def init_monster( self ):
        self.levels.append( base.Defender( 2, self ) )
        self.levels.append( base.Beast( 2, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  6   ***
#  *******************************

class Lion( base.Monster ):
    name = "Lion"
    statline = { stats.STRENGTH: 21, stats.TOUGHNESS: 15, stats.REFLEXES: 17, \
        stats.INTELLIGENCE: 3, stats.PIETY: 12, stats.CHARISMA: 9 }
    SPRITENAME = "monster_animals.png"
    FRAME = 17
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = None
    HABITAT = ( context.SET_EVERY, context.DES_SOLAR,
     context.MAP_WILDERNESS,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
    ENC_LEVEL = 6
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Beast( 6, self ) )

class WildBoar( base.Monster ):
    name = "Wild Boar"
    statline = { stats.STRENGTH: 27, stats.TOUGHNESS: 17, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 2, stats.PIETY: 13, stats.CHARISMA: 8 }
    SPRITENAME = "monster_animals.png"
    FRAME = 40
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY,
     context.DES_EARTH,
     context.MTY_BEAST, context.MTY_CREATURE,
     context.GEN_NATURE )
    ENC_LEVEL = 6
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Beast( 6, self ) )

class TombScorpion( base.Monster ):
    name = "Tomb Scorpion"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 12, stats.REFLEXES: 16, \
        stats.INTELLIGENCE: 1, stats.PIETY: 10, stats.CHARISMA: 1 }
    SPRITENAME = "monster_bugs.png"
    FRAME = 18
    TEMPLATES = (stats.BUG,)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY,
     context.DES_SOLAR, context.DES_LUNAR,
     context.MTY_BEAST, context.MTY_CREATURE )
    ENC_LEVEL = 6
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_PIERCING,
     extra_effect=effects.OpposedRoll( att_stat=None, def_stat=stats.TOUGHNESS, on_success = (
            effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
            effects.Enchant( enchantments.PoisonClassic )
        ,) )
    )
    def init_monster( self ):
        self.levels.append( base.Beast( 6, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  7   ***
#  *******************************

class GrizzlyBear( base.Monster ):
    name = "Grizzly Bear"
    statline = { stats.STRENGTH: 25, stats.TOUGHNESS: 18, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 3, stats.PIETY: 8, stats.CHARISMA: 6 }
    SPRITENAME = "monster_animals.png"
    FRAME = 15
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY, context.SET_RENFAN,
     context.MAP_WILDERNESS,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
    ENC_LEVEL = 7
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Beast( 7, self ) )

class GiantEagle( base.Monster ):
    name = "Giant Eagle"
    statline = { stats.STRENGTH: 17, stats.TOUGHNESS: 15, stats.REFLEXES: 20, \
        stats.INTELLIGENCE: 12, stats.PIETY: 14, stats.CHARISMA: 13 }
    SPRITENAME = "monster_animals.png"
    FRAME = 21
    TEMPLATES = ()
    MOVE_POINTS = 16
    VOICE = None
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY, context.SET_RENFAN,
     context.MAP_WILDERNESS,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE,
     context.DES_AIR, context.DES_SOLAR )
    ENC_LEVEL = 7
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Beast( 8, self ) )

class Scarab( base.Monster ):
    name = "Scarab"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 16, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 1, stats.PIETY: 12, stats.CHARISMA: 1,
        stats.RESIST_SOLAR: 50 }
    SPRITENAME = "monster_bugs.png"
    FRAME = 5
    TEMPLATES = (stats.BUG,)
    MOVE_POINTS = 8
    VOICE = None
    HABITAT = ( context.HAB_TUNNELS, context.SET_EVERY,
     context.DES_SOLAR,
     context.MTY_BEAST, context.MTY_CREATURE )
    ENC_LEVEL = 7
    TECHNIQUES = ( invocations.MPInvocation( "Draining Breath",
        effects.TargetIsEnemy( on_true = (
            effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
                effects.HealthDamage( (1,8,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_FIRE, anim=animobs.PurpleExplosion )
            ,), on_failure = (
                effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.PurpleExplosion )
        ,)),), on_false= (
            effects.NoEffect( anim=animobs.PurpleExplosion )
        ,)), com_tar=targetarea.Cone(reach=4), ai_tar=invocations.TargetEnemy(), mp_cost=3
      ), )
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING,
     extra_effect=abilities.POISON_ATTACK_2d6
    )
    def init_monster( self ):
        self.levels.append( base.Beast( 7, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  8   ***
#  *******************************

class DireYak( base.Monster ):
    name = "Dire Yak"
    statline = { stats.STRENGTH: 23, stats.TOUGHNESS: 14, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 2, stats.PIETY: 12, stats.CHARISMA: 1 }
    SPRITENAME = "monster_animals.png"
    FRAME = 10
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.DES_ICE,
     context.MTY_BEAST, context.MTY_CREATURE,
     context.GEN_NATURE )
    ENC_LEVEL = 8
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Beast( 9, self ) )

class Crocodile( base.Monster ):
    name = "Crocodile"
    statline = { stats.STRENGTH: 25, stats.TOUGHNESS: 18, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 1, stats.PIETY: 10, stats.CHARISMA: 1 }
    SPRITENAME = "monster_animals.png"
    FRAME = 24
    TEMPLATES = (stats.REPTILE,)
    MOVE_POINTS = 8
    VOICE = None
    TREASURE = treasuretype.Swallowed()
    HABITAT = ( context.HAB_TUNNELS, context.SET_EVERY,
     context.DES_WATER, context.MTY_BEAST, context.MTY_CREATURE,
     context.GEN_NATURE, context.GEN_DRAGON )
    ENC_LEVEL = 8
    ATTACK = items.Attack( (1,12,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Beast( 8, self ) )

class FireScorpion( base.Monster ):
    name = "Fire Scorpion"
    statline = { stats.STRENGTH: 19, stats.TOUGHNESS: 13, stats.REFLEXES: 18, \
        stats.INTELLIGENCE: 1, stats.PIETY: 12, stats.CHARISMA: 1 }
    SPRITENAME = "monster_bugs.png"
    FRAME = 16
    TEMPLATES = (stats.BUG,stats.FIRE)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY,
     context.DES_FIRE,
     context.MTY_BEAST, context.MTY_BOSS,
     context.MTY_CREATURE, context.GEN_NATURE )
    ENC_LEVEL = 8
    TECHNIQUES = ( invocations.MPInvocation( "Flamethrower",
        effects.OpposedRoll( on_success = (
            effects.HealthDamage( (2,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.Ignite ),
            effects.Enchant( enchantments.BurnLowEn )
        ,), on_failure = (
            effects.HealthDamage( (2,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.Ignite )
        ,) ), com_tar=targetarea.Line(reach=6), ai_tar=invocations.TargetEnemy(), mp_cost=12
      ), )
    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_PIERCING,
     extra_effect=effects.OpposedRoll( att_stat=None, def_stat=stats.TOUGHNESS, on_success = (
            effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
            effects.Enchant( enchantments.PoisonClassic )
        ,) )
    )
    def init_monster( self ):
        self.levels.append( base.Beast( 8, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  9   ***
#  *******************************

class GreatStag( base.Monster ):
    name = "Great Stag"
    statline = { stats.STRENGTH: 19, stats.TOUGHNESS: 14, stats.REFLEXES: 21, \
        stats.INTELLIGENCE: 3, stats.PIETY: 19, stats.CHARISMA: 16 }
    SPRITENAME = "monster_animals.png"
    FRAME = 20
    TEMPLATES = ()
    MOVE_POINTS = 14
    VOICE = None
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY, context.SET_RENFAN,
     context.MAP_WILDERNESS,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE )
    ENC_LEVEL = 9

    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 9, self ) )

class PolarBear( base.Monster ):
    name = "Polar Bear"
    statline = { stats.STRENGTH: 27, stats.TOUGHNESS: 19, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 1, stats.PIETY: 10, stats.CHARISMA: 6,
        stats.RESIST_FIRE: -50, stats.RESIST_COLD: 50 }
    SPRITENAME = "monster_animals.png"
    FRAME = 16
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.SET_EVERY, context.SET_RENFAN,
     context.DES_ICE,
     context.MAP_WILDERNESS,
     context.MTY_BEAST, context.MTY_CREATURE,
     context.GEN_NATURE )
    ENC_LEVEL = 9
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Beast( 9, self ) )


#  ********************************
#  ***   ENCOUNTER  LEVEL  10   ***
#  ********************************

class Elephant( base.Monster ):
    name = "Elephant"
    statline = { stats.STRENGTH: 30, stats.TOUGHNESS: 25, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 12, stats.CHARISMA: 6 }
    SPRITENAME = "monster_animals.png"
    FRAME = 32
    TEMPLATES = ()
    MOVE_POINTS = 8
    VOICE = None
    HABITAT = ( context.SET_EVERY,
     context.DES_SOLAR,
     context.MTY_BEAST, context.MTY_CREATURE,
     context.GEN_NATURE )
    ENC_LEVEL = 10
    ATTACK = items.Attack( (3,6,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Beast( 10, self ) )


#  ********************************
#  ***   ENCOUNTER  LEVEL  11   ***
#  ********************************



#  ********************************
#  ***   ENCOUNTER  LEVEL  12   ***
#  ********************************

class CaveBear( base.Monster ):
    name = "Cave Bear"
    statline = { stats.STRENGTH: 31, stats.TOUGHNESS: 20, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 12, stats.CHARISMA: 10, \
        stats.RESIST_SLASHING: 25, stats.RESIST_PIERCING: 25, stats.RESIST_CRUSHING: 25 }
    SPRITENAME = "monster_animals.png"
    FRAME = 28
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY,
     context.DES_EARTH,
     context.MTY_BEAST, context.MTY_CREATURE, context.MTY_BOSS,
     context.GEN_NATURE )
    ENC_LEVEL = 12
    ATTACK = items.Attack( (3,6,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Defender( 14, self ) )


#  ********************************
#  ***   ENCOUNTER  LEVEL  13   ***
#  ********************************

class Unicorn( base.Monster ):
    name = "Unicorn"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 18, stats.REFLEXES: 16, \
        stats.INTELLIGENCE: 16, stats.PIETY: 20, stats.CHARISMA: 18, \
        stats.RESIST_LUNAR: 100, stats.MAGIC_DEFENSE: 25 }
    SPRITENAME = "monster_animals.png"
    FRAME = 31
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = None
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY,
     context.DES_SOLAR,
     context.MTY_BEAST, context.MTY_CREATURE, context.MTY_LEADER, context.MTY_BOSS,
     context.GEN_NATURE )
    ENC_LEVEL = 13
    ATTACK = items.Attack( (3,6,0), element = stats.RESIST_PIERCING )
    TECHNIQUES = ( invocations.MPInvocation( "Radiance",
        effects.HealthRestore( dice=(5,8,20) ),
        mp_cost=7, com_tar=targetarea.SingleTarget(reach=10), ai_tar=invocations.TargetWoundedAlly(),
        exp_tar=targetarea.SinglePartyMember(), shot_anim=animobs.YellowVortex ),
    )
    def init_monster( self ):
        self.levels.append( base.Defender( 12, self ) )


#  ********************************
#  ***   ENCOUNTER  LEVEL  14   ***
#  ********************************

class Roc( base.Monster ):
    name = "Roc"
    statline = { stats.STRENGTH: 35, stats.TOUGHNESS: 24, stats.REFLEXES: 18, \
        stats.INTELLIGENCE: 2, stats.PIETY: 13, stats.CHARISMA: 12 }
    SPRITENAME = "monster_animals.png"
    FRAME = 30
    TEMPLATES = ()
    MOVE_POINTS = 16
    VOICE = None
    TREASURE = treasuretype.Swallowed()
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_BEAST, context.MTY_CREATURE, context.GEN_NATURE,
     context.DES_AIR, context.DES_SOLAR )
    ENC_LEVEL = 7
    ATTACK = items.Attack( (3,8,0), element = stats.RESIST_PIERCING )
    TECHNIQUES = ( invocations.MPInvocation( "Wing Sweep",
        effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
            effects.HealthDamage( (3,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_WIND, anim=animobs.Spiral )
        ,), on_failure = (
            effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.Spiral )
        ,) ), com_tar=targetarea.Cone(reach=4), ai_tar=invocations.TargetEnemy(), mp_cost=10
      ), )
    def init_monster( self ):
        self.levels.append( base.Beast( 14, self ) )


#  ********************************
#  ***   ENCOUNTER  LEVEL  15   ***
#  ********************************

class Mammoth( base.Monster ):
    name = "Mammoth"
    statline = { stats.STRENGTH: 30, stats.TOUGHNESS: 40, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 12, stats.CHARISMA: 6, \
        stats.RESIST_COLD: 50 }
    SPRITENAME = "monster_animals.png"
    FRAME = 33
    TEMPLATES = ()
    MOVE_POINTS = 8
    VOICE = None
    HABITAT = ( context.HAB_FOREST, context.SET_EVERY,
     context.DES_ICE,
     context.MTY_BEAST, context.MTY_CREATURE, context.MTY_BOSS,
     context.GEN_NATURE )
    ENC_LEVEL = 15
    COMPANIONS = ( Elephant, DireYak )
    ATTACK = items.Attack( (3,8,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Beast( 18, self ) )


#  ********************************
#  ***   ENCOUNTER  LEVEL  16   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  17   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  18   ***
#  ********************************

class DragonTurtle( base.Monster ):
    name = "Dragon Turtle"
    statline = { stats.STRENGTH: 28, stats.TOUGHNESS: 36, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 6, stats.PIETY: 14, stats.CHARISMA: 6, \
        stats.RESIST_WATER: 50 }
    SPRITENAME = "monster_animals.png"
    FRAME = 34
    TEMPLATES = (stats.REPTILE,stats.DRAGON,stats.WATER)
    MOVE_POINTS = 6
    VOICE = None
    TREASURE = treasuretype.Swallowed()
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_WATER,
     context.MTY_BEAST, context.MTY_CREATURE, context.MTY_BOSS,
     context.GEN_NATURE, context.GEN_DRAGON )
    ENC_LEVEL = 18
    ATTACK = items.Attack( (4,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( invocations.MPInvocation( "Steam Breath",
        effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
            effects.HealthDamage( (10,10,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.Steam )
        ,), on_failure = (
            effects.HealthDamage( (2,20,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.Steam )
        ,) ), com_tar=targetarea.Cone(reach=8), ai_tar=invocations.TargetEnemy(), mp_cost=15
      ), )
    def init_monster( self ):
        self.levels.append( base.Beast( 18, self ) )

#  ********************************
#  ***   ENCOUNTER  LEVEL  19   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  20   ***
#  ********************************


