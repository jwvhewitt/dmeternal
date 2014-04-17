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
import spells

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

class Salamander( base.Monster ):
    name = "Salamander"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 14, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 13, stats.PIETY: 15, stats.CHARISMA: 13 }
    SPRITENAME = "monster_e_fire.png"
    FRAME = 8
    TEMPLATES = (stats.ELEMENTAL,stats.FIRE)
    MOVE_POINTS = 6
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_FIRE,
     context.MTY_HUMANOID, context.MTY_FIGHTER )
    ENC_LEVEL = 8

    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_PIERCING, reach=2, extra_effect =
        effects.HealthDamage( (1,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE)
    )

    TECHNIQUES = ( spells.firespells.EXPLOSION, )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 8, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  9   ***
#  *******************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  10   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  11   ***
#  ********************************

class SalamanderLeader( base.Monster ):
    name = "Salamander Leader"
    statline = { stats.STRENGTH: 24, stats.TOUGHNESS: 16, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 16, stats.PIETY: 17, stats.CHARISMA: 15 }
    SPRITENAME = "monster_e_fire.png"
    FRAME = 9
    TEMPLATES = (stats.ELEMENTAL,stats.FIRE)
    MOVE_POINTS = 6
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_FIRE,
     context.MTY_HUMANOID, context.MTY_LEADER )
    ENC_LEVEL = 11
    LONER = True
    COMPANIONS = (Salamander,)

    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_SLASHING, extra_effect =
        effects.HealthDamage( (1,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE)
    )

    TECHNIQUES = ( spells.firespells.PYROTECHNICS, spells.airspells.DISPEL_MAGIC )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 11, self ) )


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


