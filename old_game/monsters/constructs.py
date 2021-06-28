from . import base
from .. import stats
from .. import items
from .. import dialogue
from .. import context
from .. import aibrain
from .. import effects
from .. import animobs
from .. import targetarea
from .. import invocations
from . import animals
from .. import enchantments
from .. import items
import random
from . import treasuretype

#  *******************************
#  ***   ENCOUNTER  LEVEL  1   ***
#  *******************************


#  *******************************
#  ***   ENCOUNTER  LEVEL  2   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  3   ***
#  *******************************

class PewterGolem( base.Monster ):
    name = "Pewter Golem"
    statline = { stats.STRENGTH: 17, stats.TOUGHNESS: 13, stats.REFLEXES: 8, \
        stats.INTELLIGENCE: 1, stats.PIETY: 11, stats.CHARISMA: 13 }
    SPRITENAME = "monster_constructs.png"
    FRAME = 10
    TEMPLATES = (stats.CONSTRUCT,)
    MOVE_POINTS = 8
    VOICE = None
    HABITAT = ( context.HAB_BUILDING, context.SET_EVERY,
     context.MTY_CONSTRUCT, )
    ENC_LEVEL = 3
    COMBAT_AI = aibrain.SteadyAI()
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Defender( 3, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  4   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  5   ***
#  *******************************

class ClockworkSoldier( base.Monster ):
    name = "Clockwork Soldier"
    statline = { stats.STRENGTH: 18, stats.TOUGHNESS: 18, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 12, stats.CHARISMA: 8, \
        stats.RESIST_LIGHTNING: -150 }
    SPRITENAME = "monster_constructs.png"
    FRAME = 11
    TEMPLATES = (stats.CONSTRUCT,)
    MOVE_POINTS = 8
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.HAB_TUNNELS, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_CONSTRUCT, context.MTY_FIGHTER )
    ENC_LEVEL = 5
    COMBAT_AI = aibrain.BrainDeadAI()
    # Clockwork soldiers don't have normal treasure, but may drop a nice sword.
    TREASURE = treasuretype.Standard( (items.SWORD,), swag_chance=25, swag_quality=2, scale=0 )
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Defender( 5, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  6   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  7   ***
#  *******************************

class LivingPotion( base.Monster ):
    name = "Living Potion"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 1,
        stats.RESIST_SLASHING: 25, stats.RESIST_PIERCING: 25, stats.RESIST_WATER: 200 }
    SPRITENAME = "monster_constructs.png"
    FRAME = 15
    TEMPLATES = (stats.CONSTRUCT,)
    MOVE_POINTS = 12
    VOICE = None
    HABITAT = ( context.SET_EVERY,
     context.MTY_CONSTRUCT, 
     context.DES_WATER )
    ENC_LEVEL = 7
    TREASURE = treasuretype.Standard( (items.POTION,) )
    COMBAT_AI = aibrain.SteadySpellAI()
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( invocations.MPInvocation( "Acid Blast",
      effects.OpposedRoll( att_modifier=10, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (2,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenCloud )
      ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenCloud )
      ,) ), com_tar=targetarea.SingleTarget(), ai_tar=invocations.TargetEnemy(), shot_anim=animobs.GreenSpray, mp_cost=1 ),
    invocations.MPInvocation( "Poison Blast",
      effects.OpposedRoll( att_modifier=10, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (2,6,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud )
      ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud )
      ,) ), com_tar=targetarea.SingleTarget(), ai_tar=invocations.TargetEnemy(), shot_anim=animobs.GreenComet, mp_cost=1 ),
    invocations.MPInvocation( "Healing Potion",
        effects.HealthRestore( dice=(3,8,0) ),
        com_tar=targetarea.SingleTarget(reach=10), ai_tar=invocations.TargetWoundedAlly(),
        exp_tar=targetarea.SinglePartyMember(), shot_anim=animobs.YellowVortex, mp_cost=1
       )
    )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 7, self ) )

