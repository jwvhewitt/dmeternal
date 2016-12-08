import base
from .. import stats
from .. import items
from .. import dialogue
from .. import context
from .. import spells
from .. import invocations
from .. import effects
from .. import animobs
from .. import targetarea
from .. import aibrain
import random
import animals
import undead

#  *******************************
#  ***   ENCOUNTER  LEVEL  1   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  2   ***
#  *******************************

class GreySlime( base.Monster ):
    name = "Grey Slime"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 1, stats.PIETY: 1, stats.CHARISMA: 1,
        stats.RESIST_SLASHING: 50, stats.RESIST_PIERCING: 50 }
    SPRITENAME = "monster_plants.png"
    FRAME = 2
    TEMPLATES = (stats.PLANT,)
    MOVE_POINTS = 6
    HABITAT = ( context.HAB_CAVE, context.HAB_TUNNELS,
     context.SET_EVERY, context.DES_EARTH, context.MTY_BEAST,
     context.MTY_PLANT, context.GEN_NATURE )
    ENC_LEVEL = 2
    COMBAT_AI = aibrain.BrainDeadAI()
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_ACID, damage_mod=None,
        hit_anim=animobs.GreenExplosion )
    def mitose( self, element ):
        return element in ( stats.RESIST_SLASHING, stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )


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


