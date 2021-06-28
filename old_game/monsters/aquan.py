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

#  ********************************
#  ***   ENCOUNTER  LEVEL  10   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  11   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  12   ***
#  ********************************

class WaterElemental( base.Monster ):
    name = "Water Elemental"
    statline = { stats.STRENGTH: 25, stats.TOUGHNESS: 25, stats.REFLEXES: 20, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 12,
        stats.RESIST_WATER: 100 }
    SPRITENAME = "monster_e_water.png"
    FRAME = 0
    TEMPLATES = (stats.ELEMENTAL,stats.WATER)
    MOVE_POINTS = 20
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_WATER, context.SUMMON_ELEMENTAL )
    ENC_LEVEL = 12
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_CRUSHING, extra_effect =
        effects.HealthDamage( (1,10,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WATER, anim=animobs.Spiral )
    )
    TECHNIQUES = ( invocations.MPInvocation( "Tidal Wave",
        effects.OpposedRoll( def_stat=stats.REFLEXES, on_success = (
            effects.HealthDamage( (3,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WATER, anim=animobs.Bubbles )
        ,), on_failure = (
            effects.HealthDamage( (1,12,0), stat_bonus=None, element=stats.RESIST_WATER, anim=animobs.Bubbles )
        ,) ), mp_cost=10, com_tar=targetarea.Cone(), ai_tar=invocations.TargetEnemy() ),
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


