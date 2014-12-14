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
import spells
import random
import enchantments
import treasuretype

#  *************************
#  ***   UNDEAD  TYPES   ***
#  *************************
#
# DES_LUNAR undead are most likely to show up in unholy or haunted places.
#  These undead are cursed to wander the earth, reduced to soulless husks who
#  can do no more than lament their state, if they have a mind left at all.
#  This category includes zombies, ghouls, vampires, and other lost souls.
#  In addition to being somewhat hard to kill, these undead frequently have
#  special abilities such as ability drain or paralysis.
#
# DES_EARTH undead are cthonic spirits, usually of the long dead or past
#  civilizations. They are frequently encountered underground. Deep beneath
#  the surface, it is rumored that there exist whole necropolises of the dead.
#  This category includes skeletons and liches. They tend to have fewer special
#  abilities than LUNAR undead, but are more physically powerful.
#
# DES_AIR undead are mischevious and malevolent spirits. They are usually
#  incorporeal, often invisible, always mysterious. This category includes
#  poltergeists, apparitions, ghosts, and specters. They rely upon special
#  abilities and defenses to a greater degree than LUNAR undead.
#
# DES_SOLAR undead are the righteous dead. They have usually taken on the curse
#  of undeath willingly in order to pursue some higher goal. These undead
#  frequently serve as the guardians of ancient tombs and abandoned temples.
#  They tend to be hard to kill, with different types having healing powers or
#  even regeneration. This category includes mummies and avenging spirits.
#



#  *******************************
#  ***   ENCOUNTER  LEVEL  1   ***
#  *******************************

class SkeletalHound( base.Monster ):
    name = "Skeletal Hound"
    statline = { stats.STRENGTH: 9, stats.TOUGHNESS: 9, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 1, stats.PIETY: 1, stats.CHARISMA: 1,
        stats.AWARENESS: 25 }
    SPRITENAME = "monster_skeletons.png"
    FRAME = 20
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 12
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_EARTH,
     context.MTY_UNDEAD, context.MTY_BEAST,
     context.GEN_UNDEAD )
    ENC_LEVEL = 1

    COMBAT_AI = aibrain.BrainDeadAI()

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 1, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  2   ***
#  *******************************

class Skeleton( base.Monster ):
    name = "Skeleton"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 1 }
    SPRITENAME = "monster_skeletons.png"
    FRAME = 0
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MTY_UNDEAD, 
     context.DES_EARTH, context.GEN_UNDEAD )
    ENC_LEVEL = 2
    TREASURE = treasuretype.Low()
    COMPANIONS = (SkeletalHound,)

    COMBAT_AI = aibrain.SteadyAI()

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )

class SkeletonWithDagger( base.Monster ):
    name = "Skeleton"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 1 }
    SPRITENAME = "monster_skeletons.png"
    FRAME = 1
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_UNDEAD, 
     context.DES_EARTH, context.GEN_UNDEAD )
    ENC_LEVEL = 2
    TREASURE = treasuretype.Standard()
    COMPANIONS = (Skeleton,)
    COMBAT_AI = aibrain.SteadyAI()
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  3   ***
#  *******************************

class Zombie( base.Monster ):
    name = "Zombie"
    statline = { stats.STRENGTH: 11, stats.TOUGHNESS: 14, stats.REFLEXES: 4, \
        stats.INTELLIGENCE: 2, stats.PIETY: 8, stats.CHARISMA: 1 }
    SPRITENAME = "monster_undead.png"
    FRAME = 9
    TEMPLATES = (stats.UNDEAD,stats.FLESHY)
    MOVE_POINTS = 6
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.HAB_TUNNELS, context.SET_EVERY,
     context.MTY_UNDEAD, 
     context.DES_LUNAR, context.GEN_UNDEAD )
    ENC_LEVEL = 3
    TREASURE = treasuretype.Low()
    COMBAT_AI = aibrain.BrainDeadAI()
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )

class SkeletonWithMorningstar( base.Monster ):
    name = "Skeleton"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 1 }
    SPRITENAME = "monster_skeletons.png"
    FRAME = 3
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_UNDEAD, 
     context.DES_EARTH, context.GEN_UNDEAD )
    ENC_LEVEL = 3
    TREASURE = treasuretype.Low()
    COMPANIONS = (Skeleton,SkeletonWithDagger)
    COMBAT_AI = aibrain.SteadyAI()
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )

