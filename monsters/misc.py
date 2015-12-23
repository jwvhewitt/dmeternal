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
import abilities
import enchantments

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
     context.DES_LUNAR, context.MTY_BOSS,
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
      ,) ), com_tar=targetarea.SingleTarget(reach=4), shot_anim=animobs.PurpleVortex,
      ai_tar=invocations.TargetMobileEnemy(), mp_cost=3
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
     context.MTY_BEAST, context.MTY_BOSS )
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
    HABITAT = ( context.HAB_EVERY, context.HAB_TUNNELS, context.SET_EVERY,
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

class Gargoyle( base.Monster ):
    name = "Gargoyle"    
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 18, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 6, stats.PIETY: 11, stats.CHARISMA: 7,
        stats.RESIST_CRUSHING: 50, stats.RESIST_PIERCING: 50,
        stats.RESIST_SLASHING: 50, stats.PHYSICAL_ATTACK: 10, stats.NATURAL_DEFENSE: 5 }
    SPRITENAME = "monster_default.png"
    FRAME = 22
    TEMPLATES = (stats.EARTH,stats.ROCK)
    MOVE_POINTS = 16
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MTY_BOSS,
     context.MAP_DUNGEON, context.DES_EARTH )
    ENC_LEVEL = 5
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (2,4,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ()
    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  6   ***
#  *******************************

class Basilisk( base.Monster ):
    name = "Basilisk"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 15, stats.REFLEXES: 8, \
        stats.INTELLIGENCE: 2, stats.PIETY: 12, stats.CHARISMA: 11 }
    SPRITENAME = "monster_default.png"
    FRAME = 39
    TEMPLATES = (stats.REPTILE,)
    MOVE_POINTS = 8
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MTY_BEAST, context.MTY_BOSS )
    ENC_LEVEL = 6
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_PIERCING )
    TECHNIQUES = ( invocations.MPInvocation( "Death Gaze",
      effects.OpposedRoll( att_stat=stats.PIETY, att_modifier=-10, on_success = (
        effects.InstaKill( anim=animobs.CriticalHit )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=4), shot_anim=animobs.PurpleVortex, ai_tar=invocations.TargetEnemy(), mp_cost=6
    ), )
    def init_monster( self ):
        self.levels.append( base.Beast( 6, self ) )


class Griffin( base.Monster ):
    name = "Griffin"    
    statline = { stats.STRENGTH: 18, stats.TOUGHNESS: 16, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 5, stats.PIETY: 13, stats.CHARISMA: 8,
        stats.PHYSICAL_ATTACK: 5, stats.PHYSICAL_DEFENSE: 5, stats.MAGIC_DEFENSE: 5 }
    SPRITENAME = "monster_default.png"
    FRAME = 35
    TEMPLATES = ()
    MOVE_POINTS = 12
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_WILDERNESS, context.DES_AIR,
     context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 6
    TREASURE = None
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ()
    def init_monster( self ):
        self.levels.append( base.Beast( 7, self ) )

class Harpy( base.Monster ):
    name = "Harpy"    
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 7, stats.PIETY: 12, stats.CHARISMA: 17 }
    SPRITENAME = "monster_default.png"
    FRAME = 38
    TEMPLATES = ()
    MOVE_POINTS = 8
    VOICE = dialogue.voice.GREEK
    HABITAT = ( context.HAB_EVERY, context.HAB_CAVE, context.SET_EVERY,
     context.DES_LUNAR,
     context.MTY_HUMANOID, context.MTY_BOSS, context.GEN_CHAOS )
    ENC_LEVEL = 6
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (2,4,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = (invocations.MPInvocation( "Sleep Song",
        effects.TargetIsEnemy( anim=animobs.SonicHit, on_true = (
            effects.TargetIs( pat=effects.ANIMAL, on_true = (
                effects.OpposedRoll( att_modifier=0, on_success = (
                    effects.CauseSleep(),
                )),)
        ,), )), com_tar=targetarea.SelfCentered(radius=6,delay_from=-1), 
        ai_tar=invocations.TargetMobileEnemy(), mp_cost=8 ),
    )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 7, self ) )

class Owlbear( base.Monster ):
    name = "Owlbear"
    statline = { stats.STRENGTH: 21, stats.TOUGHNESS: 21, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 2, stats.PIETY: 12, stats.CHARISMA: 10 }
    SPRITENAME = "monster_default.png"
    FRAME = 27
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 6
    TREASURE = None
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ()
    def init_monster( self ):
        self.levels.append( base.Beast( 6, self ) )


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
    VOICE = dialogue.voice.GREEK
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

