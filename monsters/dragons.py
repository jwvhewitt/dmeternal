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
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 15, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 9, stats.PIETY: 12, stats.CHARISMA: 10,
        stats.RESIST_POISON: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 2
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.DRACONIAN
    GP_VALUE = 200
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.HAB_CAVE,
     context.MAP_DUNGEON,
     context.DES_EARTH, context.GEN_DRAGON )
    ENC_LEVEL = 4
    ATTACK = items.Attack( (3,4,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Toxic Breath",
        effects.OpposedRoll( def_stat=stats.TOUGHNESS, anim=animobs.PoisonCloud, on_success = (
            effects.Paralyze( max_duration = 3 )
        ,) ), com_tar=targetarea.Cone(reach=4), ai_tar=invocations.vs_enemy, mp_cost=3
      ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 4, self ) )

class YoungSwampDragon( base.Monster ):
    name = "Young Swamp Dragon"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 16, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 10, stats.PIETY: 12, stats.CHARISMA: 10,
        stats.RESIST_ACID: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 0
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.DRACONIAN
    GP_VALUE = 200
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_EARTH, context.DES_WATER, context.GEN_DRAGON )
    ENC_LEVEL = 4
    ATTACK = items.Attack( (2,4,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Acid Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (2,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,) ), com_tar=targetarea.Line(reach=5), ai_tar=invocations.vs_enemy, mp_cost=3
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 4, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  5   ***
#  *******************************

class YoungSkyDragon( base.Monster ):
    name = "Young Sky Dragon"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 15, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 12, stats.PIETY: 10, stats.CHARISMA: 12,
        stats.RESIST_LIGHTNING: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 8
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.DRACONIAN
    GP_VALUE = 250
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_AIR, context.GEN_DRAGON )
    ENC_LEVEL = 5
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Lightning Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (2,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,) ), com_tar=targetarea.Line(reach=6), ai_tar=invocations.vs_enemy, mp_cost=3
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
    GP_VALUE = 300
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.HAB_FOREST, context.MAP_WILDERNESS,
     context.GEN_NATURE, context.GEN_DRAGON )
    ENC_LEVEL = 6
    ATTACK = items.Attack( (1,12,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Poison Breath",
      effects.OpposedRoll( def_stat=stats.TOUGHNESS, on_success = (
        effects.HealthDamage( (2,8,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_POISON, anim=animobs.PoisonCloud )
      ,), on_failure = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud )
      ,) ), com_tar=targetarea.Blast(radius=1), ai_tar=invocations.vs_enemy, mp_cost=4
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 6, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  7   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  8   ***
#  *******************************

class CaveDragon( base.Monster ):
    name = "Cave Dragon"
    statline = { stats.STRENGTH: 19, stats.TOUGHNESS: 18, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 10, stats.PIETY: 14, stats.CHARISMA: 11,
        stats.PHYSICAL_ATTACK: 5, stats.RESIST_POISON: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 12
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    GP_VALUE = 400
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.HAB_CAVE,
     context.MAP_DUNGEON, context.MTY_BOSS, context.MTY_LEADER,
     context.DES_EARTH, context.GEN_DRAGON )
    ENC_LEVEL = 8
    LONER = True
    COMPANIONS = ( YoungCaveDragon, )
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING, extra_effect=
        effects.SavingThrow( roll_skill=stats.RESIST_POISON, roll_stat=stats.TOUGHNESS, roll_modifier=50, on_failure = (
            effects.Enchant( enchantments.PoisonClassic, anim=animobs.DeathSparkle )
        ,)) )
    TECHNIQUES = ( invocations.MPInvocation( "Toxic Breath",
        effects.OpposedRoll( def_stat=stats.TOUGHNESS, anim=animobs.PoisonCloud, on_success = (
            effects.Paralyze( max_duration = 3 )
        ,) ), com_tar=targetarea.Cone(reach=6), ai_tar=invocations.vs_enemy, mp_cost=6
      ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 8, self ) )

