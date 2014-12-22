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
import treasuretype

#  *******************************
#  ***   ENCOUNTER  LEVEL  1   ***
#  *******************************

class Hurthling( base.Monster ):
    name = "Hurthling"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 8, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 10,
        stats.NATURAL_DEFENSE: 5 }
    SPRITENAME = "monster_people.png"
    FRAME = 5
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.HURTHISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.MTY_THIEF )
    ENC_LEVEL = 1
    TREASURE = treasuretype.Low()
    ATTACK = items.Attack( (1,4,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 1, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  2   ***
#  *******************************

class NoviceWarrior( base.Monster ):
    name = "Novice Warrior"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 13, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 10, \
        stats.COUNTER_ATTACK: 5 }
    SPRITENAME = "monster_people.png"
    FRAME = 0
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.DES_CIVILIZED,
     context.MTY_HUMANOID, context.MTY_FIGHTER,
     context.GEN_CHAOS )
    ENC_LEVEL = 2
    TREASURE = treasuretype.Low()
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )

class NoviceThief( base.Monster ):
    name = "Novice Thief"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 12, stats.PIETY: 10, stats.CHARISMA: 10,
        stats.STEALTH: 10 }
    SPRITENAME = "monster_people.png"
    FRAME = 2
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_CIVILIZED,
     context.MTY_HUMANOID, context.MTY_THIEF )
    ENC_LEVEL = 2
    TREASURE = treasuretype.Standard()
    COMPANIONS = (NoviceWarrior,)
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 1, self ) )



#  *******************************
#  ***   ENCOUNTER  LEVEL  3   ***
#  *******************************

class NovicePriest( base.Monster ):
    name = "Novice Priest"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 13, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 13, stats.PIETY: 15, stats.CHARISMA: 12 }
    SPRITENAME = "monster_spellcasters.png"
    FRAME = 0
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.DES_CIVILIZED, context.DES_SOLAR, context.DES_AIR,
     context.MTY_HUMANOID, context.MTY_PRIEST )
    ENC_LEVEL = 3
    TREASURE = treasuretype.Standard( ( items.scrolls.Rank1Scroll, items.scrolls.Rank2Scroll ) )
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (NoviceWarrior,)
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.waterspells.FREEZE_FOE, spells.airspells.SILENCE,
        spells.solarspells.BLESSING, spells.solarspells.MINOR_CURE )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )

class NoviceMage( base.Monster ):
    name = "Novice Mage"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 10, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 15, stats.PIETY: 13, stats.CHARISMA: 12 }
    SPRITENAME = "monster_spellcasters.png"
    FRAME = 21
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.DES_CIVILIZED, context.DES_LUNAR, context.DES_FIRE,
     context.MTY_HUMANOID, context.MTY_MAGE )
    ENC_LEVEL = 3
    TREASURE = treasuretype.Standard( ( items.scrolls.Rank1Scroll, items.scrolls.Rank2Scroll ) )
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (NovicePriest,NoviceWarrior)
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.firespells.FIRE_BOLT, spells.lunarspells.CURSE,
        spells.magespells.FIRE_ARC, spells.lunarspells.SLEEP )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 3, self ) )

class Highwayman( base.Monster ):
    name = "Highwayman"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 10, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 10 }
    SPRITENAME = "monster_people.png"
    FRAME = 4
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY, context.SET_RENFAN,
     context.MAP_WILDERNESS,
     context.DES_CIVILIZED,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.MTY_THIEF )
    ENC_LEVEL = 3
    TREASURE = treasuretype.Standard()
    COMPANIONS = (NoviceThief,)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  4   ***
#  *******************************

class NoviceDruid( base.Monster ):
    name = "Novice Druid"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 13, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 14, stats.PIETY: 14, stats.CHARISMA: 12 }
    SPRITENAME = "monster_spellcasters.png"
    FRAME = 8
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.DES_SOLAR, context.DES_EARTH, context.DES_FIRE,
     context.MTY_HUMANOID, context.MTY_PRIEST, context.GEN_NATURE )
    ENC_LEVEL = 4
    TREASURE = treasuretype.Standard( ( items.scrolls.Rank1Scroll, items.scrolls.Rank2Scroll ) )
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (animals.Wolf,animals.BlackBear)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.solarspells.MINOR_CURE, spells.earthspells.CALL_CRITTER,
        spells.earthspells.ACID_BOLT, spells.earthspells.BEASTLY_MIGHT )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )
        self.levels.append( base.Spellcaster( 2, self ) )