class SkeletalBat( base.Monster ):
    name = "Skeletal Bat"
    statline = { stats.STRENGTH: 9, stats.TOUGHNESS: 9, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 1, stats.CHARISMA: 1 }
    SPRITENAME = "monster_skeletons.png"
    FRAME = 24
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 12
    VOICE = None
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY,
     context.DES_AIR, context.DES_LUNAR,
     context.MTY_UNDEAD, context.MTY_BEAST,
     context.GEN_UNDEAD )
    ENC_LEVEL = 3
    COMBAT_AI = aibrain.BrainDeadAI()
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING, extra_effect=
        effects.SavingThrow( roll_skill=stats.RESIST_LUNAR, roll_stat=stats.TOUGHNESS, on_failure = (
            effects.StatDamage( stats.PIETY, anim=animobs.BloodSplat )
        ,))
    )
    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )

class SkeletonGuard( base.Monster ):
    name = "Skeleton Guard"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 16, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 1,
        stats.NATURAL_DEFENSE: 10 }
    SPRITENAME = "monster_skeletons.png"
    FRAME = 6
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 8
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_UNDEAD, 
     context.DES_EARTH, context.DES_SOLAR, context.GEN_UNDEAD )
    ENC_LEVEL = 3
    TREASURE = treasuretype.High()
    COMPANIONS = (SkeletonWithDagger,SkeletonWithMorningstar)
    COMBAT_AI = aibrain.SteadyAI()
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Defender( 3, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  4   ***
#  *******************************

class Ghoul( base.Monster ):
    name = "Ghoul"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 15, stats.REFLEXES: 8, \
        stats.INTELLIGENCE: 11, stats.PIETY: 10, stats.CHARISMA: 4 }
    SPRITENAME = "monster_undead.png"
    FRAME = 35
    TEMPLATES = (stats.UNDEAD,stats.FLESHY)
    MOVE_POINTS = 8
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.HAB_TUNNELS, context.SET_EVERY,
     context.MTY_UNDEAD, 
     context.DES_LUNAR, context.GEN_UNDEAD )
    ENC_LEVEL = 4
    TREASURE = treasuretype.Standard()
    COMPANIONS = (Zombie,animals.PlagueRat)
    COMBAT_AI = aibrain.GhoulAI()
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING, extra_effect =
         effects.OpposedRoll( att_modifier=-10, on_success = (
            effects.Paralyze( max_duration = 6 )
        ,) )
     )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )

class SkeletonFighter( base.Monster ):
    name = "Skeleton Fighter"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 12, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 1,
        stats.NATURAL_DEFENSE: 10 }
    SPRITENAME = "monster_skeletons.png"
    FRAME = 5
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_UNDEAD, context.MTY_HUMANOID, context.MTY_FIGHTER, 
     context.DES_EARTH, context.GEN_UNDEAD )
    ENC_LEVEL = 4
    TREASURE = treasuretype.Standard()
    COMPANIONS = (SkeletonWithDagger,SkeletonWithMorningstar)
    COMBAT_AI = aibrain.SteadyAI()
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )

class SkeletonThief( base.Monster ):
    name = "Skeleton Thief"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 12, stats.REFLEXES: 16, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 1,
        stats.STEALTH: 20 }
    SPRITENAME = "monster_skeletons.png"
    FRAME = 13
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 12
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_UNDEAD, context.MTY_HUMANOID, context.MTY_THIEF, 
     context.DES_EARTH, context.GEN_UNDEAD )
    ENC_LEVEL = 4
    TREASURE = treasuretype.Standard()
    COMPANIONS = (SkeletonFighter,SkeletalBat)
    COMBAT_AI = aibrain.SteadyAI()
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  5   ***
#  *******************************

class PlagueZombie( base.Monster ):
    name = "Plague Zombie"
    statline = { stats.STRENGTH: 11, stats.TOUGHNESS: 14, stats.REFLEXES: 4, \
        stats.INTELLIGENCE: 2, stats.PIETY: 8, stats.CHARISMA: 1 }
    SPRITENAME = "monster_undead.png"
    FRAME = 10
    TEMPLATES = (stats.UNDEAD,stats.FLESHY)
    MOVE_POINTS = 6
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.HAB_TUNNELS,
     context.SET_EVERY, context.SET_RENFAN,
     context.MTY_UNDEAD, 
     context.DES_LUNAR, context.GEN_UNDEAD )
    ENC_LEVEL = 5
    TREASURE = treasuretype.High()
    COMPANIONS = (Zombie,Ghoul)
    COMBAT_AI = aibrain.BrainDeadAI()
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_CRUSHING, extra_effect=
        effects.SavingThrow( roll_skill=stats.RESIST_LUNAR, roll_stat=stats.TOUGHNESS, on_failure = (
            effects.StatDamage( stats.TOUGHNESS, anim=animobs.GreenBoom )
        ,))
    )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 6, self ) )

