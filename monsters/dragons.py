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
import random
import enchantments
import treasuretype
import abilities

# The order of dragons...
# 1 - Cave (Poison/Paralysis, more cc than bw) [BRASS]
#   - Swamp (Acid)                    [WHITE]
# 2 - Sky (Lightning)                 [COPPER]
#   - Ice (Ice)                       [BLACK]
# 3 - Forest (Poison)                 [GREEN]
#   - Sea (Steam, aka Fire)           [BRONZE]
# 4 - Sun (Fire, Lightning, Special)  [SILVER]
#   - Night (Ice, Acid, Special)      [BLUE]
# 5 - Fire (Fire, Atomic)             [RED]
#   - Chromatic (Fire, Acid, Lightning, Poison, and Ice) [GOLD]

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

class YoungCaveDragon( base.Monster ):
    name = "Young Cave Dragon"
    statline = { stats.STRENGTH: 11, stats.TOUGHNESS: 13, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 11, stats.CHARISMA: 10,
        stats.RESIST_POISON: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 2
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.HAB_CAVE,
     context.MAP_DUNGEON, context.MTY_DRAGON, context.MTY_BOSS,
     context.DES_EARTH, context.GEN_DRAGON )
    ENC_LEVEL = 4
    COMBAT_AI = aibrain.BruiserAI()
    TREASURE = treasuretype.DragonHoard()
    ATTACK = items.Attack( (3,4,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Toxic Breath",
        effects.OpposedRoll( def_stat=stats.TOUGHNESS, anim=animobs.PoisonCloud, on_success = (
            effects.Paralyze( max_duration = 3 )
        ,) ), com_tar=targetarea.Cone(reach=4), ai_tar=invocations.TargetEnemy(), mp_cost=4
      ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 4, self ) )

class YoungSwampDragon( base.Monster ):
    name = "Young Swamp Dragon"
    statline = { stats.STRENGTH: 11, stats.TOUGHNESS: 13, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 6, stats.PIETY: 11, stats.CHARISMA: 6,
        stats.RESIST_ACID: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 0
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.MTY_DRAGON,
     context.MTY_BOSS,
     context.DES_EARTH, context.DES_WATER, context.GEN_DRAGON )
    ENC_LEVEL = 4
    TREASURE = treasuretype.DragonHoard()
    ATTACK = items.Attack( (2,4,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Acid Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (2,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,) ), com_tar=targetarea.Line(reach=4), ai_tar=invocations.TargetEnemy(), mp_cost=5
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 4, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  5   ***
#  *******************************

class YoungSkyDragon( base.Monster ):
    name = "Young Sky Dragon"
    statline = { stats.STRENGTH: 11, stats.TOUGHNESS: 13, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 12, stats.PIETY: 13, stats.CHARISMA: 12,
        stats.RESIST_LIGHTNING: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 8
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.MTY_DRAGON,
     context.MAP_WILDERNESS,
     context.DES_AIR, context.GEN_DRAGON, context.MTY_BOSS )
    ENC_LEVEL = 5
    COMBAT_AI = aibrain.ArcherAI(approach_allies=0)
    TREASURE = treasuretype.DragonHoard()
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Lightning Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (2,4,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,), on_failure = (
        effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,) ), com_tar=targetarea.Line(reach=5), ai_tar=invocations.TargetEnemy(), mp_cost=6
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 5, self ) )

class YoungIceDragon( base.Monster ):
    name = "Young Ice Dragon"
    statline = { stats.STRENGTH: 11, stats.TOUGHNESS: 13, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 8, stats.PIETY: 11, stats.CHARISMA: 8,
        stats.RESIST_COLD: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 7
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.MTY_DRAGON,
     context.DES_ICE, context.GEN_DRAGON, context.MTY_BOSS )
    ENC_LEVEL = 5
    TREASURE = treasuretype.DragonHoard()
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Frost Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (2,4,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
      ,), on_failure = (
        effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
      ,) ), com_tar=targetarea.Cone(reach=4), ai_tar=invocations.TargetEnemy(), mp_cost=8
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 5, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  6   ***
#  *******************************

