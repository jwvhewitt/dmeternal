#
# Contains magical or other effects that get attached to items.
#

import stats
import effects
import animobs
from . import SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, BOW, ARROW, SHIELD, \
    SLING, BULLET, CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, HAT, HELM, GLOVE, GAUNTLET, \
    SANDALS, SHOES, BOOTS, CLOAK, HOLYSYMBOL, WAND, FARMTOOL
import enchantments

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
    PLUSRANK = 2
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10, stats.NATURAL_DEFENSE: 10 })

class Seeker( Enhancer ):
    NAMEPAT = "Seeker {0}"
    DESCPAT = "{0} It has been enchanted to give +10% attack."
    PLUSRANK = 2
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, BOW, SLING)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 10 })

class Balanced( Enhancer ):
    NAMEPAT = "Balanced {0}"
    DESCPAT = "{0} It is balanced to give +5% attack and +5% defense."
    PLUSRANK = 2
    AFFECTS = (SWORD, DAGGER, STAFF)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class DreadWeapon( Enhancer ):
    NAMEPAT = "Dread {0}"
    DESCPAT = "{0} Targets struck by this weapon may find themselves cursed."
    PLUSRANK = 3
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, BOW, SLING)
    ATTACK_ON_HIT = effects.Enchant( enchantments.CurseEn, anim=animobs.PurpleSparkle )

class Smasher( Enhancer ):
    NAMEPAT = "{1} of Smashing"
    DESCPAT = "{0} This weapon does extra damage to constructs."
    PLUSRANK = 3
    AFFECTS = (AXE, MACE, STAFF)
    ATTACK_ON_HIT = effects.TargetIs( effects.CONSTRUCT, on_true=(
            effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_ATOMIC, anim=animobs.EarthBoom )
        ,))
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5 })

class Lockpick( Enhancer ):
    NAMEPAT = "Lockpick {0}"
    DESCPAT = "{0} It contains tools which give +15% to disarm traps."
    PLUSRANK = 3
    AFFECTS = (DAGGER,)
    BONUSES = stats.StatMod({ stats.DISARM_TRAPS: 15 })

class Blessed( Enhancer ):
    NAMEPAT = "Blessed {0}"
    DESCPAT = "{0} This weapon does extra damage to unholy creatures."
    PLUSRANK = 4
    AFFECTS = (SWORD, MACE, STAFF, POLEARM, ARROW, BULLET)
    ATTACK_ON_HIT = effects.TargetIs( effects.UNHOLY, on_true=(
            effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
        ,))
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5 })

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

class Slimy( Enhancer ):
    NAMEPAT = "Slimy {0}"
    DESCPAT = "{0} It does an extra 1d8 acid damage."
    PLUSRANK = 4
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, ARROW, BULLET)
    ATTACK_ON_HIT = effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )

class Shocking( Enhancer ):
    NAMEPAT = "Shocking {0}"
    DESCPAT = "{0} It calls magical lightning that does an extra 1d8 damage."
    PLUSRANK = 4
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, ARROW, BULLET)
    ATTACK_ON_HIT = effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap )

class Sharp( Enhancer ):
    NAMEPAT = "Sharp {0}"
    DESCPAT = "{0} It gives a +5% bonus to Critical Hit."
    PLUSRANK = 5
    AFFECTS = (SWORD, AXE, POLEARM, FARMTOOL)
    BONUSES = stats.StatMod({ stats.CRITICAL_HIT: 5 })

class RuneWeapon( Enhancer ):
    NAMEPAT = "Rune {0}"
    DESCPAT = "{0} Its mystic sigils add 1d8 dark damage and protect its user against spells."
    PLUSRANK = 5
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, BOW, SLING)
    ATTACK_ON_HIT = effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion )
    BONUSES = stats.StatMod({ stats.MAGIC_DEFENSE: 5 })

class HolyWeapon( Enhancer ):
    NAMEPAT = "Holy {0}"
    DESCPAT = "{0} It does an extra 1d8 holy damage and disrupts unholy creatures."
    PLUSRANK = 6
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, BOW, SLING)
    ATTACK_ON_HIT = effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion, on_success= (
        effects.TargetIs( effects.UNHOLY, on_true=(
            effects.OpposedRoll( att_stat=stats.PIETY, att_modifier=-20, on_success=(
                effects.InstaKill( anim=animobs.CriticalHit )
            ,), on_failure=(
                effects.OpposedRoll( on_success = (
                    effects.Paralyze( max_duration = 3 )
                ,)
            ,),)
        ,) ) 
        ),))
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.RESIST_LUNAR: 10 })

