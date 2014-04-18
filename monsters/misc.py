import base
import stats
import items
import dialogue
import context
import spells
import invocations
import effects
import animobs
import targetarea
import aibrain
import animals

# Contains critters that don't quite fit in anywhere else.

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

class Cockatrice( base.Monster ):
    name = "Cockatrice"
    statline = { stats.STRENGTH: 8, stats.TOUGHNESS: 8, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 1, stats.PIETY: 10, stats.CHARISMA: 4 }
    SPRITENAME = "monster_default.png"
    FRAME = 21
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.SET_RENFAN,
     context.DES_AIR, context.DES_EARTH,
     context.MTY_BEAST )
    ENC_LEVEL = 4
    COMPANIONS = (animals.Chicken,)
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING, skill_mod=stats.REFLEXES )
    TECHNIQUES = ( invocations.MPInvocation( "Death Gaze",
      effects.OpposedRoll( att_stat=stats.PIETY, att_modifier=-20, on_success = (
        effects.InstaKill( anim=animobs.CriticalHit )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=4), shot_anim=animobs.PurpleVortex, ai_tar=invocations.vs_enemy, mp_cost=4
    ), )
    def init_monster( self ):
        self.levels.append( base.Beast( 3, self ) )


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