class Manticore( base.Monster ):
    name = "Manticore"    
    statline = { stats.STRENGTH: 20, stats.TOUGHNESS: 19, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 7, stats.PIETY: 12, stats.CHARISMA: 9 }
    SPRITENAME = "monster_default.png"
    FRAME = 26
    TEMPLATES = ()
    MOVE_POINTS = 12
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_WILDERNESS, context.MTY_BEAST, context.MTY_BOSS )
    ENC_LEVEL = 7
    COMBAT_AI = aibrain.ArcherAI()
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (2,4,0), element = stats.RESIST_PIERCING, extra_effect=abilities.POISON_ATTACK )
    TECHNIQUES = (invocations.MPInvocation( "Tail Spikes",
        effects.NoEffect( children=(
          effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, att_modifier=5, on_success = (
            effects.HealthDamage( (1,8,0), stat_bonus=stats.STRENGTH, element=stats.RESIST_PIERCING, anim=animobs.RedBoom ),
          ), on_failure = (
            effects.NoEffect( anim=animobs.SmallBoom ),
          )),
          effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, att_modifier=5, on_success = (
            effects.HealthDamage( (1,8,0), stat_bonus=stats.STRENGTH, element=stats.RESIST_PIERCING, anim=animobs.RedBoom ),
          ), on_failure = (
            effects.NoEffect( anim=animobs.SmallBoom ),
          ) ),
          effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, att_modifier=5, on_success = (
            effects.HealthDamage( (1,8,0), stat_bonus=stats.STRENGTH, element=stats.RESIST_PIERCING, anim=animobs.RedBoom ),
          ), on_failure = (
            effects.NoEffect( anim=animobs.SmallBoom ),
          ) ),
          effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, att_modifier=5, on_success = (
            effects.HealthDamage( (1,8,0), stat_bonus=stats.STRENGTH, element=stats.RESIST_PIERCING, anim=animobs.RedBoom ),
          ), on_failure = (
            effects.NoEffect( anim=animobs.SmallBoom ),
          ) ),
        ),), mp_cost=10, com_tar=targetarea.SingleTarget(reach=9), shot_anim=animobs.GoldStone, ai_tar=invocations.TargetEnemy()
        ),
    )
    def init_monster( self ):
        self.levels.append( base.Beast( 6, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  8   ***
#  *******************************

# Megaraptor

class Wyvern( base.Monster ):
    name = "Wyvern"
    statline = { stats.STRENGTH: 19, stats.TOUGHNESS: 15, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 6, stats.PIETY: 12, stats.CHARISMA: 9 }
    SPRITENAME = "monster_default.png"
    FRAME = 44
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_BEAST, context.GEN_DRAGON )
    ENC_LEVEL = 8
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_PIERCING,
        extra_effect=abilities.POISON_ATTACK_1d8 )
    TECHNIQUES = ()
    def init_monster( self ):
        self.levels.append( base.Terror( 8, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  9   ***
#  *******************************


class Chimera( base.Monster ):
    name = "Chimera"
    # This is based on the version from the Pathfinder SRD rather than the
    # regular SRD; the only difference is the beefed-up breath weapon.
    statline = { stats.STRENGTH: 19, stats.TOUGHNESS: 17, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 4, stats.PIETY: 13, stats.CHARISMA: 10,
        stats.AWARENESS: 50 }
    SPRITENAME = "monster_by_Joe.png"
    FRAME = 0
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = dialogue.voice.GREEK
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.DES_FIRE,
     context.MTY_BEAST, context.GEN_CHAOS, context.MTY_BOSS )
    ENC_LEVEL = 9
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_PIERCING )
    TECHNIQUES = ( invocations.MPInvocation( "Fire Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (6,8,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
      ,), on_failure = (
        effects.HealthDamage( (3,8,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
      ,) ), com_tar=targetarea.Cone(reach=4), ai_tar=invocations.TargetEnemy(), mp_cost=16
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 9, self ) )

class Medusa( base.Monster ):
    name = "Medusa"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 12, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 12, stats.PIETY: 13, stats.CHARISMA: 15 }
    SPRITENAME = "monster_default.png"
    FRAME = 30
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.GREEK
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MTY_HUMANOID )
    ENC_LEVEL = 9
    COMBAT_AI = aibrain.ArcherAI(approach_allies=0,technique_chance=75)
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING, extra_effect=abilities.POISON_ATTACK_2d6 )
    TECHNIQUES = ( invocations.MPInvocation( "Death Gaze",
      effects.OpposedRoll( att_stat=stats.PIETY, att_modifier=-10, on_success = (
        effects.InstaKill( anim=animobs.CriticalHit )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=6), shot_anim=animobs.PurpleVortex, ai_tar=invocations.TargetEnemy(), mp_cost=9
    ), abilities.LONGBOW )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 6, self ) )