class Vorpal( Enhancer ):
    NAMEPAT = "Vorpal {0}"
    DESCPAT = "{0} It gives a +10% bonus to Critical Hit."
    PLUSRANK = 10
    AFFECTS = (SWORD, AXE, POLEARM, FARMTOOL)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.CRITICAL_HIT: 10 })

#  ****************
#  ***   AMMO   ***
#  ****************

class BurningAmmo( Enhancer ):
    NAMEPAT = "Burning {0}"
    DESCPAT = "{0} They ignite for an extra 1d4 fire damage."
    PLUSRANK = 1
    AFFECTS = (ARROW,BULLET)
    ATTACK_ON_HIT = effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )

class FreezingAmmo( Enhancer ):
    NAMEPAT = "Freezing {0}"
    DESCPAT = "{0} They do an extra 1d4 cold damage and may freeze their target in place."
    PLUSRANK = 2
    AFFECTS = (ARROW,BULLET)
    ATTACK_ON_HIT = effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.BlueExplosion, on_success= (
        effects.OpposedRoll( att_modifier=-20, on_success = (
            effects.Paralyze( max_duration = 3 )
        ,) )
    ,) )


#  *******************************
#  ***   ARMOR  ENHANCEMENTS   ***
#  *******************************

class FineArmor( Enhancer ):
    NAMEPAT = "Fine {0}"
    DESCPAT = "{0} It has been enhanced to provide an additional +5% to defense."
    PLUSRANK = 1
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class ShinyArmor( Enhancer ):
    NAMEPAT = "Shiny {0}"
    DESCPAT = "{0} It provides an additional +5% to aura and defense."
    PLUSRANK = 3
    AFFECTS = (HEAVY_ARMOR,)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.MAGIC_DEFENSE: 5 })

class FireArmor( Enhancer ):
    NAMEPAT = "Fire {0}"
    DESCPAT = "{0} It provides 25% protection against fire."
    PLUSRANK = 4
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, SHIELD)
    BONUSES = stats.StatMod({ stats.RESIST_FIRE:25 })

class ColdArmor( Enhancer ):
    NAMEPAT = "Cold {0}"
    DESCPAT = "{0} It provides 25% protection against cold."
    PLUSRANK = 4
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, SHIELD)
    BONUSES = stats.StatMod({ stats.RESIST_COLD:25 })

class AcidArmor( Enhancer ):
    NAMEPAT = "Acid {0}"
    DESCPAT = "{0} It provides 25% protection against acid."
    PLUSRANK = 4
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, SHIELD)
    BONUSES = stats.StatMod({ stats.RESIST_ACID:25 })

class LightningArmor( Enhancer ):
    NAMEPAT = "Lightning {0}"
    DESCPAT = "{0} It provides 25% protection against lightning."
    PLUSRANK = 4
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, SHIELD)
    BONUSES = stats.StatMod({ stats.RESIST_LIGHTNING:25 })

class SturdyArmor( Enhancer ):
    NAMEPAT = "Sturdy {0}"
    DESCPAT = "{0} It has been reinforced to give an extra +10% to defense."
    PLUSRANK = 5
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10, stats.NATURAL_DEFENSE: 10 })

class WardedArmor( Enhancer ):
    NAMEPAT = "Warded {0}"
    DESCPAT = "{0} It is covered in protective runes which give +10% to aura."
    PLUSRANK = 5
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR)
    BONUSES = stats.StatMod({ stats.MAGIC_DEFENSE: 10 })

class ShadowArmor( Enhancer ):
    NAMEPAT = "Shadow {0}"
    DESCPAT = "{0} It has been enchanted to give +20% to stealth."
    PLUSRANK = 6
    AFFECTS = (CLOTHES, LIGHT_ARMOR)
    BONUSES = stats.StatMod({ stats.STEALTH: 20 })

class HeroicArmor( Enhancer ):
    NAMEPAT = "Heroic {0}"
    DESCPAT = "{0} Its intricate design boosts morale and charisma."
    PLUSRANK = 6
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR)
    BONUSES = stats.StatMod({ stats.CHARISMA: 2, stats.PHYSICAL_ATTACK: 5, stats.PHYSICAL_DEFENSE: 5, stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class InvulnerableArmor( Enhancer ):
    NAMEPAT = "Invulnerable {0}"
    DESCPAT = "{0} It provides 25% protection against slashing, piercing, and crushing attacks."
    PLUSRANK = 7
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, SHIELD)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5, stats.RESIST_SLASHING:25, stats.RESIST_CRUSHING:25, stats.RESIST_PIERCING:25 })

