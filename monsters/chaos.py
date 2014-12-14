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
import animals
import undead
import enchantments
import people
import treasuretype

#
# Chaos is not necessarily a destructive force- though to the powers-that-be
# the distinction between creation and destruction may seem small.
#
# SOLAR chaos is the Erisian sect, reveling in creation and life, heedless of
#  consequence.
#
# FIRE chaos is that of blood; it seeks danger and conflict, proving itself in
#  battle. Specializes in physical attack.
#
# WATER chaos is survival and mutation. Life adapts, changing the world around
#  it in the process and spurring new changes. Specializes in defense.
#
# EARTH chaos is decadence and artifice. Greed and competition.
#  Generalist rather than specialist.
#
# AIR chaos is that of secrets and heresy. Whispers that may cause the rise
#  or fall of empires. Specializes in magic and stealth.
#
# LUNAR chaos is the nihilistic sect, seeking only destruction.
#  Has most of the monsters rather than sentient followers.
#
# Many chaos followers are either MTY_MAGE or MTY_FIGHTER.
#

#  *******************************
#  ***   ENCOUNTER  LEVEL  1   ***
#  *******************************

class Cultist( base.Monster ):
    name = "Cultist"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 10, \
        stats.PHYSICAL_ATTACK: 15 }
    SPRITENAME = "monster_chaos.png"
    FRAME = 1
    TEMPLATES = ()
    MOVE_POINTS = 10
    TREASURE = treasuretype.Low()
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_HUMANOID, context.GEN_CHAOS )
    ENC_LEVEL = 1
    ATTACK = items.Attack( (1,4,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 1, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  2   ***
#  *******************************

class Hooligan( base.Monster ):
    name = "Hooligan"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 6, stats.PIETY: 10, stats.CHARISMA: 5 }
    SPRITENAME = "monster_chaos.png"
    FRAME = 14
    TEMPLATES = ()
    MOVE_POINTS = 8
    TREASURE = treasuretype.Standard()
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_LUNAR,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_CHAOS )
    ENC_LEVEL = 2
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  3   ***
#  *******************************

class Heretic( base.Monster ):
    name = "Heretic"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 10, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 13, stats.PIETY: 13, stats.CHARISMA: 12 }
    SPRITENAME = "monster_chaos.png"
    FRAME = 17
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_AIR,
     context.MTY_HUMANOID, context.MTY_MAGE, context.GEN_CHAOS )
    ENC_LEVEL = 3
    COMBAT_AI = aibrain.BasicTechnicalAI()
    TREASURE = treasuretype.Standard( ( items.scrolls.Rank1Scroll, items.scrolls.Rank2Scroll ) )
    TECHNIQUES = ( spells.firespells.IGNITE,
        spells.druidspells.ACID_SPRAY, spells.waterspells.FREEZE_FOE )
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )

class CultLeader( base.Monster ):
    name = "Cult Leader"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 16, \
        stats.PHYSICAL_ATTACK: 5 }
    SPRITENAME = "monster_chaos.png"
    FRAME = 2
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_HUMANOID, context.MTY_PRIEST, context.GEN_CHAOS )
    ENC_LEVEL = 3
    LONER = True
    TREASURE = treasuretype.High()
    COMPANIONS = ( Cultist, Cultist, Heretic, people.NoviceWarrior )
    TECHNIQUES = ( spells.solarspells.MODERATE_CURE, spells.lunarspells.WIZARD_MISSILE )
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING, extra_effect =
         effects.OpposedRoll( on_success = (
            effects.Paralyze( max_duration = 6 )
        ,) )
     )
    def init_monster( self ):
        self.levels.append( base.Leader( 3, self ) )

class Centaur( base.Monster ):
    name = "Centaur"    
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 13, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 12 }
    SPRITENAME = "monster_chaos.png"
    FRAME = 19
    TEMPLATES = ()
    MOVE_POINTS = 12
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.DES_SOLAR,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_CHAOS )
    ENC_LEVEL = 3
    COMBAT_AI = aibrain.BasicTechnicalAI()
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.Invocation( "Arrow",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_PIERCING, anim=animobs.RedBoom )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=8), shot_anim=animobs.Arrow, ai_tar=invocations.vs_enemy
    ), )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )

# MARAUDER (Fire,Fighter)



#  *******************************
#  ***   ENCOUNTER  LEVEL  4   ***
#  *******************************

# Earth, Water generally on evens

# BEASTMAN (Lunar,Fighter)
# CHAOS WARRIOR (Fighter)
# CROSSBOWMAN (Earth,Fighter)
# CHAOS MAGE (Mage)
# (Water)

#  *******************************
#  ***   ENCOUNTER  LEVEL  5   ***
#  *******************************

# Fire, Air generally on odds

# Blood Warrior (Fire,Fighter)
# Death Dancer (Air,Fighter)
# MUTANT (Lunar)

class CentaurWarrior( base.Monster ):
    name = "Centaur Warrior"    
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 15, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 12, \
        stats.PHYSICAL_ATTACK: 5, stats.COUNTER_ATTACK: 15 }
    SPRITENAME = "monster_chaos.png"
    FRAME = 20
    TEMPLATES = ()
    MOVE_POINTS = 12
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.DES_SOLAR,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_CHAOS )
    ENC_LEVEL = 5
    TREASURE = treasuretype.Standard((items.ARROW,))
    COMPANIONS = ( Centaur, )
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_PIERCING )
    TECHNIQUES = ( invocations.Invocation( "Arrow",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_PIERCING, anim=animobs.RedBoom )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=8), shot_anim=animobs.Arrow, ai_tar=invocations.vs_enemy
    ), )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 5, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  6   ***
