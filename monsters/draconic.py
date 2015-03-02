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
import animals
import treasuretype
import abilities

# This file contains monsters that are not dragons proper, but which
# belong to the GEN_DRAGON faction. Examples include lizardmen and other
# assorted dragon henchmen.

#  *******************************
#  ***   ENCOUNTER  LEVEL  1   ***
#  *******************************


#  *******************************
#  ***   ENCOUNTER  LEVEL  2   ***
#  *******************************

#  *******************************
#  ***   ENCOUNTER  LEVEL  3   ***
#  *******************************

class Reptal( base.Monster ):
    name = "Reptal"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 15, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 8, stats.PIETY: 9, stats.CHARISMA: 9 }
    SPRITENAME = "monster_draconic.png"
    FRAME = 3
    TEMPLATES = (stats.REPTILE,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_WATER,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_DRAGON )
    ENC_LEVEL = 3
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  4   ***
#  *******************************

class ReptalWarrior( base.Monster ):
    name = "Reptal Warrior"
    statline = { stats.STRENGTH: 17, stats.TOUGHNESS: 15, stats.REFLEXES: 11, \
        stats.INTELLIGENCE: 8, stats.PIETY: 9, stats.CHARISMA: 9,
        stats.NATURAL_DEFENSE: 10 }
    SPRITENAME = "monster_draconic.png"
    FRAME = 5
    TEMPLATES = (stats.REPTILE,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_WATER,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_DRAGON )
    ENC_LEVEL = 4
    TREASURE = treasuretype.Standard()
    COMPANIONS = (Reptal,animals.GiantLizard,animals.GiantFrog)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )

class ReptalArcher( base.Monster ):
    name = "Reptal Archer"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 15, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 8, stats.PIETY: 9, stats.CHARISMA: 9 }
    SPRITENAME = "monster_draconic.png"
    FRAME = 4
    TEMPLATES = (stats.REPTILE,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_WATER,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_DRAGON )
    ENC_LEVEL = 4
    COMBAT_AI = aibrain.BasicTechnicalAI()
    TREASURE = treasuretype.Standard((items.ARROW,))
    COMPANIONS = (ReptalWarrior,Reptal)
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( abilities.LONGBOW, )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  5   ***
#  *******************************

class ReptalDruid( base.Monster ):
    name = "Reptal Druid"
    statline = { stats.STRENGTH: 17, stats.TOUGHNESS: 15, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 13, stats.PIETY: 13, stats.CHARISMA: 9 }
    SPRITENAME = "monster_draconic.png"
    FRAME = 6
    TEMPLATES = (stats.REPTILE,)
    MOVE_POINTS = 10
    VOICE = dialogue.voice.DRACONIAN
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_WATER,
     context.MTY_HUMANOID, context.MTY_MAGE, context.MTY_PRIEST,
     context.GEN_DRAGON, context.GEN_NATURE )
    ENC_LEVEL = 5
    TECHNIQUES = ( spells.solarspells.MODERATE_CURE, spells.firespells.IGNITE,
        spells.earthspells.ACID_BOLT, spells.firespells.EXPLOSION,
        spells.waterspells.REGENERATION )
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    TREASURE = treasuretype.HighItems(( items.scrolls.Rank2Scroll, items.scrolls.Rank3Scroll, items.potions.PotionOfStrength ))
    COMPANIONS = (ReptalWarrior,ReptalArcher)
    LONER = True
    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )


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