class RuneArmor( Enhancer ):
    NAMEPAT = "Rune {0}"
    DESCPAT = "{0} Protective runes give +10% to defense and aura, while also reducing both dark and holy damage."
    PLUSRANK = 8
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10, stats.NATURAL_DEFENSE: 10, stats.MAGIC_DEFENSE: 10, stats.RESIST_SOLAR: 25, stats.RESIST_LUNAR: 25 })


#  ********************************
#  ***   SHIELD  ENHANCEMENTS   ***
#  ********************************

class SturdyShield( Enhancer ):
    NAMEPAT = "Sturdy {0}"
    DESCPAT = "{0} It is reinforced to provide an additional +5% to defense."
    PLUSRANK = 2
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })

class ShinyShield( Enhancer ):
    NAMEPAT = "Shiny {0}"
    DESCPAT = "{0} It provides an additional +5% to aura and defense."
    PLUSRANK = 3
    AFFECTS = (HEAVY_ARMOR,)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.MAGIC_DEFENSE: 5 })

class ElementalShield( Enhancer ):
    NAMEPAT = "Elemental {0}"
    DESCPAT = "{0} It has been warded to provide 20% protection against fire, cold, lightning, and acid."
    PLUSRANK = 8
    AFFECTS = (SHIELD,)
    BONUSES = stats.StatMod({ stats.RESIST_FIRE:20, stats.RESIST_COLD: 20, stats.RESIST_LIGHTNING: 20, stats.RESIST_ACID: 20 })

#  *******************************
#  ***   CLOAK  ENHANCEMENTS   ***
#  *******************************

class DefenseCloak( Enhancer ):
    NAMEPAT = "{1} of Defense"
    DESCPAT = "{0} It has been enhanced to provide +5% to defense."
    PLUSRANK = 2
    AFFECTS = (CLOAK,)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class ElvenCloak( Enhancer ):
    NAMEPAT = "Elven {0}"
    DESCPAT = "{0} Its fine construction provides a +5% bonus to aura and stealth."
    PLUSRANK = 3
    AFFECTS = (CLOAK,)
    BONUSES = stats.StatMod({ stats.MAGIC_DEFENSE: 5, stats.STEALTH: 5 })

class HealthCloak( Enhancer ):
    NAMEPAT = "{1} of Health"
    DESCPAT = "{0} It provides a +2 bonus to toughness."
    PLUSRANK = 5
    AFFECTS = (CLOAK,CLOTHES)
    BONUSES = stats.StatMod({ stats.TOUGHNESS:2 })

class ProtectionCloak( Enhancer ):
    NAMEPAT = "{1} of Protection"
    DESCPAT = "{0} It has been warded to provide 20% protection against fire, cold, lightning, and acid."
    PLUSRANK = 7
    AFFECTS = (CLOAK,)
    BONUSES = stats.StatMod({ stats.RESIST_FIRE:20, stats.RESIST_COLD: 20, stats.RESIST_LIGHTNING: 20, stats.RESIST_ACID: 20 })

#  ********************
#  ***   HEADGEAR   ***
#  ********************

class AwareHat( Enhancer ):
    NAMEPAT = "{1} of Awareness"
    DESCPAT = "{0} It provides a +20% bonus to awareness."
    PLUSRANK = 2
    AFFECTS = (HAT,HELM)
    BONUSES = stats.StatMod({ stats.AWARENESS:20 })

class SmartHat( Enhancer ):
    NAMEPAT = "{1} of Intelligence"
    DESCPAT = "{0} It provides a +2 bonus to intelligence."
    PLUSRANK = 5
    AFFECTS = (HAT,HELM)
    BONUSES = stats.StatMod({ stats.INTELLIGENCE:2 })

class PiousHat( Enhancer ):
    NAMEPAT = "{1} of Faith"
    DESCPAT = "{0} It provides a +2 bonus to piety."
    PLUSRANK = 5
    AFFECTS = (HAT,HELM)
    BONUSES = stats.StatMod({ stats.PIETY:2 })

class SturdyHat( Enhancer ):
    NAMEPAT = "Sturdy {0}"
    DESCPAT = "{0} It is reinforced to provide an additional +5% to defense."
    PLUSRANK = 6
    AFFECTS = (HAT,HELM)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })


#  **********************************
#  ***   GLOVES  AND  GAUNTLETS   ***
#  **********************************

