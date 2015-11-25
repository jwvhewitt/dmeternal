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
import random
import treasuretype

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

#  *******************************
#  ***   ENCOUNTER  LEVEL  9   ***
#  *******************************

class Xorn( base.Monster ):
    name = "Xorn"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 15, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 12, stats.CHARISMA: 10, \
        stats.RESIST_PIERCING: 50, stats.RESIST_SLASHING: 50, stats.RESIST_FIRE: 100, \
        stats.RESIST_COLD: 100, stats.STEALTH: 40 }
    SPRITENAME = "monster_e_earth.png"
    FRAME = 5
    TEMPLATES = (stats.ELEMENTAL,stats.EARTH)
    MOVE_POINTS = 4
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY,
     context.MTY_BOSS, context.MTY_ELEMENTAL, context.GEN_TERRAN,
     context.DES_EARTH )
    ENC_LEVEL = 9
    TREASURE = treasuretype.Standard( (items.GEM, ) )
    ATTACK = items.Attack( (3,4,0), element = stats.RESIST_SLASHING)

    def init_monster( self ):
        self.levels.append( base.Defender( 9, self ) )


#  ********************************
#  ***   ENCOUNTER  LEVEL  10   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  11   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  12   ***
#  ********************************

class EarthElemental( base.Monster ):
    name = "Earth Elemental"
    statline = { stats.STRENGTH: 25, stats.TOUGHNESS: 35, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 12,
        stats.RESIST_ACID: 100 }
    SPRITENAME = "monster_e_earth.png"
    FRAME = 1
    TEMPLATES = (stats.ELEMENTAL,stats.EARTH)
    MOVE_POINTS = 6
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_EARTH, context.MTY_ELEMENTAL, context.GEN_TERRAN,
     context.SUMMON_ELEMENTAL )
    ENC_LEVEL = 12

    ATTACK = items.Attack( (3,10,0), element = stats.RESIST_CRUSHING)

    TECHNIQUES = ( invocations.MPInvocation( "Earthquake",
        effects.TargetIsEnemy( anim=animobs.EarthBoom, on_true = (
            effects.OpposedRoll( def_stat=stats.REFLEXES, on_success = (
                effects.HealthDamage( (5,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_CRUSHING, anim=animobs.RedBoom )
            ,), on_failure = (
                effects.HealthDamage( (1,12,0), stat_bonus=None, element=stats.RESIST_CRUSHING, anim=animobs.RedBoom )
            ,) )
        ,) ), mp_cost=15, com_tar=targetarea.SelfCentered(radius=8,delay_from=-1,exclude_middle=True),
        ai_tar=invocations.TargetEnemy() ),
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


