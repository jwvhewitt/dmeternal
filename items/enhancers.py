#
# Contains magical or other effects that get attached to items.
#

import stats
import effects
import animobs
from . import SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, BOW, ARROW, SHIELD, \
    SLING, BULLET, CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, HAT, HELM, GLOVE, GAUNTLET, \
    SANDALS, SHOES, BOOTS, CLOAK, HOLYSYMBOL, WAND, FARMTOOL

class Enhancer( object ):
    NAMEPAT = "Enhanced {0}"
    DESCPAT = "{0}"
    PLUSRANK = 2
    AFFECTS = ()
    BONUSES = stats.StatMod()
    ATTACK_ON_HIT = None
    def get_name( self, it ):
        return self.NAMEPAT.format( it.true_name, it.itemtype.name )
    def cost( self ):
        return 250 * self.PLUSRANK

#  ********************************
#  ***   WEAPON  ENHANCEMENTS   ***
#  ********************************

class Defender( Enhancer ):
    NAMEPAT = "Defender {0}"
    DESCPAT = "{0} It has been enchanted to provide +10% defense."
    PLUSRANK = 1
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10, stats.NATURAL_DEFENSE: 10 })

class Seeker( Enhancer ):
    NAMEPAT = "Seeker {0}"
    DESCPAT = "{0} It has been enchanted to give +10% attack."
    PLUSRANK = 2
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, BOW, SLING)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 10 })

class Flaming( Enhancer ):
    NAMEPAT = "Flaming {0}"
    DESCPAT = "{0} It glows with magical fire that does an extra 1d8 damage."
    PLUSRANK = 4
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, ARROW, BULLET)
    ATTACK_ON_HIT = effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )

class Frost( Enhancer ):
    NAMEPAT = "Frost {0}"
    DESCPAT = "{0} It shimmers with magical cold that does an extra 1d8 damage."
    PLUSRANK = 4
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, ARROW, BULLET)
    ATTACK_ON_HIT = effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.BlueExplosion )

#  *******************************
#  ***   ARMOR  ENHANCEMENTS   ***
#  *******************************

class FineArmor( Enhancer ):
    NAMEPAT = "Fine {0}"
    DESCPAT = "{0} It has been enhanced to provide an additional +5% to both defense and aura."
    PLUSRANK = 2
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5, stats.MAGIC_DEFENSE: 5 })

#  ********************************
#  ***   SHIELD  ENHANCEMENTS   ***
#  ********************************

class ElementalShield( Enhancer ):
    NAMEPAT = "Elemental {0}"
    DESCPAT = "{0} It has been warded to provide 25% protection against fire, cold, lightning, and acid."
    PLUSRANK = 5
    AFFECTS = (SHIELD,)
    BONUSES = stats.StatMod({ stats.RESIST_FIRE:25, stats.RESIST_COLD: 25, stats.RESIST_LIGHTNING: 25, stats.RESIST_ACID: 25 })

#  *******************************
#  ***   CLOAK  ENHANCEMENTS   ***
#  *******************************

class DefenseCloak( Enhancer ):
    NAMEPAT = "{1} of Defense"
    DESCPAT = "{0} It has been enhanced to provide +5% to defense."
    PLUSRANK = 1
    AFFECTS = (CLOAK,)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class ElvenCloak( Enhancer ):
    NAMEPAT = "Elven {0}"
    DESCPAT = "{0} Its fine construction provides a +5% bonus to aura and stealth."
    PLUSRANK = 2
    AFFECTS = (CLOAK,)
    BONUSES = stats.StatMod({ stats.MAGIC_DEFENSE: 5, stats.STEALTH: 5 })

class ProtectionCloak( Enhancer ):
    NAMEPAT = "{1} of Protection"
    DESCPAT = "{0} It has been warded to provide 25% protection against fire, cold, lightning, and acid."
    PLUSRANK = 6
    AFFECTS = (CLOAK,)
    BONUSES = stats.StatMod({ stats.RESIST_FIRE:25, stats.RESIST_COLD: 25, stats.RESIST_LIGHTNING: 25, stats.RESIST_ACID: 25 })