class Shade( base.Monster ):
    name = "Shade"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 8, \
        stats.RESIST_SOLAR: -50, stats.RESIST_FIRE: -100, stats.STEALTH: 10 }
    SPRITENAME = "monster_undead.png"
    FRAME = 42
    TEMPLATES = (stats.UNDEAD,stats.INCORPOREAL)
    MOVE_POINTS = 6
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_UNDEAD, 
     context.DES_AIR, context.GEN_UNDEAD )
    ENC_LEVEL = 5
    ATTACK = items.Attack( (2,4,0), element = stats.RESIST_ATOMIC, extra_effect=
        effects.SavingThrow( roll_skill=stats.RESIST_LUNAR, roll_stat=stats.TOUGHNESS, on_failure = (
            effects.StatDamage( stats.STRENGTH, anim=animobs.GreenBoom )
        ,))
    )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 5, self ) )

class SkeletonMage( base.Monster ):
    name = "Skeleton Mage"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 14, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 16, stats.PIETY: 14, stats.CHARISMA: 10 }
    SPRITENAME = "monster_skeletons.png"
    FRAME = 15
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 10
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_UNDEAD, context.MTY_HUMANOID, context.MTY_MAGE, context.MTY_BOSS,
     context.DES_EARTH, context.GEN_UNDEAD )
    ENC_LEVEL = 5
    TREASURE = treasuretype.HighItems( ( items.scrolls.Rank2Scroll, items.scrolls.Rank3Scroll ) )
    COMPANIONS = (SkeletonFighter,SkeletonGuard)
    LONER = True
    TECHNIQUES = ( spells.waterspells.FREEZE_FOE, spells.airspells.SILENCE,
        spells.lunarspells.SLEEP, spells.firespells.IGNITE,
        spells.firespells.EXPLOSION, spells.airspells.THUNDER_STRIKE )
    COMBAT_AI = aibrain.SteadySpellAI()
    ATTACK = items.Attack( (1,8,2), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 4, self ) )

class Mummy( base.Monster ):
    name = "Mummy"
    statline = { stats.STRENGTH: 20, stats.TOUGHNESS: 20, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 6, stats.PIETY: 14, stats.CHARISMA: 15 }
    SPRITENAME = "monster_undead.png"
    FRAME = 47
    TEMPLATES = (stats.UNDEAD,stats.MUMMY)
    MOVE_POINTS = 6
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.HAB_TUNNELS, context.SET_EVERY,
     context.MTY_UNDEAD, 
     context.DES_SOLAR, context.GEN_UNDEAD )
    ENC_LEVEL = 5
    TREASURE = treasuretype.High()
    COMBAT_AI = aibrain.BrainDeadAI()
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_CRUSHING, extra_effect =
         effects.OpposedRoll( att_modifier=-10, on_success = (
            effects.StatDamage( stats.TOUGHNESS, anim=animobs.GreenBoom ),
            effects.Enchant( enchantments.DiseaseEn, anim=None )
        ,) )
     )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 5, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  6   ***
#  *******************************

class Ghast( base.Monster ):
    name = "Ghast"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 17, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 11, stats.PIETY: 12, stats.CHARISMA: 4,
        stats.PHYSICAL_ATTACK: 10 }
    SPRITENAME = "monster_undead.png"
    FRAME = 40
    TEMPLATES = (stats.UNDEAD,stats.FLESHY)
    MOVE_POINTS = 8
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.HAB_TUNNELS, context.SET_EVERY,
     context.MTY_UNDEAD, 
     context.DES_LUNAR, context.GEN_UNDEAD )
    ENC_LEVEL = 6
    TREASURE = treasuretype.High()
    COMPANIONS = (PlagueZombie,Ghoul)
    COMBAT_AI = aibrain.GhoulAI()
    ATTACK = items.Attack( (1,12,0), element = stats.RESIST_CRUSHING, extra_effect =
         effects.OpposedRoll( att_modifier=0, on_success = (
            effects.Paralyze( max_duration = 6 )
        ,) )
     )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 6, self ) )

class SkeletonHunter( base.Monster ):
    name = "Skeleton Hunter"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 12, stats.REFLEXES: 16, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 10,
        stats.NATURAL_DEFENSE: 10, stats.PHYSICAL_ATTACK: 5 }
    SPRITENAME = "monster_skeletons.png"
    FRAME = 9
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 8
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.SET_RENFAN,
     context.MTY_UNDEAD, context.MTY_HUMANOID, context.MTY_FIGHTER, context.MTY_BOSS, 
     context.DES_EARTH, context.GEN_UNDEAD )
    ENC_LEVEL = 6
    TREASURE = treasuretype.High((items.BOW,items.ARROW,items.ARROW))
    LONER = True
    COMPANIONS = (Shade,Ghast,SkeletonMage,SkeletonFighter,SkeletonThief,SkeletalHound)
    COMBAT_AI = aibrain.SteadyAI()
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( invocations.Invocation( "Arrow",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_PIERCING, anim=animobs.RedBoom ),
        effects.TargetIs( effects.ANIMAL, on_true=(
            effects.PercentRoll( roll_skill=stats.MAGIC_ATTACK, roll_stat=None, 
            roll_modifier=-5, target_affects=True, on_success=(
                effects.InstaKill( anim=animobs.CriticalHit )
            ,) )
        ,) ) 
      ), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=8), shot_anim=animobs.Arrow, ai_tar=invocations.vs_enemy
    ), )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 5, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  7   ***