#  *******************************

# Chaos Knight
# Bronze Knight (Earth)
# Warper (Water,Mage)
# Killer Clown (Lunar)

#  *******************************
#  ***   ENCOUNTER  LEVEL  7   ***
#  *******************************

# Blood Knight (Fire)
# Astrologer (Air)

class CentaurKnight( base.Monster ):
    name = "Centaur Knight"    
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 16, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 12, stats.PIETY: 14, stats.CHARISMA: 13, \
        stats.NATURAL_DEFENSE: 10, stats.MAGIC_DEFENSE: 10 }
    SPRITENAME = "monster_chaos.png"
    FRAME = 4
    TEMPLATES = ()
    MOVE_POINTS = 12
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.DES_SOLAR,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_CHAOS )
    ENC_LEVEL = 7
    TREASURE = treasuretype.Standard((items.ARROW,))
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = ( Centaur, CentaurWarrior )
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.Invocation( "Arrow",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,10,0), stat_bonus=stats.STRENGTH, element=stats.RESIST_PIERCING, anim=animobs.RedBoom )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=9), shot_anim=animobs.Arrow, ai_tar=invocations.vs_enemy
    ), spells.solarspells.MAJOR_CURE, spells.solarspells.CURE_POISON )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 7, self ) )

# Plague Bearer (Water)

#  *******************************
#  ***   ENCOUNTER  LEVEL  8   ***
#  *******************************

# Chaos Sorceror
# Plague Knight (Water)
# Paragon (Earth)
# Mad Monk

#  *******************************
#  ***   ENCOUNTER  LEVEL  9   ***
#  *******************************

# Flame Mother (Fire,Mage)
# Deceiver (Air,Mage)
# Creeping Chaos

class CentaurChampion( base.Monster ):
    name = "Centaur Champion"    
    statline = { stats.STRENGTH: 17, stats.TOUGHNESS: 17, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 13, stats.PIETY: 15, stats.CHARISMA: 13, \
        stats.NATURAL_DEFENSE: 15 }
    SPRITENAME = "monster_chaos.png"
    FRAME = 9
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.DES_SOLAR,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.MTY_LEADER, context.MTY_BOSS,
     context.GEN_CHAOS )
    ENC_LEVEL = 9
    TREASURE = treasuretype.Standard((items.ARROW,items.POLEARM))
    COMPANIONS = ( CentaurKnight, CentaurWarrior )
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING,
     extra_effect=effects.OpposedRoll( att_stat=None, def_stat=stats.TOUGHNESS, on_success = (
            effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
            effects.Enchant( enchantments.PoisonClassic )
        ,) )
    )
    TECHNIQUES = ( invocations.Invocation( "Arrow",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,10,0), stat_bonus=stats.STRENGTH, element=stats.RESIST_PIERCING, anim=animobs.RedBoom )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=9), shot_anim=animobs.Arrow, ai_tar=invocations.vs_enemy
    ), )
    def init_monster( self ):
        self.levels.append( base.Leader( 9, self ) )


#  ********************************
#  ***   ENCOUNTER  LEVEL  10   ***
#  ********************************

# Chaos Champion
# Plague Lord (Water)
# Golden Champion (Earth)
# Desecrator (Lunar)

#  ********************************
#  ***   ENCOUNTER  LEVEL  11   ***
#  ********************************

# Blood Champion (Fire)
# Warlock (Air)

class CentaurHero( base.Monster ):
    name = "Centaur Hero"    
    statline = { stats.STRENGTH: 18, stats.TOUGHNESS: 18, stats.REFLEXES: 16, \
        stats.INTELLIGENCE: 13, stats.PIETY: 15, stats.CHARISMA: 13, \
        stats.NATURAL_DEFENSE: 20 }
    SPRITENAME = "monster_chaos.png"
    FRAME = 23
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.DES_SOLAR,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.MTY_LEADER, context.MTY_BOSS,
     context.GEN_CHAOS )
    ENC_LEVEL = 11
    TREASURE = treasuretype.Standard((items.ARROW,items.POLEARM,items.BOW))
    COMBAT_AI = aibrain.BasicTechnicalAI()
    LONER = True
    COMPANIONS = ( CentaurKnight, CentaurChampion )
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING,
     extra_effect=effects.OpposedRoll( att_stat=None, def_stat=stats.TOUGHNESS, on_success = (
            effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
            effects.Enchant( enchantments.PoisonClassic )
        ,) )
    )
    TECHNIQUES = ( invocations.Invocation( "Arrow 23",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (2,8,0), stat_bonus=stats.STRENGTH, element=stats.RESIST_PIERCING, anim=animobs.RedBoom ),
        effects.OpposedRoll( att_stat=None, att_modifier=5, on_success = (
            effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud ),
            effects.Enchant( enchantments.BurnLowEn )
        ,) )
      ,), on_failure = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_PIERCING, anim=animobs.RedBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=9), shot_anim=animobs.Arrow, ai_tar=invocations.vs_enemy
    ), spells.solarspells.MAJOR_CURE, spells.solarspells.CURE_POISON )
    def init_monster( self ):
        self.levels.append( base.Leader( 11, self ) )


#  ********************************
#  ***   ENCOUNTER  LEVEL  12   ***
#  ********************************

# Libertine (Earth)
# Corruptor (Water)

#  ********************************
#  ***   ENCOUNTER  LEVEL  13   ***
#  ********************************

# Warlord (Fire)
# Nemesis (Air)

#  ********************************
#  ***   ENCOUNTER  LEVEL  14   ***
#  ********************************

# Exalted

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





