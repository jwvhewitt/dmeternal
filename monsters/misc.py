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
import treasuretype

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
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 2, \
        stats.MAGIC_ATTACK: 20, stats.MAGIC_DEFENSE: 10 }
    SPRITENAME = "monster_default.png"
    FRAME = 18
    TEMPLATES = ()
    MOVE_POINTS = 6
    VOICE = None
    HABITAT = ( context.HAB_CAVE, context.HAB_TUNNELS, context.SET_EVERY,
     context.DES_LUNAR,
     context.MTY_BEAST, context.GEN_CHAOS )
    ENC_LEVEL = 3
    ATTACK = items.Attack( (2,4,0), element = stats.RESIST_LUNAR,
     skill_mod=stats.REFLEXES, hit_anim=animobs.PurpleExplosion, extra_effect =
         effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
            effects.Paralyze( max_duration = 3 )
        ,) )
     )
    TECHNIQUES = ( invocations.MPInvocation( "Evil Gaze",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, att_modifier=10, on_success = (
        effects.Paralyze( max_duration = 3 )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=4), shot_anim=animobs.PurpleVortex, ai_tar=invocations.TargetEnemy(), mp_cost=3
    ), )
    def init_monster( self ):
        self.levels.append( base.Beast( 3, self ) )

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
      ,) ), com_tar=targetarea.SingleTarget(reach=4), shot_anim=animobs.PurpleVortex, ai_tar=invocations.TargetEnemy(), mp_cost=4
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
      ), com_tar=targetarea.SelfCentered(radius=1,exclude_middle=True), ai_tar=invocations.TargetEnemy(), mp_cost=8 ), )
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

class Lamia( base.Monster ):
    name = "Lamia"    
    statline = { stats.STRENGTH: 18, stats.TOUGHNESS: 12, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 13, stats.PIETY: 15, stats.CHARISMA: 12 }
    SPRITENAME = "monster_default.png"
    FRAME = 2
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_DESERT, context.SET_EVERY,
     context.DES_LUNAR,
     context.MTY_HUMANOID, context.MTY_BOSS )
    ENC_LEVEL = 7
    TREASURE = treasuretype.HighItems()
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_SLASHING, extra_effect=
        effects.StatDamage( stats.PIETY, amount=4, anim=animobs.GreenBoom )
    )
    TECHNIQUES = ( invocations.MPInvocation( "Spirit Drain",
        effects.TargetIsEnemy( on_true = (
            effects.OpposedRoll( on_success = (
                effects.ManaDamage( (1,8,0), stat_bonus=stats.TOUGHNESS, anim=animobs.PurpleExplosion ),
                effects.CauseSleep()
            ,), on_failure = (
                effects.ManaDamage( (1,8,0), stat_bonus=None, anim=animobs.PurpleExplosion )
        ,)),), on_false= (
            effects.NoEffect( anim=animobs.PurpleExplosion )
        ,)), com_tar=targetarea.Cone(reach=4), ai_tar=invocations.TargetEnemy(), mp_cost=12
      ), )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 8, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  8   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  9   ***
#  *******************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  10   ***
#  ********************************

class Sphinx( base.Monster ):
    name = "Sphinx"    
    statline = { stats.STRENGTH: 19, stats.TOUGHNESS: 13, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 18, stats.PIETY: 19, stats.CHARISMA: 19, \
        stats.NATURAL_DEFENSE: 15 }
    SPRITENAME = "monster_default.png"
    FRAME = 37
    TEMPLATES = ()
    MOVE_POINTS = 12
    HABITAT = ( context.HAB_DESERT, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.DES_SOLAR,
     context.MTY_HUMANOID, context.MTY_LEADER, context.MTY_BOSS )
    ENC_LEVEL = 10
    TREASURE = treasuretype.High()
    ATTACK = items.Attack( (2,6,4), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( spells.lunarspells.DEATH_RAY, spells.airspells.DISPEL_MAGIC,
        spells.priestspells.SANCTUARY, spells.solarspells.REMOVE_CURSE,
        spells.solarspells.MASS_CURE )
    def init_monster( self ):
        self.levels.append( base.Terror( 8, self ) )


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