class PunchingGlove( Enhancer ):
    NAMEPAT = "{1} of Punching"
    DESCPAT = "{0} They provide a +5% bonus to kung fu."
    PLUSRANK = 3
    AFFECTS = (GLOVE,)
    BONUSES = stats.StatMod({ stats.KUNG_FU:5 })

class StrengthGlove( Enhancer ):
    NAMEPAT = "{1} of Might"
    DESCPAT = "{0} They provide a +2 bonus to strength."
    PLUSRANK = 5
    AFFECTS = (GLOVE,GAUNTLET)
    BONUSES = stats.StatMod({ stats.STRENGTH:2 })

class SturdyGlove( Enhancer ):
    NAMEPAT = "Sturdy {0}"
    DESCPAT = "{0} They are reinforced to provide an additional +5% to defense."
    PLUSRANK = 6
    AFFECTS = (GLOVE,GAUNTLET)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })

class AlchemicalGlove( Enhancer ):
    NAMEPAT = "Alchemical {0}"
    DESCPAT = "{0} They reduce acid damage by 25%."
    PLUSRANK = 7
    AFFECTS = (GLOVE,GAUNTLET)
    BONUSES = stats.StatMod({ stats.RESIST_ACID: 25 })

class ForgeGlove( Enhancer ):
    NAMEPAT = "Forge {0}"
    DESCPAT = "{0} They reduce fire damage by 25%."
    PLUSRANK = 7
    AFFECTS = (GLOVE,GAUNTLET)
    BONUSES = stats.StatMod({ stats.RESIST_FIRE: 25 })


#  ********************
#  ***   FOOTWEAR   ***
#  ********************

class KickingShoe( Enhancer ):
    NAMEPAT = "{1} of Kicking"
    DESCPAT = "{0} They provide a +5% bonus to kung fu."
    PLUSRANK = 3
    AFFECTS = (SHOES,SANDALS,BOOTS)
    BONUSES = stats.StatMod({ stats.KUNG_FU:5 })

class SilenceShoe( Enhancer ):
    NAMEPAT = "Silent {1}"
    DESCPAT = "{0} They provide a +5% bonus to stealth."
    PLUSRANK = 4
    AFFECTS = (SHOES,SANDALS,BOOTS)
    BONUSES = stats.StatMod({ stats.STEALTH:5 })

class ReflexShoe( Enhancer ):
    NAMEPAT = "{1} of Speed"
    DESCPAT = "{0} They provide a +2 bonus to reflexes."
    PLUSRANK = 5
    AFFECTS = (SHOES,SANDALS,BOOTS)
    BONUSES = stats.StatMod({ stats.REFLEXES:2 })

class RubberSoledShoe( Enhancer ):
    NAMEPAT = "Rubber Soled {1}"
    DESCPAT = "{0} They provide 25% resistance to lightning."
    PLUSRANK = 6
    AFFECTS = (SHOES,SANDALS,BOOTS)
    BONUSES = stats.StatMod({ stats.RESIST_LIGHTNING:25 })

class WinterShoe( Enhancer ):
    NAMEPAT = "Winter {1}"
    DESCPAT = "{0} They provide 25% resistance to cold."
    PLUSRANK = 6
    AFFECTS = (SHOES,BOOTS)
    BONUSES = stats.StatMod({ stats.RESIST_COLD:25 })


#  ***********************************
#  ***   HOLYSYMBOLS  AND  WANDS   ***
#  ***********************************

class Evoca( Enhancer ):
    NAMEPAT = "Evoca {0}"
    DESCPAT = "{0} It aids spellcasting, providing +5% to magic."
    PLUSRANK = 4
    AFFECTS = (WAND,HOLYSYMBOL)
    BONUSES = stats.StatMod({ stats.MAGIC_ATTACK: 5 })

class Ajura( Enhancer ):
    NAMEPAT = "Ajura {0}"
    DESCPAT = "{0} It aids counterspells, providing +5% to aura."
    PLUSRANK = 3
    AFFECTS = (WAND,HOLYSYMBOL)
    BONUSES = stats.StatMod({ stats.MAGIC_DEFENSE: 5 })


#  *************************
#  ***   MISCELLANEOUS   ***
#  *************************

class Lucky( Enhancer ):
    NAMEPAT = "Lucky {0}"
    DESCPAT = "{0} It provides an additional +5% to aura and defense."
    PLUSRANK = 5
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, BOW, SHIELD, \
        SLING, CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, HAT, HELM, GLOVE, \
        GAUNTLET, SANDALS, SHOES, BOOTS, CLOAK, HOLYSYMBOL, WAND, FARMTOOL)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5, stats.MAGIC_DEFENSE: 5 })



