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
import animals
import enchantments

#  *******************************
#  ***   ENCOUNTER  LEVEL  1   ***
#  *******************************


#  *******************************
#  ***   ENCOUNTER  LEVEL  2   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  3   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  4   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  5   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  6   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  7   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  8   ***
#  *******************************

class Belker( base.Monster ):
    name = "Belker"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 13, stats.REFLEXES: 21, \
        stats.INTELLIGENCE: 6, stats.PIETY: 11, stats.CHARISMA: 11 }
    SPRITENAME = "monster_e_air.png"
    FRAME = 10
    TEMPLATES = (stats.ELEMENTAL,stats.AIR,stats.INCORPOREAL)
    MOVE_POINTS = 12
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_AIR, context.DES_LUNAR, context.MTY_ELEMENTAL )
    ENC_LEVEL = 8
    ATTACK = items.Attack( (2,4,0), element = stats.RESIST_WIND )
    TECHNIQUES = ( invocations.MPInvocation( "Smoke Claw",
        effects.OpposedRoll( att_stat=stats.STRENGTH, def_stat=stats.TOUGHNESS, on_success = (
            effects.HealthDamage( (2,4,0), stat_bonus=stats.STRENGTH, element=stats.RESIST_WIND, anim=animobs.RedBoom ),
            effects.TargetIs( effects.ALIVE, on_true=(
                effects.HealthDamage( (3,4,0), stat_bonus=None, element=None, anim=animobs.BloodSplat ),
                effects.Enchant( enchantments.Bleeding ),
            )),
        ), on_failure = (
            effects.HealthDamage( (2,4,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.RedBoom )
        ,) ), 
        mp_cost=5, com_tar=targetarea.SingleTarget(reach=1), ai_tar=invocations.TargetEnemy() ),
    )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 8, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  9   ***
#  *******************************

class InvisibleStalker( base.Monster ):
    name = "Invisible Stalker"
    statline = { stats.STRENGTH: 18, stats.TOUGHNESS: 14, stats.REFLEXES: 19, \
        stats.INTELLIGENCE: 14, stats.PIETY: 15, stats.CHARISMA: 11,
        stats.PHYSICAL_ATTACK: 5, stats.STEALTH: 50, stats.AWARENESS: 25 }
    SPRITENAME = "monster_e_air.png"
    FRAME = 7
    TEMPLATES = (stats.ELEMENTAL,stats.AIR,stats.INCORPOREAL)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_AIR, context.MTY_ELEMENTAL )
    ENC_LEVEL = 9
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_WIND )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 9, self ) )


#  ********************************
#  ***   ENCOUNTER  LEVEL  10   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  11   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  12   ***
#  ********************************

class AirElemental( base.Monster ):
    name = "Air Elemental"
    statline = { stats.STRENGTH: 20, stats.TOUGHNESS: 20, stats.REFLEXES: 30, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 12,
        stats.RESIST_WIND: 100 }
    SPRITENAME = "monster_e_air.png"
    FRAME = 0
    TEMPLATES = (stats.ELEMENTAL,stats.AIR)
    MOVE_POINTS = 20
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_AIR, context.MTY_ELEMENTAL, context.SUMMON_ELEMENTAL )
    ENC_LEVEL = 12
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING, extra_effect =
        effects.HealthDamage( (1,10,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.Spiral )
    )
    TECHNIQUES = ( invocations.MPInvocation( "Tornado",
        effects.OpposedRoll( def_stat=stats.REFLEXES, on_success = (
            effects.HealthDamage( (3,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.Spiral )
        ,), on_failure = (
            effects.HealthDamage( (1,12,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.Spiral )
        ,) ), mp_cost=10, com_tar=targetarea.Blast(radius=3), shot_anim=animobs.Whirlwind, ai_tar=invocations.TargetEnemy() ),
        invocations.MPInvocation( "Lightning Bolt",
        effects.OpposedRoll( def_stat=stats.REFLEXES, on_success = (
            effects.HealthDamage( (3,12,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap )
        ,), on_failure = (
            effects.HealthDamage( (2,10,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap )
        ,) ), 
        mp_cost=5, com_tar=targetarea.SingleTarget(), shot_anim=animobs.Lightning, ai_tar=invocations.TargetEnemy() )
    )
    def init_monster( self ):
        self.levels.append( base.Beast( 12, self ) )


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