class YoungForestDragon( base.Monster ):
    name = "Young Forest Dragon"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 16, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 12,
        stats.RESIST_POISON: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 4
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.HAB_FOREST, context.MAP_WILDERNESS, context.MTY_DRAGON,
     context.GEN_NATURE, context.GEN_DRAGON, context.MTY_BOSS )
    ENC_LEVEL = 6
    TREASURE = treasuretype.DragonHoard()
    ATTACK = items.Attack( (1,12,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Poison Breath",
      effects.OpposedRoll( def_stat=stats.TOUGHNESS, on_success = (
        effects.HealthDamage( (3,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_POISON, anim=animobs.PoisonCloud )
      ,), on_failure = (
        effects.HealthDamage( (1,10,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud )
      ,) ), com_tar=targetarea.Blast(radius=1), ai_tar=invocations.TargetEnemy(), mp_cost=9, shot_anim=animobs.GreenComet
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 7, self ) )

class YoungSeaDragon( base.Monster ):
    name = "Young Sea Dragon"
    statline = { stats.STRENGTH: 17, stats.TOUGHNESS: 15, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 14, stats.CHARISMA: 12,
        stats.RESIST_WATER: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 1
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_WATER, context.MTY_DRAGON,
     context.GEN_DRAGON, context.MTY_BOSS )
    ENC_LEVEL = 6
    TREASURE = treasuretype.DragonHoard()
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Steam Breath",
      effects.OpposedRoll( def_stat=stats.TOUGHNESS, on_success = (
        effects.HealthDamage( (2,10,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_FIRE, anim=animobs.Steam )
      ,), on_failure = (
        effects.HealthDamage( (1,10,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.Steam )
      ,) ), com_tar=targetarea.Cone(reach=5), ai_tar=invocations.TargetEnemy(), mp_cost=10
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 7, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  7   ***
#  *******************************

class YoungSunDragon( base.Monster ):
    name = "Young Sun Dragon"
    statline = { stats.STRENGTH: 17, stats.TOUGHNESS: 15, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 15, stats.PIETY: 15, stats.CHARISMA: 14,
        stats.RESIST_FIRE: 100, stats.RESIST_LIGHTNING: 100, stats.RESIST_SOLAR: 50 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 3
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_SOLAR, context.MTY_DRAGON,
     context.GEN_DRAGON, context.MTY_BOSS )
    ENC_LEVEL = 7
    TREASURE = treasuretype.DragonHoard()
    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Fire Breath",
      effects.OpposedRoll( def_stat=stats.TOUGHNESS, on_success = (
        effects.HealthDamage( (2,10,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_FIRE, anim=animobs.DragonFire )
      ,), on_failure = (
        effects.HealthDamage( (1,10,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.DragonFire )
      ,) ), com_tar=targetarea.Cone(reach=5), ai_tar=invocations.TargetEnemy(), mp_cost=12
    ), invocations.MPInvocation( "Lightning Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (3,8,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_LIGHTNING, anim=animobs.Spark ),
      ), on_failure = (
        effects.HealthDamage( (2,6,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,) ), com_tar=targetarea.Line(reach=8), ai_tar=invocations.TargetEnemy(), mp_cost=10
    ),
    )
    def init_monster( self ):
        self.levels.append( base.Terror( 9, self ) )

class YoungMoonDragon( base.Monster ):
    name = "Young Moon Dragon"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 16, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 16, stats.PIETY: 14, stats.CHARISMA: 14,
        stats.RESIST_COLD: 100, stats.RESIST_ACID: 100, stats.RESIST_LUNAR: 50 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 9
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_LUNAR, context.MTY_DRAGON,
     context.GEN_DRAGON, context.MTY_BOSS )
    ENC_LEVEL = 7
    TREASURE = treasuretype.DragonHoard()
    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Cold Breath",
      effects.OpposedRoll( def_stat=stats.TOUGHNESS, on_success = (
        effects.HealthDamage( (2,10,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
      ,), on_failure = (
        effects.HealthDamage( (1,10,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
      ,) ), com_tar=targetarea.Cone(reach=5), ai_tar=invocations.TargetEnemy(), mp_cost=12
    ), invocations.MPInvocation( "Acid Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (3,8,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_ACID, anim=animobs.GreenCloud ),
      ), on_failure = (
        effects.HealthDamage( (2,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenCloud )
      ,) ), com_tar=targetarea.Line(reach=8), ai_tar=invocations.TargetEnemy(), mp_cost=10
    ),
    )
    def init_monster( self ):
        self.levels.append( base.Terror( 9, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  8   ***
#  *******************************

class YoungFireDragon( base.Monster ):
    name = "Young Fire Dragon"
    statline = { stats.STRENGTH: 17, stats.TOUGHNESS: 15, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 13, stats.PIETY: 15, stats.CHARISMA: 15,
        stats.RESIST_FIRE: 100, stats.RESIST_LIGHTNING: 100, stats.RESIST_SOLAR: 50 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 3
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_SOLAR, context.MTY_DRAGON,
     context.GEN_DRAGON, context.MTY_BOSS )
    ENC_LEVEL = 8
    TREASURE = treasuretype.DragonHoard()
    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Fire Breath",
      effects.OpposedRoll( def_stat=stats.TOUGHNESS, on_success = (
        effects.HealthDamage( (4,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_FIRE, anim=animobs.DragonFire )
      ,), on_failure = (
        effects.HealthDamage( (2,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.DragonFire )
      ,) ), com_tar=targetarea.Cone(reach=5), ai_tar=invocations.TargetEnemy(), mp_cost=14
    ),)
    def init_monster( self ):
        self.levels.append( base.Terror( 10, self ) )


class CaveDragon( base.Monster ):
    name = "Cave Dragon"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 15, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 12, stats.PIETY: 13, stats.CHARISMA: 12,
        stats.PHYSICAL_ATTACK: 5, stats.RESIST_POISON: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 12
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.HAB_CAVE,
     context.MAP_DUNGEON, context.MTY_BOSS, context.MTY_LEADER, context.MTY_DRAGON,
     context.DES_EARTH, context.GEN_DRAGON )
    ENC_LEVEL = 8
    COMBAT_AI = aibrain.BruiserAI()
    TREASURE = treasuretype.DragonHoard()
    LONER = True
    COMPANIONS = ( YoungCaveDragon, )
    ATTACK = items.Attack( (3,8,0), element = stats.RESIST_SLASHING,
        extra_effect=abilities.POISON_ATTACK )
    TECHNIQUES = ( invocations.MPInvocation( "Toxic Breath",
        effects.OpposedRoll( def_stat=stats.TOUGHNESS, anim=None, on_success = (
            effects.HealthDamage( (2,8,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
            effects.Paralyze( max_duration = 3 ),
            effects.Enchant( enchantments.PoisonClassic, anim=animobs.DeathSparkle ),
        ), on_failure = (
            effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
        ) ), com_tar=targetarea.Cone(reach=6), ai_tar=invocations.TargetEnemy(), mp_cost=8
      ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 10, self ) )

class SwampDragon( base.Monster ):
    name = "Swamp Dragon"
    statline = { stats.STRENGTH: 17, stats.TOUGHNESS: 15, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 8, stats.PIETY: 11, stats.CHARISMA: 8,
        stats.RESIST_ACID: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 10
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
      context.MTY_BOSS, context.MTY_LEADER, context.MTY_DRAGON,
     context.DES_EARTH, context.DES_WATER, context.GEN_DRAGON )
    ENC_LEVEL = 8
    TREASURE = treasuretype.DragonHoard()
    LONER = True
    COMPANIONS = ( YoungSwampDragon, )
    ATTACK = items.Attack( (3,6,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Acid Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (4,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,), on_failure = (
        effects.HealthDamage( (2,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,) ), com_tar=targetarea.Line(reach=6), ai_tar=invocations.TargetEnemy(), mp_cost=14
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 12, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  9   ***
#  *******************************

class SkyDragon( base.Monster ):
    name = "Sky Dragon"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 15, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 14, stats.PIETY: 15, stats.CHARISMA: 14,
        stats.RESIST_LIGHTNING: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 18
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.HAB_DESERT, context.SET_EVERY,
     context.MAP_WILDERNESS, context.MTY_BOSS, context.MTY_DRAGON,
     context.DES_AIR, context.GEN_DRAGON )
    ENC_LEVEL = 9
    COMBAT_AI = aibrain.ArcherAI(approach_allies=0)
    TREASURE = treasuretype.DragonHoard()
    LONER = True
    COMPANIONS = ( YoungSkyDragon, )
    ATTACK = items.Attack( (2,10,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Lightning Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (6,4,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,), on_failure = (
        effects.HealthDamage( (2,6,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,) ), com_tar=targetarea.Line(reach=7), ai_tar=invocations.TargetEnemy(), mp_cost=16
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 11, self ) )

class IceDragon( base.Monster ):
    name = "Ice Dragon"
    statline = { stats.STRENGTH: 17, stats.TOUGHNESS: 15, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 11, stats.CHARISMA: 10,
        stats.RESIST_COLD: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 17
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.MTY_DRAGON,
     context.DES_ICE, context.GEN_DRAGON, context.MTY_BOSS )
    ENC_LEVEL = 9
    TREASURE = treasuretype.DragonHoard()
    ATTACK = items.Attack( (3,8,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Frost Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (4,8,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
      ,), on_failure = (
        effects.HealthDamage( (2,8,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
      ,) ), com_tar=targetarea.Cone(reach=5), ai_tar=invocations.TargetEnemy(), mp_cost=16
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 13, self ) )



#  ********************************
#  ***   ENCOUNTER  LEVEL  10   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  11   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  12   ***
#  ********************************

class OldCaveDragon( base.Monster ):
    name = "Old Cave Dragon"
    statline = { stats.STRENGTH: 19, stats.TOUGHNESS: 17, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 14, stats.PIETY: 15, stats.CHARISMA: 14,
        stats.PHYSICAL_ATTACK: 5, stats.RESIST_POISON: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 22
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.HAB_CAVE,
     context.MAP_DUNGEON, context.MTY_LEADER, context.MTY_DRAGON, context.MTY_BOSS,
     context.DES_EARTH, context.GEN_DRAGON )
    ENC_LEVEL = 12
    COMBAT_AI = aibrain.BruiserAI()
    TREASURE = treasuretype.DragonHoard()
    LONER = True
    COMPANIONS = ( CaveDragon, )
    ATTACK = items.Attack( (4,8,0), element = stats.RESIST_SLASHING,
     extra_effect=abilities.POISON_ATTACK_2d6 )
    TECHNIQUES = ( invocations.MPInvocation( "Toxic Breath",
        effects.OpposedRoll( def_stat=stats.TOUGHNESS, anim=None, on_success = (
            effects.HealthDamage( (5,6,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
            effects.Paralyze( max_duration = 3 ),
            effects.Enchant( enchantments.PoisonClassic, anim=animobs.DeathSparkle ),
        ), on_failure = (
            effects.HealthDamage( (3,5,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
        ) ), com_tar=targetarea.Cone(reach=7), ai_tar=invocations.TargetEnemy(), mp_cost=22
      ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 16, self ) )

class OldSwampDragon( base.Monster ):
    name = "Old Swamp Dragon"
    statline = { stats.STRENGTH: 23, stats.TOUGHNESS: 19, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 11, stats.CHARISMA: 12,
        stats.RESIST_ACID: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 20
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
      context.MTY_LEADER, context.MTY_DRAGON, context.MTY_BOSS,
     context.DES_EARTH, context.DES_WATER, context.GEN_DRAGON )
    ENC_LEVEL = 12
    TREASURE = treasuretype.DragonHoard()
    LONER = True
    COMPANIONS = ( SwampDragon, )
    ATTACK = items.Attack( (3,10,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Acid Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (6,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,), on_failure = (
        effects.HealthDamage( (3,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,) ), com_tar=targetarea.Line(reach=8), ai_tar=invocations.TargetEnemy(), mp_cost=22
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 18, self ) )


#  ********************************
#  ***   ENCOUNTER  LEVEL  13   ***
#  ********************************

class OldSkyDragon( base.Monster ):
    name = "Old Sky Dragon"
    statline = { stats.STRENGTH: 19, stats.TOUGHNESS: 17, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 16, stats.PIETY: 17, stats.CHARISMA: 16,
        stats.RESIST_LIGHTNING: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 28
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.HAB_DESERT, context.SET_EVERY,
     context.MAP_WILDERNESS, context.MTY_BOSS, context.MTY_DRAGON,
     context.DES_AIR, context.GEN_DRAGON )
    ENC_LEVEL = 13
    COMBAT_AI = aibrain.ArcherAI(approach_allies=0)
    TREASURE = treasuretype.DragonHoard()
    LONER = True
    COMPANIONS = ( YoungSkyDragon, )
    ATTACK = items.Attack( (2,12,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Lightning Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (10,4,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,), on_failure = (
        effects.HealthDamage( (5,4,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,) ), com_tar=targetarea.Line(reach=9), ai_tar=invocations.TargetEnemy(), mp_cost=24
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 17, self ) )

class OldIceDragon( base.Monster ):
    name = "Old Ice Dragon"
    statline = { stats.STRENGTH: 23, stats.TOUGHNESS: 19, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 12, stats.PIETY: 13, stats.CHARISMA: 12,
        stats.RESIST_COLD: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 27
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.MTY_DRAGON,
     context.DES_ICE, context.GEN_DRAGON, context.MTY_BOSS )
    ENC_LEVEL = 13
    TREASURE = treasuretype.DragonHoard()
    ATTACK = items.Attack( (3,10,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Frost Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (6,8,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
      ,), on_failure = (
        effects.HealthDamage( (3,8,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
      ,) ), com_tar=targetarea.Cone(reach=6), ai_tar=invocations.TargetEnemy(), mp_cost=24
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 19, self ) )


#  ********************************
#  ***   ENCOUNTER  LEVEL  14   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  15   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  16   ***
#  ********************************

class AncientCaveDragon( base.Monster ):
    name = "Ancient Cave Dragon"
    statline = { stats.STRENGTH: 27, stats.TOUGHNESS: 21, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 16, stats.PIETY: 17, stats.CHARISMA: 16,
        stats.PHYSICAL_ATTACK: 10, stats.RESIST_POISON: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 32
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.HAB_CAVE,
     context.MAP_DUNGEON, context.MTY_LEADER, context.MTY_DRAGON, context.MTY_BOSS,
     context.DES_EARTH, context.GEN_DRAGON )
    ENC_LEVEL = 16
    COMBAT_AI = aibrain.BruiserAI()
    TREASURE = treasuretype.DragonHoard()
    LONER = True
    COMPANIONS = ( OldCaveDragon, )
    ATTACK = items.Attack( (5,8,0), element = stats.RESIST_SLASHING,
     extra_effect=abilities.POISON_ATTACK_2d6)
    TECHNIQUES = ( invocations.MPInvocation( "Toxic Breath",
        effects.OpposedRoll( def_stat=stats.TOUGHNESS, anim=None, on_success = (
            effects.HealthDamage( (7,6,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
            effects.Paralyze( max_duration = 3 ),
            effects.Enchant( enchantments.PoisonClassic, anim=animobs.DeathSparkle ),
        ), on_failure = (
            effects.HealthDamage( (3,7,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
        ) ), com_tar=targetarea.Cone(reach=7), ai_tar=invocations.TargetEnemy(), mp_cost=30
      ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 22, self ) )

class AncientSwampDragon( base.Monster ):
    name = "Ancient Swamp Dragon"
    statline = { stats.STRENGTH: 29, stats.TOUGHNESS: 21, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 12, stats.PIETY: 13, stats.CHARISMA: 12,
        stats.RESIST_ACID: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 30
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
      context.MTY_LEADER, context.MTY_DRAGON, context.MTY_BOSS,
     context.DES_EARTH, context.DES_WATER, context.GEN_DRAGON )
    ENC_LEVEL = 16
    TREASURE = treasuretype.DragonHoard()
    LONER = True
    COMPANIONS = ( OldSwampDragon, )
    ATTACK = items.Attack( (3,12,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Acid Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (8,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,), on_failure = (
        effects.HealthDamage( (4,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,) ), com_tar=targetarea.Line(reach=10), ai_tar=invocations.TargetEnemy(), mp_cost=20
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 24, self ) )


#  ********************************
#  ***   ENCOUNTER  LEVEL  17   ***
#  ********************************

class AncientSkyDragon( base.Monster ):
    name = "Ancient Sky Dragon"
    statline = { stats.STRENGTH: 27, stats.TOUGHNESS: 21, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 18, stats.PIETY: 19, stats.CHARISMA: 18,
        stats.RESIST_LIGHTNING: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 38
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.HAB_DESERT, context.SET_EVERY,
     context.MAP_WILDERNESS, context.MTY_BOSS, context.MTY_DRAGON,
     context.DES_AIR, context.GEN_DRAGON )
    ENC_LEVEL = 17
    COMBAT_AI = aibrain.ArcherAI(approach_allies=0)
    TREASURE = treasuretype.DragonHoard()
    LONER = True
    COMPANIONS = ( YoungSkyDragon, )
    ATTACK = items.Attack( (4,8,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Lightning Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (14,4,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,), on_failure = (
        effects.HealthDamage( (7,4,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,) ), com_tar=targetarea.Line(reach=9), ai_tar=invocations.TargetEnemy(), mp_cost=32
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 23, self ) )

class AncientIceDragon( base.Monster ):
    name = "Ancient Ice Dragon"
    statline = { stats.STRENGTH: 29, stats.TOUGHNESS: 21, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 14, stats.PIETY: 15, stats.CHARISMA: 14,
        stats.RESIST_COLD: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 37
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.MTY_DRAGON,
     context.DES_ICE, context.GEN_DRAGON, context.MTY_BOSS )
    ENC_LEVEL = 17
    TREASURE = treasuretype.DragonHoard()
    ATTACK = items.Attack( (4,10,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Frost Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (8,8,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
      ,), on_failure = (
        effects.HealthDamage( (4,8,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
      ,) ), com_tar=targetarea.Cone(reach=7), ai_tar=invocations.TargetEnemy(), mp_cost=32
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 25, self ) )


#  ********************************
#  ***   ENCOUNTER  LEVEL  18   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  19   ***
#  ********************************


#  ********************************
#  ***   ENCOUNTER  LEVEL  20   ***
#  ********************************

class GreatCaveWyrm( base.Monster ):
    name = "Great Cave Wyrm"
    statline = { stats.STRENGTH: 27, stats.TOUGHNESS: 21, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 16, stats.PIETY: 17, stats.CHARISMA: 16,
        stats.PHYSICAL_ATTACK: 20, stats.RESIST_POISON: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 42
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.HAB_CAVE,
     context.MAP_DUNGEON, context.MTY_LEADER, context.MTY_DRAGON, context.MTY_BOSS,
     context.DES_EARTH, context.GEN_DRAGON )
    ENC_LEVEL = 20
    COMBAT_AI = aibrain.BruiserAI()
    TREASURE = treasuretype.DragonHoard()
    LONER = True
    COMPANIONS = ( OldCaveDragon, AncientCaveDragon, )
    ATTACK = items.Attack( (7,8,0), element = stats.RESIST_SLASHING,
     extra_effect=abilities.POISON_ATTACK_2d6)
    TECHNIQUES = ( invocations.MPInvocation( "Toxic Breath",
        effects.OpposedRoll( def_stat=stats.TOUGHNESS, anim=None, on_success = (
            effects.HealthDamage( (9,6,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
            effects.Paralyze( max_duration = 3 ),
            effects.Enchant( enchantments.PoisonClassic, anim=animobs.DeathSparkle ),
        ), on_failure = (
            effects.HealthDamage( (3,9,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
        ) ), com_tar=targetarea.Cone(reach=8), ai_tar=invocations.TargetEnemy(), mp_cost=38
      ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 28, self ) )

class GreatSwampWyrm( base.Monster ):
    name = "Great Swamp Wyrm"
    statline = { stats.STRENGTH: 33, stats.TOUGHNESS: 23, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 14, stats.PIETY: 15, stats.CHARISMA: 14,
        stats.RESIST_ACID: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 40
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
      context.MTY_LEADER, context.MTY_DRAGON, context.MTY_BOSS,
     context.DES_EARTH, context.DES_WATER, context.GEN_DRAGON )
    ENC_LEVEL = 20
    TREASURE = treasuretype.DragonHoard()
    LONER = True
    COMPANIONS = ( OldSwampDragon, )
    ATTACK = items.Attack( (5,10,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Acid Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (10,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,), on_failure = (
        effects.HealthDamage( (5,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,) ), com_tar=targetarea.Line(reach=10), ai_tar=invocations.TargetEnemy(), mp_cost=38
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 30, self ) )

#  ********************************
#  ***   ENCOUNTER  LEVEL  21   ***
#  ********************************

class GreatSkyWyrm( base.Monster ):
    name = "Great Sky Wyrm"
    statline = { stats.STRENGTH: 29, stats.TOUGHNESS: 22, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 18, stats.PIETY: 19, stats.CHARISMA: 18,
        stats.RESIST_LIGHTNING: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 48
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.HAB_DESERT, context.SET_EVERY,
     context.MAP_WILDERNESS, context.MTY_BOSS, context.MTY_DRAGON,
     context.DES_AIR, context.GEN_DRAGON )
    ENC_LEVEL = 21
    COMBAT_AI = aibrain.ArcherAI(approach_allies=0)
    TREASURE = treasuretype.DragonHoard()
    LONER = True
    COMPANIONS = ( YoungSkyDragon, )
    ATTACK = items.Attack( (5,8,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Lightning Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (16,4,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,), on_failure = (
        effects.HealthDamage( (8,4,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,) ), com_tar=targetarea.Line(reach=10), ai_tar=invocations.TargetEnemy(), mp_cost=40
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 26, self ) )

class GreatIceWyrm( base.Monster ):
    name = "Great Ice Wyrm"
    statline = { stats.STRENGTH: 33, stats.TOUGHNESS: 23, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 16, stats.PIETY: 17, stats.CHARISMA: 16,
        stats.RESIST_COLD: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 47
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.MTY_DRAGON,
     context.DES_ICE, context.GEN_DRAGON, context.MTY_BOSS )
    ENC_LEVEL = 21
    TREASURE = treasuretype.DragonHoard()
    ATTACK = items.Attack( (5,10,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Frost Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (10,8,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
      ,), on_failure = (
        effects.HealthDamage( (5,8,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
      ,) ), com_tar=targetarea.Cone(reach=8), ai_tar=invocations.TargetEnemy(), mp_cost=40
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 31, self ) )