class AnimatedSword( base.Monster ):
    name = "Animated Sword"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 10, stats.CHARISMA: 1,
        stats.RESIST_SLASHING: 50, stats.COUNTER_ATTACK: 50 }
    SPRITENAME = "monster_constructs.png"
    FRAME = 16
    TEMPLATES = (stats.CONSTRUCT,)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.SET_EVERY,
     context.MTY_CONSTRUCT, 
     context.DES_AIR )
    ENC_LEVEL = 7
    COMBAT_AI = aibrain.SteadyAI()
    ATTACK = items.Attack( (1,12,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Beast( 7, self ) )

class AnimatedFlail( base.Monster ):
    name = "Animated Flail"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 10, stats.CHARISMA: 1,
        stats.RESIST_CRUSHING: 50 }
    SPRITENAME = "monster_constructs.png"
    FRAME = 17
    TEMPLATES = (stats.CONSTRUCT,)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.SET_EVERY,
     context.MTY_CONSTRUCT, 
     context.DES_EARTH )
    ENC_LEVEL = 7
    COMBAT_AI = aibrain.SteadyAI()
    ATTACK = items.Attack( (3,6,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Beast( 7, self ) )

class CreepingCoins( base.Monster ):
    name = "Creeping Coins"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 10, stats.CHARISMA: 1, \
        stats.RESIST_COLD: 155 }
    SPRITENAME = "monster_constructs.png"
    FRAME = 18
    TEMPLATES = (stats.CONSTRUCT,)
    MOVE_POINTS = 6
    VOICE = None
    HABITAT = ( context.HAB_CAVE, context.SET_RENFAN,
     context.MTY_CONSTRUCT, 
     context.DES_ICE )
    ENC_LEVEL = 7
    TREASURE = treasuretype.High()
    COMBAT_AI = aibrain.SteadyAI()
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( invocations.MPInvocation( "Cold Blast",
      effects.OpposedRoll( att_modifier=10, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,10,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
      ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
      ,) ), com_tar=targetarea.Cone(reach=5), ai_tar=invocations.TargetEnemy(), mp_cost=1 ),
    )
    def init_monster( self ):
        self.levels.append( base.Defender( 6, self ) )

class AnimatedCandlestick( base.Monster ):
    name = "Candlestick"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 12 }
    SPRITENAME = "monster_constructs.png"
    FRAME = 19
    TEMPLATES = (stats.CONSTRUCT,)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_BUILDING, context.SET_EVERY,
     context.MTY_CONSTRUCT, 
     context.DES_FIRE )
    ENC_LEVEL = 7
    COMBAT_AI = aibrain.SteadyAI()
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_PIERCING, extra_effect=
        effects.OpposedRoll( att_modifier=-10, on_success = (
            effects.Enchant( enchantments.BurnLowEn, anim=animobs.RedCloud )
        ,))
    )
    TECHNIQUES = ( invocations.MPInvocation( "Fireball",
      effects.OpposedRoll( def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,10,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud ),
      ), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud ),
      ) ), com_tar=targetarea.SingleTarget(), ai_tar=invocations.TargetEnemy(), shot_anim=animobs.Fireball, mp_cost=5 ),
    )
    def init_monster( self ):
        self.levels.append( base.Beast( 7, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  8   ***
#  *******************************

class LivingStatue( base.Monster ):
    name = "Living Statue"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 13, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 1, \
        stats.RESIST_FIRE: 155 }
    SPRITENAME = "monster_constructs.png"
    FRAME = 13
    TEMPLATES = (stats.CONSTRUCT,)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_BUILDING, context.HAB_TUNNELS, context.SET_EVERY,
     context.MTY_CONSTRUCT, 
     context.DES_FIRE, context.DES_SOLAR )
    ENC_LEVEL = 8
    TREASURE = treasuretype.Low()
    COMBAT_AI = aibrain.SteadyAI()
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Magma Blast",
      effects.OpposedRoll( att_modifier=10, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (2,8,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )
      ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )
      ,) ), com_tar=targetarea.Line(), ai_tar=invocations.TargetEnemy(), mp_cost=1 ),
    )
    def init_monster( self ):
        self.levels.append( base.Defender( 7, self ) )


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

class FlamingSword( base.Monster ):
    name = "Flaming Sword"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 14, stats.REFLEXES: 18, \
        stats.INTELLIGENCE: 12, stats.PIETY: 20, stats.CHARISMA: 14,
        stats.RESIST_SLASHING: 50, stats.MAGIC_DEFENSE: 50, stats.COUNTER_ATTACK: 50 }
    SPRITENAME = "monster_constructs.png"
    FRAME = 9
    TEMPLATES = (stats.CONSTRUCT,)
    MOVE_POINTS = 12
    VOICE = None
    HABITAT = ( context.SET_EVERY,
     context.MTY_CONSTRUCT, 
     context.DES_AIR, context.DES_FIRE,
     context.SUMMON_FLAMINGSWORD )
    ENC_LEVEL = 14
    COMBAT_AI = aibrain.SteadyAI()
    ATTACK = items.Attack( (3,8,0), element = stats.RESIST_SLASHING, extra_effect=
        effects.OpposedRoll( on_success = (
            effects.HealthDamage( (3,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.RedCloud ),
            effects.Enchant( enchantments.BurnLowEn )
        ), on_failure = (
            effects.HealthDamage( (3,8,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud ),
        ) )
    )
    def init_monster( self ):
        self.levels.append( base.Defender( 14, self ) )

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