class Bushwhacker( base.Monster ):
    name = "Bushwhacker"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 13, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 12,
        stats.NATURAL_DEFENSE: 10 }
    SPRITENAME = "monster_people.png"
    FRAME = 1
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.MTY_THIEF, context.MTY_LEADER,
     context.GEN_CHAOS )
    ENC_LEVEL = 4
    TREASURE = treasuretype.Standard()
    COMPANIONS = (Highwayman,)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  5   ***
#  *******************************

class Necromancer( base.Monster ):
    name = "Necromancer"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 15, stats.PIETY: 13, stats.CHARISMA: 12 }
    SPRITENAME = "monster_spellcasters.png"
    FRAME = 23
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.DES_CIVILIZED, context.DES_LUNAR,
     context.MTY_HUMANOID, context.MTY_MAGE, context.GEN_UNDEAD )
    ENC_LEVEL = 5
    TREASURE = treasuretype.HighItems( ( items.scrolls.Rank2Scroll, items.scrolls.Rank3Scroll ) )
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (undead.Ghoul,undead.SkeletonWithMorningstar)
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.lunarspells.ENERVATE, spells.necrospells.ACID_CLOUD,
        spells.necrospells.TOUCH_OF_DEATH, spells.necrospells.RAISE_CORPSE )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 5, self ) )

class Warrior( base.Monster ):
    name = "Warrior"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 14, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 10, stats.PIETY: 12, stats.CHARISMA: 12,
        stats.NATURAL_DEFENSE: 10, stats.COUNTER_ATTACK: 15 }
    SPRITENAME = "monster_people.png"
    FRAME = 9
    TEMPLATES = ()
    MOVE_POINTS = 8
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_CIVILIZED,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.MTY_LEADER )
    ENC_LEVEL = 5
    TREASURE = treasuretype.Standard((items.SWORD,))
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 5, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  6   ***
#  *******************************

class Priest( base.Monster ):
    name = "Priest"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 14, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 13, stats.PIETY: 16, stats.CHARISMA: 12 }
    SPRITENAME = "monster_spellcasters.png"
    FRAME = 2
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.DES_CIVILIZED, context.DES_SOLAR, context.MTY_LEADER,
     context.MTY_HUMANOID, context.MTY_PRIEST )
    ENC_LEVEL = 6
    TREASURE = treasuretype.HighItems( ( items.scrolls.Rank2Scroll, items.scrolls.Rank3Scroll, items.POTION ) )
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (NoviceWarrior,NovicePriest,Warrior)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.waterspells.FREEZE_FOE, spells.priestspells.HEALING_LIGHT,
        spells.solarspells.SUNRAY, spells.airspells.SILENCE,
        spells.priestspells.HEROISM, spells.priestspells.ARMOR_OF_FAITH )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 6, self ) )

class Mercenary( base.Monster ):
    name = "Mercenary"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 14, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 10, stats.PIETY: 12, stats.CHARISMA: 12 }
    SPRITENAME = "monster_people.png"
    FRAME = 17
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_HUMANOID, context.MTY_FIGHTER )
    ENC_LEVEL = 6
    TREASURE = treasuretype.Low( (items.POLEARM,items.LIGHT_ARMOR) )
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING, reach=2 )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 6, self ) )

class Ranger( base.Monster ):
    name = "Ranger"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 12, \
        stats.STEALTH: 24 }
    SPRITENAME = "monster_people.png"
    FRAME = 16
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_NATURE )
    ENC_LEVEL = 6
    TREASURE = treasuretype.Standard( ( items.ARROW, items.BOW ) )
    COMPANIONS = (NoviceDruid,)
    COMBAT_AI = aibrain.BasicTechnicalAI()
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.Invocation( "Arrow",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_PIERCING, anim=animobs.RedBoom )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=8), shot_anim=animobs.Arrow, ai_tar=invocations.TargetEnemy()
    ), spells.earthspells.EARTHBIND )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 5, self ) )



#  *******************************
#  ***   ENCOUNTER  LEVEL  7   ***
#  *******************************

class Conjuoror( base.Monster ):
    name = "Conjuoror"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 16, stats.PIETY: 14, stats.CHARISMA: 12 }
    SPRITENAME = "monster_spellcasters.png"
    FRAME = 10
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.DES_CIVILIZED, context.DES_LUNAR, context.DES_FIRE,
     context.MTY_HUMANOID, context.MTY_MAGE )
    ENC_LEVEL = 7
    TREASURE = treasuretype.HighItems( ( items.scrolls.Rank3Scroll, items.scrolls.Rank4Scroll ) )
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (NovicePriest,NoviceWarrior,Warrior,Mercenary)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.magespells.LIGHTNING_BOLT, spells.lunarspells.SLEEP,
        spells.lunarspells.HELLBLAST, spells.firespells.EXPLOSION,
        spells.firespells.PYROTECHNICS
         )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 7, self ) )


