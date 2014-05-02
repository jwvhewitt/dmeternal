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

class EvilEye( base.Monster ):
    name = "Evil Eye"
    statline = { stats.STRENGTH: 6, stats.TOUGHNESS: 12, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 2 }
    SPRITENAME = "monster_default.png"
    FRAME = 18
    TEMPLATES = ()
    MOVE_POINTS = 6
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_CAVE, context.HAB_TUNNELS, context.SET_EVERY,
     context.DES_LUNAR,
     context.MTY_BEAST, context.GEN_CHAOS )
    ENC_LEVEL = 3
    ATTACK = items.Attack( (2,4,0), element = stats.RESIST_LUNAR,
     skill_mod=stats.REFLEXES, hit_anim=animobs.PurpleExplosion )
    TECHNIQUES = ( invocations.MPInvocation( "Evil Gaze",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.Paralyze( max_duration = 3 )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=4), shot_anim=animobs.PurpleVortex, ai_tar=invocations.vs_enemy, mp_cost=3
    ), )
    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )

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
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.SET_RENFAN,
     context.DES_AIR, context.DES_EARTH,
     context.MTY_BEAST )
    ENC_LEVEL = 4
    COMPANIONS = (animals.Chicken,)
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING, skill_mod=stats.REFLEXES )
    TECHNIQUES = ( invocations.MPInvocation( "Death Gaze",
      effects.OpposedRoll( att_stat=stats.PIETY, att_modifier=-10, on_success = (
        effects.InstaKill( anim=animobs.CriticalHit )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=4), shot_anim=animobs.PurpleVortex, ai_tar=invocations.vs_enemy, mp_cost=4
    ), )
    def init_monster( self ):
        self.levels.append( base.Beast( 3, self ) )

class CorpseEater( base.Monster ):
    name = "Corpse Eater"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 14, stats.REFLEXES: 8, \
        stats.INTELLIGENCE: 2, stats.PIETY: 12, stats.CHARISMA: 2 }
    SPRITENAME = "monster_default.png"
    FRAME = 13
    TEMPLATES = (stats.BUG,)
    MOVE_POINTS = 8
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.DES_LUNAR,
     context.MTY_BEAST )
    ENC_LEVEL = 4
    ATTACK = items.Attack( (3,4,0), element = stats.RESIST_PIERCING, extra_effect =
         effects.OpposedRoll( att_stat=stats.TOUGHNESS, on_success = (
            effects.Paralyze( max_duration = 6 )
        ,) )
     )
    TECHNIQUES = ( invocations.MPInvocation( "Tentacle Slime",
      effects.TargetIsEnemy( on_true = (
          effects.OpposedRoll( anim=animobs.GreenSplat, att_stat=stats.TOUGHNESS, on_success = (
            effects.Paralyze( max_duration = 3 )
          ,), on_failure = (
            effects.NoEffect( anim=animobs.SmallBoom )
          ,) ),
          )
      ), com_tar=targetarea.SelfCentered(radius=1,exclude_middle=True), ai_tar=invocations.vs_enemy, mp_cost=8 ), )
    def init_monster( self ):
        self.levels.append( base.Beast( 4, self ) )


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



