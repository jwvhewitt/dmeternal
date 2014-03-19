import base
import stats
import items
import dialogue
import context
import aibrain
import effects
import animobs
import targetarea
import invocations

#  *******************************
#  ***   ENCOUNTER  LEVEL  1   ***
#  *******************************

class SkeletalHound( base.Monster ):
    name = "Skeletal Hound"
    statline = { stats.STRENGTH: 9, stats.TOUGHNESS: 9, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 1, stats.PIETY: 1, stats.CHARISMA: 1 }
    SPRITENAME = "monster_undead2.png"
    FRAME = 0
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_LUNAR,
     context.MTY_UNDEAD, context.MTY_BEAST,
     context.GEN_UNDEAD )
    ENC_LEVEL = 1

    COMBAT_AI = aibrain.BrainDeadAI()

    ATTACK = items.Attack( (1,4,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 1, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  2   ***
#  *******************************

class Skeleton( base.Monster ):
    name = "Skeleton"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 1 }
    SPRITENAME = "monster_undead.png"
    FRAME = 0
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 5
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MTY_UNDEAD, 
     context.DES_LUNAR, context.GEN_UNDEAD )
    ENC_LEVEL = 2
    COMPANIONS = (SkeletalHound,)

    COMBAT_AI = aibrain.SteadyAI()

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )

class SkeletonWithDagger( base.Monster ):
    name = "Skeleton"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 1 }
    SPRITENAME = "monster_undead.png"
    FRAME = 1
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 10
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_UNDEAD, 
     context.DES_LUNAR, context.GEN_UNDEAD )
    ENC_LEVEL = 2
    COMPANIONS = (Skeleton,)

    COMBAT_AI = aibrain.SteadyAI()

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_SLASHING )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  3   ***
#  *******************************

class Zombie( base.Monster ):
    name = "Zombie"
    statline = { stats.STRENGTH: 11, stats.TOUGHNESS: 14, stats.REFLEXES: 4, \
        stats.INTELLIGENCE: 2, stats.PIETY: 8, stats.CHARISMA: 1, \
        stats.RESIST_CRUSHING: 50, stats.RESIST_FIRE: 50, stats.RESIST_PIERCING: 50 }
    SPRITENAME = "monster_undead.png"
    FRAME = 9
    TEMPLATES = (stats.UNDEAD,)
    MOVE_POINTS = 6
    VOICE = None
    GP_VALUE = 5
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MTY_UNDEAD, 
     context.DES_LUNAR, context.GEN_UNDEAD )
    ENC_LEVEL = 3

    COMBAT_AI = aibrain.BrainDeadAI()

    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_CRUSHING )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )

class SkeletonWithMorningstar( base.Monster ):
    name = "Skeleton"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 1 }
    SPRITENAME = "monster_undead.png"
    FRAME = 3
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 15
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_UNDEAD, 
     context.DES_LUNAR, context.GEN_UNDEAD )
    ENC_LEVEL = 3
    COMPANIONS = (Skeleton,SkeletonWithDagger)

    COMBAT_AI = aibrain.SteadyAI()

    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  4   ***
#  *******************************

class Ghoul( base.Monster ):
    name = "Ghoul"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 15, stats.REFLEXES: 8, \
        stats.INTELLIGENCE: 11, stats.PIETY: 10, stats.CHARISMA: 4, \
        stats.RESIST_FIRE: 50, stats.RESIST_PIERCING: 50 }
    SPRITENAME = "monster_undead.png"
    FRAME = 35
    TEMPLATES = (stats.UNDEAD,)
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 50
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MTY_UNDEAD, 
     context.DES_LUNAR, context.GEN_UNDEAD )
    ENC_LEVEL = 4
    COMPANIONS = (Zombie,)

    COMBAT_AI = aibrain.GhoulAI()

    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING, extra_effect =
         effects.OpposedRoll( att_modifier=-10, on_success = (
            effects.Paralyze( max_duration = 6 )
        ,) )
     )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  5   ***
#  *******************************

class PlagueZombie( base.Monster ):
    name = "Plague Zombie"
    statline = { stats.STRENGTH: 11, stats.TOUGHNESS: 14, stats.REFLEXES: 4, \
        stats.INTELLIGENCE: 2, stats.PIETY: 8, stats.CHARISMA: 1, \
        stats.RESIST_CRUSHING: 50, stats.RESIST_FIRE: 50, stats.RESIST_PIERCING: 50 }
    SPRITENAME = "monster_undead.png"
    FRAME = 10
    TEMPLATES = (stats.UNDEAD,)
    MOVE_POINTS = 6
    VOICE = None
    GP_VALUE = 25
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_UNDEAD, 
     context.DES_LUNAR, context.GEN_UNDEAD )
    ENC_LEVEL = 5
    COMPANIONS = (Zombie,)
    COMBAT_AI = aibrain.BrainDeadAI()

    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_CRUSHING, extra_effect=
        effects.SavingThrow( roll_skill=stats.RESIST_LUNAR, roll_stat=stats.TOUGHNESS, on_failure = (
            effects.StatDamage( stats.TOUGHNESS, anim=animobs.GreenBoom )
        ,))
    )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 6, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  6   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  7   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  8   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  9   ***
#  *******************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  10   ***
#  ********************************


class Fossil( base.Monster ):
    name = "Fossil"
    statline = { stats.STRENGTH: 24, stats.TOUGHNESS: 19, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 14, stats.CHARISMA: 1 }
    SPRITENAME = "monster_undead2.png"
    FRAME = 11
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 6
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY,
     context.DES_LUNAR, context.DES_EARTH,
     context.MTY_UNDEAD, context.MTY_BEAST,
     context.GEN_NATURE )
    ENC_LEVEL = 10

    COMBAT_AI = aibrain.BrainDeadAI()

    ATTACK = items.Attack( (3,8,0), element = stats.RESIST_CRUSHING )

    TECHNIQUES = ( invocations.MPInvocation( "Hellfire",
      effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, att_modifier=10, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,10,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion )
      ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion )
      ,) ), com_tar=targetarea.Blast(radius=2), shot_anim=animobs.MysticBolt, ai_tar=invocations.vs_enemy, mp_cost=3
    ), )

    def init_monster( self ):
        self.levels.append( base.Beast( 10, self ) )

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