class Executioner( base.Monster ):
    name = "Executioner"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 16, stats.REFLEXES: 12,
        stats.INTELLIGENCE: 10, stats.PIETY: 12, stats.CHARISMA: 10,
        stats.CRITICAL_HIT: 20 }
    SPRITENAME = "monster_people.png"
    FRAME = 6
    TEMPLATES = ()
    MOVE_POINTS = 8
    HABITAT = ( context.HAB_EVERY, context.SET_RENFAN,
     context.MTY_HUMANOID, context.MTY_BOSS,
     context.MTY_FIGHTER )
    ENC_LEVEL = 7
    TREASURE = treasuretype.Standard((items.AXE,))
    COMPANIONS = (Bushwhacker,)
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 6, self ) )

# Lieutenant - Sprite 11
# Druid - Sprite 6

#  *******************************
#  ***   ENCOUNTER  LEVEL  8   ***
#  *******************************

# Crusader - Get knightly sprite, PRIEST+WARRIOR, Sprite 21

#  *******************************
#  ***   ENCOUNTER  LEVEL  9   ***
#  *******************************

# Warden - spellcaster Sprite 5
# Witch - spellcaster Sprite 18
# Commander - Sprite 10


#  ********************************
#  ***   ENCOUNTER  LEVEL  10   ***
#  ********************************

class Healer( base.Monster ):
    name = "Healer"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 16, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 14, stats.PIETY: 18, stats.CHARISMA: 18 }
    SPRITENAME = "monster_spellcasters.png"
    FRAME = 16
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.DES_CIVILIZED, context.DES_SOLAR, context.DES_WATER, context.MTY_BOSS,
     context.MTY_HUMANOID, context.MTY_PRIEST )
    ENC_LEVEL = 10
    TREASURE = treasuretype.HighItems( ( items.potions.PotionOfHealing, items.scrolls.Rank4Scroll, items.scrolls.Rank5Scroll ) )
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (NoviceWarrior,NovicePriest,Warrior)
    ATTACK = items.Attack( (3,6,0), element = stats.RESIST_SOLAR,
        hit_anim=animobs.YellowExplosion )
    TECHNIQUES = ( spells.priestspells.SMITE, spells.solarspells.MASS_CURE,
        spells.solarspells.MAXIMUM_CURE, invocations.MPInvocation( "Repent",
            effects.TargetIsAlly( on_true = (
                effects.Enchant( enchantments.BlessingEn, anim=animobs.GreenSparkle ),
                effects.TargetIsDamaged( on_true= (
                    effects.HealthRestore( dice=(3,12,12) ),
                ))
            ), on_false=(
                effects.TargetIsEnemy( on_true = (
                    effects.HealthDamage( (3,12,0), stat_bonus=stats.CHARISMA, element=stats.RESIST_WATER, anim=animobs.Bubbles ),
                )),
            )), shot_anim=animobs.BlueComet, com_tar=targetarea.Blast(radius=3),
            ai_tar=invocations.TargetEnemy(), mp_cost=12 )
        )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 6, self ) )
        self.levels.append( base.Defender( 4, self ) )

#  ********************************
#  ***   ENCOUNTER  LEVEL  11   ***
#  ********************************

# Ranger Hero - Sprite 12


#  ********************************
#  ***   ENCOUNTER  LEVEL  12   ***
#  ********************************

# Antihero - Sprite 18
# High Priest - Sprite 1


#  ********************************
#  ***   ENCOUNTER  LEVEL  13   ***
#  ********************************

# High Druid - Sprite 7

#  ********************************
#  ***   ENCOUNTER  LEVEL  14   ***
#  ********************************


#  ********************************
#  ***   ENCOUNTER  LEVEL  15   ***
#  ********************************

# Bishop - Sprite 3

#  ********************************
#  ***   ENCOUNTER  LEVEL  16   ***
#  ********************************

# Master Druid - Sprite 11

#  ********************************
#  ***   ENCOUNTER  LEVEL  17   ***
#  ********************************


#  ********************************
#  ***   ENCOUNTER  LEVEL  18   ***
#  ********************************

# Cannoness - Sprite 4

#  ********************************
#  ***   ENCOUNTER  LEVEL  19   ***

#  ********************************

# Elder Druid - Sprite 9

#  ********************************
#  ***   ENCOUNTER  LEVEL  20   ***
#  ********************************

# Archmage - Sprite 24



