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
from .. import spells
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

class Avoral( base.Monster ):
    name = "Avoral"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 20, stats.REFLEXES: 23, \
        stats.INTELLIGENCE: 15, stats.PIETY: 16, stats.CHARISMA: 16, \
        stats.AWARENESS: 65, stats.MAGIC_DEFENSE: 25 }
    SPRITENAME = "monster_celestial.png"
    FRAME = 12
    TEMPLATES = (stats.CELESTIAL,stats.AIR)
    MOVE_POINTS = 16
    HABITAT = ( context.SET_EVERY,
     context.DES_SOLAR, context.DES_AIR,
     context.MTY_HUMANOID, context.MTY_CELESTIAL )
    ENC_LEVEL = 12
    COMBAT_AI = aibrain.ArcherAI()
    TREASURE = treasuretype.Standard()
    TECHNIQUES = ( invocations.Invocation("Avoral Missile",
        effects.HealthDamage((1,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion ),
        com_tar=targetarea.SingleTarget(), shot_anim=animobs.WizardMissile,
        ai_tar=invocations.TargetEnemy() ),
      invocations.Invocation( "Hold Person",
        effects.OpposedRoll( att_modifier=20, on_success = (
            effects.Paralyze( max_duration = 3 )
        ,), on_failure =(
            effects.NoEffect( anim=animobs.SmallBoom )
        ,) ), com_tar=targetarea.SingleTarget(), shot_anim=animobs.BlueComet,
        ai_tar=invocations.TargetMobileEnemy() ),
      invocations.MPInvocation( "Thunder Strike",
        effects.OpposedRoll( on_success = (
            effects.HealthDamage( (3,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
        ,), on_failure = (
            effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
        ,) ), mp_cost=16, com_tar=targetarea.Line(), ai_tar=invocations.TargetEnemy() )
    )
    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Terror( 7, self ) )

#  ********************************
#  ***   ENCOUNTER  LEVEL  12   ***
#  ********************************

class HoundArchon( base.Monster ):
    name = "Hound Archon"
    statline = { stats.STRENGTH: 23, stats.TOUGHNESS: 17, stats.REFLEXES: 8, \
        stats.INTELLIGENCE: 10, stats.PIETY: 13, stats.CHARISMA: 12, \
        stats.AWARENESS: 25, stats.CRITICAL_HIT: 20 }
    SPRITENAME = "monster_celestial.png"
    FRAME = 0
    TEMPLATES = (stats.CELESTIAL,)
    MOVE_POINTS = 16
    HABITAT = ( context.SET_EVERY,
     context.DES_SOLAR,
     context.MTY_HUMANOID, context.MTY_CELESTIAL )
    ENC_LEVEL = 12
    TREASURE = treasuretype.HighItems( ( None, items.POTION, items.SWORD ) )
    TECHNIQUES = ( spells.priestspells.HEROISM, )
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING, extra_effect =
        effects.HealthDamage( (1,4,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
    )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 14, self ) )



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

class Planetar( base.Monster ):
    name = "Planetar"
    statline = { stats.STRENGTH: 25, stats.TOUGHNESS: 20, stats.REFLEXES: 19, \
        stats.INTELLIGENCE: 22, stats.PIETY: 23, stats.CHARISMA: 22,
        stats.MAGIC_DEFENSE: 50, stats.RESIST_CRUSHING: 75, stats.RESIST_PIERCING: 75,
        stats.RESIST_SLASHING: 75 }
    SPRITENAME = "monster_celestial.png"
    FRAME = 4
    TEMPLATES = (stats.CELESTIAL,)
    MOVE_POINTS = 12
    HABITAT = ( context.SET_EVERY,
     context.DES_SOLAR, context.MTY_CELESTIAL )
    ENC_LEVEL = 18
    TREASURE = treasuretype.HighItems( ( None, items.POTION, items.SCROLL ) )
    ATTACK = items.Attack( (3,6,0), element = stats.RESIST_SLASHING, extra_effect =
        effects.HealthDamage( (1,10,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
    )
    # Planetars are supposed to get a whole lot more abilities; fill in later.
    TECHNIQUES = ( spells.solarspells.RENEWAL, spells.solarspells.SUNBURST,

    )
    def init_monster( self ):
        self.levels.append( base.Terror( 16, self ) )
        self.condition.append( enchantments.PermaMegaRegeneration() )


#  ********************************
#  ***   ENCOUNTER  LEVEL  19   ***
#  ********************************


#  ********************************
#  ***   ENCOUNTER  LEVEL  20   ***
#  ********************************