class SwampDragon( base.Monster ):
    name = "Swamp Dragon"
    statline = { stats.STRENGTH: 17, stats.TOUGHNESS: 19, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 11, stats.PIETY: 15, stats.CHARISMA: 11,
        stats.RESIST_ACID: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 10
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    GP_VALUE = 400
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
      context.MTY_BOSS, context.MTY_LEADER,
     context.DES_EARTH, context.DES_WATER, context.GEN_DRAGON )
    ENC_LEVEL = 8
    LONER = True
    COMPANIONS = ( YoungSwampDragon, )
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Acid Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (3,8,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,), on_failure = (
        effects.HealthDamage( (1,12,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,) ), com_tar=targetarea.Line(reach=6), ai_tar=invocations.vs_enemy, mp_cost=6
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 8, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  9   ***
#  *******************************

class SkyDragon( base.Monster ):
    name = "Sky Dragon"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 18, stats.REFLEXES: 18, \
        stats.INTELLIGENCE: 14, stats.PIETY: 11, stats.CHARISMA: 13,
        stats.RESIST_LIGHTNING: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 18
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    GP_VALUE = 450
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_WILDERNESS, context.MTY_BOSS,
     context.DES_AIR, context.GEN_DRAGON )
    ENC_LEVEL = 9
    LONER = True
    COMPANIONS = ( YoungSkyDragon, )
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Lightning Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (5,6,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,), on_failure = (
        effects.HealthDamage( (2,8,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
      ,) ), com_tar=targetarea.Line(reach=8), ai_tar=invocations.vs_enemy, mp_cost=6
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 9, self ) )


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
    statline = { stats.STRENGTH: 22, stats.TOUGHNESS: 21, stats.REFLEXES: 16, \
        stats.INTELLIGENCE: 10, stats.PIETY: 16, stats.CHARISMA: 12,
        stats.PHYSICAL_ATTACK: 5, stats.RESIST_POISON: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 22
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    GP_VALUE = 600
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.HAB_CAVE,
     context.MAP_DUNGEON, context.MTY_LEADER,
     context.DES_EARTH, context.GEN_DRAGON )
    ENC_LEVEL = 12
    LONER = True
    COMPANIONS = ( CaveDragon, )
    ATTACK = items.Attack( (4,8,0), element = stats.RESIST_SLASHING, extra_effect=
        effects.SavingThrow( roll_skill=stats.RESIST_POISON, roll_stat=stats.TOUGHNESS, on_failure = (
            effects.Enchant( enchantments.PoisonClassic, anim=animobs.DeathSparkle )
        ,)) )
    TECHNIQUES = ( invocations.MPInvocation( "Toxic Breath",
        effects.OpposedRoll( def_stat=stats.TOUGHNESS, anim=animobs.PoisonCloud, on_success = (
            effects.Paralyze( max_duration = 3 )
        ,) ), com_tar=targetarea.Cone(reach=8), ai_tar=invocations.vs_enemy, mp_cost=9
      ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 12, self ) )

class OldSwampDragon( base.Monster ):
    name = "Old Swamp Dragon"
    statline = { stats.STRENGTH: 19, stats.TOUGHNESS: 22, stats.REFLEXES: 16, \
        stats.INTELLIGENCE: 12, stats.PIETY: 18, stats.CHARISMA: 12,
        stats.RESIST_ACID: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 20
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    GP_VALUE = 600
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
      context.MTY_LEADER,
     context.DES_EARTH, context.DES_WATER, context.GEN_DRAGON )
    ENC_LEVEL = 12
    LONER = True
    COMPANIONS = ( SwampDragon, )
    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Acid Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (5,8,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,), on_failure = (
        effects.HealthDamage( (2,12,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,) ), com_tar=targetarea.Line(reach=8), ai_tar=invocations.vs_enemy, mp_cost=9
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 12, self ) )


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

class AncientCaveDragon( base.Monster ):
    name = "Ancient Cave Dragon"
    statline = { stats.STRENGTH: 25, stats.TOUGHNESS: 24, stats.REFLEXES: 18, \
        stats.INTELLIGENCE: 12, stats.PIETY: 18, stats.CHARISMA: 12,
        stats.PHYSICAL_ATTACK: 10, stats.RESIST_POISON: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 32
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    GP_VALUE = 800
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.HAB_CAVE,
     context.MAP_DUNGEON, context.MTY_LEADER,
     context.DES_EARTH, context.GEN_DRAGON )
    ENC_LEVEL = 16
    LONER = True
    COMPANIONS = ( OldCaveDragon, )
    ATTACK = items.Attack( (8,8,0), element = stats.RESIST_SLASHING, extra_effect=
        effects.SavingThrow( roll_skill=stats.RESIST_POISON, roll_stat=stats.TOUGHNESS, roll_modifier=-25, on_failure = (
            effects.Enchant( enchantments.PoisonClassic, anim=animobs.DeathSparkle )
        ,)) )
    TECHNIQUES = ( invocations.MPInvocation( "Toxic Breath",
        effects.OpposedRoll( def_stat=stats.TOUGHNESS, anim=animobs.PoisonCloud, on_success = (
            effects.Paralyze( max_duration = 3 )
        ,) ), com_tar=targetarea.Cone(reach=10), ai_tar=invocations.vs_enemy, mp_cost=12
      ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 16, self ) )

class AncientSwampDragon( base.Monster ):
    name = "Ancient Swamp Dragon"
    statline = { stats.STRENGTH: 21, stats.TOUGHNESS: 25, stats.REFLEXES: 17, \
        stats.INTELLIGENCE: 13, stats.PIETY: 21, stats.CHARISMA: 13,
        stats.RESIST_ACID: 100 }
    SPRITENAME = "monster_dragons.png"
    FRAME = 30
    TEMPLATES = (stats.DRAGON,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    GP_VALUE = 800
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
      context.MTY_LEADER,
     context.DES_EARTH, context.DES_WATER, context.GEN_DRAGON )
    ENC_LEVEL = 16
    LONER = True
    COMPANIONS = ( OldSwampDragon, )
    ATTACK = items.Attack( (3,10,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Acid Breath",
      effects.OpposedRoll( att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (10,8,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,), on_failure = (
        effects.HealthDamage( (4,10,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,) ), com_tar=targetarea.Line(reach=10), ai_tar=invocations.vs_enemy, mp_cost=12
    ), )
    def init_monster( self ):
        self.levels.append( base.Terror( 16, self ) )


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