class Umbull( base.Monster ):
    name = "Umbull"    
    statline = { stats.STRENGTH: 23, stats.TOUGHNESS: 19, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 9, stats.PIETY: 11, stats.CHARISMA: 13 }
    SPRITENAME = "monster_default.png"
    FRAME = 4
    TEMPLATES = ()
    MOVE_POINTS = 8
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY,
     context.MAP_DUNGEON, context.DES_EARTH )
    ENC_LEVEL = 9
    COMBAT_AI = aibrain.BruiserAI()
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (3,6,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = (invocations.Invocation( "Freezing Gaze",
        effects.OpposedRoll( att_modifier=20, on_success = (
            effects.Paralyze( max_duration = 6 )
        ,), on_failure =(
            effects.NoEffect( anim=animobs.SmallBoom )
        ,) ), com_tar=targetarea.SingleTarget(), shot_anim=animobs.PurpleVortex,
        ai_tar=invocations.TargetMobileEnemy() ),
    )
    def init_monster( self ):
        self.levels.append( base.Defender( 9, self ) )


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
    VOICE = dialogue.voice.GREEK
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

class Behir( base.Monster ):
    name = "Behir"    
    statline = { stats.STRENGTH: 26, stats.TOUGHNESS: 21, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 7, stats.PIETY: 14, stats.CHARISMA: 12, \
        stats.RESIST_LIGHTNING: 150, stats.AWARENESS: 50, stats.CRITICAL_HIT: 10 }
    SPRITENAME = "monster_by_Joe.png"
    FRAME = 5
    TEMPLATES = ()
    MOVE_POINTS = 12
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.DES_AIR,
     context.MTY_BOSS )
    ENC_LEVEL = 10
    TREASURE = treasuretype.Swallowed(scale=1,swag_chance=20)
    ATTACK = items.Attack( (2,4,0), element = stats.RESIST_PIERCING )
    TECHNIQUES = ( invocations.MPInvocation( "Lightning Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (7,6,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,), on_failure = (
        effects.HealthDamage( (3,7,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,) ), com_tar=targetarea.Line(reach=5), ai_tar=invocations.TargetEnemy(), mp_cost=30
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 9, self ) )

#  ********************************
#  ***   ENCOUNTER  LEVEL  11   ***
#  ********************************

class Hydra( base.Monster ):
    name = "Hydra"    
    statline = { stats.STRENGTH: 21, stats.TOUGHNESS: 20, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 3, stats.PIETY: 10, stats.CHARISMA: 9,
        stats.PHYSICAL_ATTACK: 20 }
    SPRITENAME = "monster_default.png"
    FRAME = 3
    TEMPLATES = (stats.REPTILE,stats.EARTH,)
    MOVE_POINTS = 8
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_EARTH, context.MTY_BOSS )
    ENC_LEVEL = 11
    VOICE = dialogue.voice.GREEK
    COMBAT_AI = aibrain.BruiserAI()
    TREASURE = treasuretype.Low()
    ATTACK = items.Attack( (2,10,0), element = stats.RESIST_PIERCING )
    TECHNIQUES = ( invocations.MPInvocation( "Poison Breath",
      effects.OpposedRoll( def_stat=stats.TOUGHNESS, on_success = (
        effects.HealthDamage( (3,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
        effects.TargetIs( effects.ALIVE, on_true=( effects.OpposedRoll( att_stat=None, def_stat=stats.TOUGHNESS, on_success = (
            effects.Enchant( enchantments.PoisonClassic )
        ,) ), ))
      ), on_failure = (
        effects.HealthDamage( (2,6,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud )
      ,) ), com_tar=targetarea.Blast(radius=2), ai_tar=invocations.TargetEnemy(min_distance=3), mp_cost=20, shot_anim=animobs.GreenComet
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 10, self ) )
        self.condition.append( enchantments.PermaMegaRegeneration() )


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

#  ********************************
#  ***   ENCOUNTER  LEVEL  21   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  22   ***
#  ********************************

class Kaiju( base.Monster ):
    name = "Kaiju"    
    statline = { stats.STRENGTH: 45, stats.TOUGHNESS: 35, stats.REFLEXES: 16, \
        stats.INTELLIGENCE: 3, stats.PIETY: 14, stats.CHARISMA: 14, stats.RESIST_ATOMIC: 50,
        stats.RESIST_FIRE: 200, stats.RESIST_POISON: 200, stats.RESIST_LUNAR: 200 }
    SPRITENAME = "monster_default.png"
    FRAME = 14
    TEMPLATES = ()
    MOVE_POINTS = 8
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_BEAST )
    ENC_LEVEL = 22
    VOICE = dialogue.voice.DRACONIAN
    COMBAT_AI = aibrain.BruiserAI()
    TREASURE = None
    ATTACK = items.Attack( (4,8,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( invocations.MPInvocation( "Atomic Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (10,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_ATOMIC, anim=animobs.Nuclear )
      ,), on_failure = (
        effects.HealthDamage( (3,10,0), stat_bonus=None, element=stats.RESIST_ATOMIC, anim=animobs.Nuclear )
      ,) ), com_tar=targetarea.Cone(reach=8), ai_tar=invocations.TargetEnemy(), mp_cost=60
    ), )
    def init_monster( self ):
        self.levels.append( base.Beast( 48, self ) )
        self.condition.append( enchantments.PermaMegaRegeneration() )



