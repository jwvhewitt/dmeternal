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

class FireElemental( base.Monster ):
    name = "Fire Elemental"
    statline = { stats.STRENGTH: 35, stats.TOUGHNESS: 15, stats.REFLEXES: 20, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 12,
        stats.RESIST_FIRE: 100 }
    SPRITENAME = "monster_e_fire.png"
    FRAME = 0
    TEMPLATES = (stats.ELEMENTAL,stats.FIRE)
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_FIRE, context.SUMMON_ELEMENTAL )
    ENC_LEVEL = 12

    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_ATOMIC, extra_effect =
        effects.HealthDamage( (2,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.RedCloud,
            on_success=( effects.Enchant( enchantments.BurnLowEn ),
            )
        )
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