#  *******************************

class MummyPriest( base.Monster ):
    name = "Mummy Priest"
    statline = { stats.STRENGTH: 22, stats.TOUGHNESS: 20, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 16, stats.CHARISMA: 15 }
    SPRITENAME = "monster_undead.png"
    FRAME = 48
    TEMPLATES = (stats.UNDEAD,stats.MUMMY)
    MOVE_POINTS = 6
    VOICE = None
    HABITAT = ( context.HAB_EVERY, context.HAB_TUNNELS, context.SET_EVERY,
     context.MTY_UNDEAD, context.MTY_HUMANOID, context.MTY_PRIEST, context.MTY_MAGE, context.MTY_BOSS,
     context.DES_SOLAR, context.GEN_UNDEAD )
    ENC_LEVEL = 7
    TREASURE = treasuretype.High(( items.scrolls.Rank3Scroll, items.scrolls.Rank4Scroll ))
    COMPANIONS = (Mummy,animals.Scarab,animals.TombScorpion)
    COMBAT_AI = aibrain.SteadySpellAI()
    TECHNIQUES = ( spells.lunarspells.HELLBLAST, spells.priestspells.HEALING_LIGHT,
        spells.priestspells.DIVINE_HAMMER, spells.solarspells.MAJOR_CURE,
        spells.priestspells.SANCTUARY, spells.magespells.INCINERATE
    )
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_CRUSHING, extra_effect =
         effects.OpposedRoll( att_modifier=-10, on_success = (
            effects.StatDamage( stats.TOUGHNESS, anim=animobs.GreenBoom ),
            effects.Enchant( enchantments.DiseaseEn, anim=None )
        ,) )
     )
    def init_monster( self ):
        self.levels.append( base.Leader( 7, self ) )
        self.condition.append( enchantments.PermaRegeneration() )


#  *******************************
#  ***   ENCOUNTER  LEVEL  8   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  9   ***
#  *******************************

# Mummy #3

#  ********************************
#  ***   ENCOUNTER  LEVEL  10   ***
#  ********************************


class Fossil( base.Monster ):
    name = "Fossil"
    statline = { stats.STRENGTH: 24, stats.TOUGHNESS: 19, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 14, stats.CHARISMA: 1,
        stats.RESIST_LUNAR: 155 }
    SPRITENAME = "monster_skeletons.png"
    FRAME = 27
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 6
    VOICE = None
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY,
     context.DES_LUNAR, context.DES_EARTH,
     context.MTY_UNDEAD, context.MTY_BEAST, context.MTY_BOSS,
     context.GEN_UNDEAD, context.GEN_NATURE )
    ENC_LEVEL = 10

    COMBAT_AI = aibrain.BrainDeadAI()

    ATTACK = items.Attack( (3,8,0), element = stats.RESIST_CRUSHING )

    TECHNIQUES = ( invocations.MPInvocation( "Hellfire",
      effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, att_modifier=10, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,10,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion, on_success = (
            effects.SavingThrow( roll_skill=stats.RESIST_LUNAR, roll_stat=stats.TOUGHNESS, on_failure = (
                effects.StatDamage( stats.STRENGTH, anim=animobs.GreenBoom )
            ,))
         ,))
      ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion )
      ,) ), com_tar=targetarea.Blast(radius=2), shot_anim=animobs.MysticBolt, ai_tar=invocations.vs_enemy, mp_cost=3
    ), )

    def init_monster( self ):
        self.levels.append( base.Beast( 10, self ) )

#  ********************************
#  ***   ENCOUNTER  LEVEL  11   ***
#  ********************************

# Mummy #4

#  ********************************
#  ***   ENCOUNTER  LEVEL  12   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  13   ***
#  ********************************

# Mummy #5

#  ********************************
#  ***   ENCOUNTER  LEVEL  14   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  15   ***
#  ********************************

# Mummy #6

#  ********************************
#  ***   ENCOUNTER  LEVEL  16   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  17   ***
#  ********************************

# Mummy #7

#  ********************************
#  ***   ENCOUNTER  LEVEL  18   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  19   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  20   ***
#  ********************************



