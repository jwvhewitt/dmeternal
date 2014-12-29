#
# Contains magical or other effects that get attached to items.
#

import stats
import effects
import animobs
from . import SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, BOW, ARROW, SHIELD, \
    SLING, BULLET, CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, HAT, HELM, GLOVE, GAUNTLET, \
    SANDALS, SHOES, BOOTS, CLOAK, HOLYSYMBOL, WAND, FARMTOOL, LANCE
import enchantments
import spells
import invocations
import targetarea

class Enhancer( object ):
    NAMEPAT = "Enhanced {0}"
    DESCPAT = "{0}"
    PLUSRANK = 2
    AFFECTS = ()
    BONUSES = stats.StatMod()
    # Attack Enhancements- for weapons & ammo only
    ATTACK_ON_HIT = None
    # Techniques- list of invocations
    TECH = ()
    def get_name( self, it ):
        return self.NAMEPAT.format( it.true_name, it.itemtype.name )
    def cost( self ):
        return 250 * self.PLUSRANK

#  ********************************
#  ***   WEAPON  ENHANCEMENTS   ***
#  ********************************

class ProtectionStaff( Enhancer ):
    NAMEPAT = "{0} of Protection"
    DESCPAT = "{0} It allows its user to cast Shield of Wind in combat."
    PLUSRANK = 1
    AFFECTS = (STAFF,WAND)
    TECH = (spells.airspells.AIR_ARMOR,)

class BlessingStaff( Enhancer ):
    NAMEPAT = "{0} of Blessing"
    DESCPAT = "{0} It allows its user to cast Blessing in combat."
    PLUSRANK = 1
    AFFECTS = (STAFF,WAND)
    TECH = (spells.solarspells.BLESSING,)

class CursingStaff( Enhancer ):
    NAMEPAT = "{0} of Cursing"
    DESCPAT = "{0} It allows its user to cast Curse in combat."
    PLUSRANK = 1
    AFFECTS = (STAFF,WAND)
    TECH = (spells.lunarspells.CURSE,)

class OrcishWeapon( Enhancer ):
    NAMEPAT = "Orcish {0}"
    DESCPAT = "{0} Its heavy construction does an extra 1d3 crushing damage."
    PLUSRANK = 1
    AFFECTS = (SWORD, DAGGER, POLEARM, FARMTOOL)
    ATTACK_ON_HIT = effects.HealthDamage( (1,3,0), stat_bonus=None, element=stats.RESIST_CRUSHING, anim=animobs.BloodSplat )
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: -5 })

class DwarvenWeapon( Enhancer ):
    NAMEPAT = "Dwarven {0}"
    DESCPAT = "{0} Its fine craftsmanship provides +5% to attack."
    PLUSRANK = 1
    AFFECTS = (SWORD, MACE, POLEARM, STAFF)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5 })

class ElvenWeapon( Enhancer ):
    NAMEPAT = "Elven {0}"
    DESCPAT = "{0} It has been balanced for parrying, providing +5% to defense."
    PLUSRANK = 1
    AFFECTS = (SWORD,DAGGER,STAFF,LANCE)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class ElvenBow( Enhancer ):
    NAMEPAT = "Elven {0}"
    DESCPAT = "{0} Its elegant craftsmanship provides +5% to attack."
    PLUSRANK = 1
    AFFECTS = (BOW,)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5 })

class HurthlingSling( Enhancer ):
    NAMEPAT = "Hurthling {0}"
    DESCPAT = "{0} It gives +5% to attack."
    PLUSRANK = 1
    AFFECTS = (SLING,)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5 })

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
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, BOW, SLING, LANCE)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 10 })

class Balanced( Enhancer ):
    NAMEPAT = "Balanced {0}"
    DESCPAT = "{0} It is balanced to give +5% attack and +5% defense."
    PLUSRANK = 2
    AFFECTS = (SWORD, DAGGER, STAFF)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class HealingStaff( Enhancer ):
    NAMEPAT = "{0} of Healing"
    DESCPAT = "{0} It allows its user to cast Minor Cure."
    PLUSRANK = 2
    AFFECTS = (STAFF,WAND)
    TECH = (spells.solarspells.MINOR_CURE,)

class DreadWeapon( Enhancer ):
    NAMEPAT = "Dread {0}"
    DESCPAT = "{0} Targets struck by this weapon may find themselves cursed."
    PLUSRANK = 2
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, BOW, SLING)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5 })
    ATTACK_ON_HIT = effects.Enchant( enchantments.CurseEn, anim=animobs.PurpleSparkle )

class Lockpick( Enhancer ):
    NAMEPAT = "Lockpick {0}"
    DESCPAT = "{0} It contains tools which give +15% to disarm traps."
    PLUSRANK = 2
    AFFECTS = (DAGGER,SWORD)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.DISARM_TRAPS: 15 })

class Smasher( Enhancer ):
    NAMEPAT = "{1} of Smashing"
    DESCPAT = "{0} It does extra damage to constructs."
    PLUSRANK = 3
    AFFECTS = (AXE, MACE, STAFF)
    ATTACK_ON_HIT = effects.TargetIs( effects.CONSTRUCT, on_true=(
            effects.HealthDamage( (2,4,0), stat_bonus=None, element=stats.RESIST_ATOMIC, anim=animobs.EarthBoom )
        ,))
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5 })

class HarvestWeapon( Enhancer ):
    NAMEPAT = "{0} of Harvest"
    DESCPAT = "{0} It does extra damage to plants."
    PLUSRANK = 3
    AFFECTS = (SWORD, AXE, STAFF, POLEARM, FARMTOOL)
    ATTACK_ON_HIT = effects.TargetIs( effects.PLANT, on_true=(
            effects.HealthDamage( (2,4,0), stat_bonus=None, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion )
        ,))
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5 })

class SpiteWeapon( Enhancer ):
    NAMEPAT = "{0} of Spite"
    DESCPAT = "{0} It gives a +15% bonus to Counter Attack."
    PLUSRANK = 3
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, LANCE)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.COUNTER_ATTACK: 15 })

class Blessed( Enhancer ):
    NAMEPAT = "Blessed {0}"
    DESCPAT = "{0} This weapon does extra damage to unholy creatures."
    PLUSRANK = 3
    AFFECTS = (SWORD, MACE, STAFF, POLEARM, LANCE)
    ATTACK_ON_HIT = effects.TargetIs( effects.UNHOLY, on_true=(
            effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
        ,))
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.MAGIC_DEFENSE: 5 })

class GoldenWeapon( Enhancer ):
    NAMEPAT = "Golden {0}"
    DESCPAT = "{0} It gives a +15% bonus to Looting."
    PLUSRANK = 3
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, LANCE, BOW, SLING)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.LOOTING: 15 })

class NatureStaff( Enhancer ):
    NAMEPAT = "{0} of Nature"
    DESCPAT = "{0} It allows its user to cast Call Animal."
    PLUSRANK = 3
    AFFECTS = (STAFF,)
    TECH = ( spells.druidspells.CALL_ANIMAL, )
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.MAGIC_DEFENSE: 5 })

class NightStaff( Enhancer ):
    NAMEPAT = "{0} of Night"
    DESCPAT = "{0} It allows its user to cast Sleep and Wizard Missile."
    PLUSRANK = 4
    AFFECTS = (STAFF,)
    TECH = ( spells.lunarspells.SLEEP, spells.lunarspells.WIZARD_MISSILE )
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.MAGIC_DEFENSE: 5 })

class Flaming( Enhancer ):
    NAMEPAT = "Flaming {0}"
    DESCPAT = "{0} It glows with magical fire that does an extra 1d6 damage."
    PLUSRANK = 4
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, LANCE)
    ATTACK_ON_HIT = effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )

class Frost( Enhancer ):
    NAMEPAT = "Frost {0}"
    DESCPAT = "{0} It shimmers with magical cold that does an extra 1d6 damage."
    PLUSRANK = 4
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, LANCE)
    ATTACK_ON_HIT = effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.BlueExplosion )

class Slimy( Enhancer ):
    NAMEPAT = "Slimy {0}"
    DESCPAT = "{0} It does an extra 1d6 acid damage."
    PLUSRANK = 4
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, LANCE)
    ATTACK_ON_HIT = effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )

class Shocking( Enhancer ):
    NAMEPAT = "Shocking {0}"
    DESCPAT = "{0} It calls magical lightning that does an extra 1d6 damage."
    PLUSRANK = 4
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, LANCE)
    ATTACK_ON_HIT = effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap )

class Sharp( Enhancer ):
    NAMEPAT = "Sharp {0}"
    DESCPAT = "{0} It gives a +5% bonus to Critical Hit."
    PLUSRANK = 4
    AFFECTS = (SWORD, AXE, POLEARM, FARMTOOL)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.CRITICAL_HIT: 5 })

class ResistStaff( Enhancer ):
    NAMEPAT = "{0} of Resistance"
    DESCPAT = "{0} It allows its user to cast Resist Energy and Resist Elements."
    PLUSRANK = 5
    AFFECTS = (STAFF,)
    TECH = (spells.waterspells.RESIST_ENERGY,spells.waterspells.RESIST_ELEMENTS)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.MAGIC_DEFENSE: 10 })

class RuneWeapon( Enhancer ):
    NAMEPAT = "Rune {0}"
    DESCPAT = "{0} It crackles with eldritch fire, doing an extra 1d8 dark damage."
    PLUSRANK = 5
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM)
    ATTACK_ON_HIT = effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion )
    BONUSES = stats.StatMod({ stats.MAGIC_DEFENSE: 5 })

class RuneBow( Enhancer ):
    NAMEPAT = "Rune {0}"
    DESCPAT = "{0} It crackles with eldritch power, shielding its user from harm."
    PLUSRANK = 5
    AFFECTS = (BOW, SLING)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 10, stats.MAGIC_DEFENSE: 10,
     stats.PHYSICAL_DEFENSE: 10, stats.NATURAL_DEFENSE: 10 })
    TECH = (spells.lunarspells.WIZARD_MISSILE,)

class HolyWeapon( Enhancer ):
    NAMEPAT = "Holy {0}"
    DESCPAT = "{0} It does an extra 1d8 holy damage and disrupts unholy creatures."
    PLUSRANK = 6
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, LANCE)
    ATTACK_ON_HIT = effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion, on_success= (
        effects.TargetIs( effects.UNHOLY, on_true=(
            effects.OpposedRoll( att_stat=stats.PIETY, att_modifier=-20, on_success=(
                effects.InstaKill( anim=animobs.CriticalHit )
            ,), on_failure=(
                effects.OpposedRoll( on_success = (
                    effects.Paralyze( max_duration = 3 )
                ,)
            ,),)
        ), ) 
        ),))
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.RESIST_LUNAR: 25 })

class HolyBow( Enhancer ):
    NAMEPAT = "Holy {0}"
    DESCPAT = "{0} A hit from this weapon may disrupt unholy creatures."
    PLUSRANK = 6
    AFFECTS = (BOW, SLING)
    ATTACK_ON_HIT = effects.TargetIs( effects.UNHOLY, on_true=(
            effects.OpposedRoll( att_stat=stats.PIETY, att_modifier=-10, on_success=(
                effects.InstaKill( anim=animobs.CriticalHit )
            ,), on_failure=(
                effects.OpposedRoll( att_modifier=10, on_success = (
                    effects.Paralyze( max_duration = 3 )
                ,)
            ,),)
        ,), ) )
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 10, stats.RESIST_LUNAR: 25 })

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

class BlessedAmmo( Enhancer ):
    NAMEPAT = "Blessed {0}"
    DESCPAT = "{0} They do extra damage to unholy creatures."
    PLUSRANK = 2
    AFFECTS = (ARROW, BULLET)
    ATTACK_ON_HIT = effects.TargetIs( effects.UNHOLY, on_true=(
            effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
        ,))

class AcidAmmo( Enhancer ):
    NAMEPAT = "Acid {0}"
    DESCPAT = "{0} They do an extra 1d6 acid damage."
    PLUSRANK = 3
    AFFECTS = (ARROW,BULLET)
    ATTACK_ON_HIT = effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )

class SleepySand( Enhancer ):
    NAMEPAT = "Sleepysand {0}"
    DESCPAT = "{0} They may put the target to sleep."
    PLUSRANK = 3
    AFFECTS = (BULLET,)
    ATTACK_ON_HIT = effects.TargetIs( pat=effects.ANIMAL, on_true = (
        effects.OpposedRoll( att_modifier=50, on_success = (
            effects.CauseSleep(),
        )),))


#  *******************************
#  ***   ARMOR  ENHANCEMENTS   ***
#  *******************************

class FineArmor( Enhancer ):
    NAMEPAT = "Fine {0}"
    DESCPAT = "{0} It has been enhanced to provide an additional +5% to defense."
    PLUSRANK = 1
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class FireArmor( Enhancer ):
    NAMEPAT = "Flame {0}"
    DESCPAT = "{0} It provides 25% protection against fire."
    PLUSRANK = 2
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, SHIELD)
    BONUSES = stats.StatMod({ stats.RESIST_FIRE:25, stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class ColdArmor( Enhancer ):
    NAMEPAT = "Ice {0}"
    DESCPAT = "{0} It provides 25% protection against cold."
    PLUSRANK = 2
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, SHIELD)
    BONUSES = stats.StatMod({ stats.RESIST_COLD:25, stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class AcidArmor( Enhancer ):
    NAMEPAT = "Acid {0}"
    DESCPAT = "{0} It provides 25% protection against acid."
    PLUSRANK = 2
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, SHIELD)
    BONUSES = stats.StatMod({ stats.RESIST_ACID:25, stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class LightningArmor( Enhancer ):
    NAMEPAT = "Lightning {0}"
    DESCPAT = "{0} It provides 25% protection against lightning."
    PLUSRANK = 2
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, SHIELD)
    BONUSES = stats.StatMod({ stats.RESIST_LIGHTNING:25, stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class ShadowArmor( Enhancer ):
    NAMEPAT = "Shadow {0}"
    DESCPAT = "{0} It has been enchanted to give +10% to stealth."
    PLUSRANK = 3
    AFFECTS = (CLOTHES, LIGHT_ARMOR)
    BONUSES = stats.StatMod({ stats.STEALTH: 10, stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class ShinyArmor( Enhancer ):
    NAMEPAT = "Shiny {0}"
    DESCPAT = "{0} It provides an additional +5% to aura and defense."
    PLUSRANK = 3
    AFFECTS = (HEAVY_ARMOR,)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.MAGIC_DEFENSE: 5 })

class SturdyArmor( Enhancer ):
    NAMEPAT = "Sturdy {0}"
    DESCPAT = "{0} It has been reinforced to give an extra +10% to defense."
    PLUSRANK = 4
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10, stats.NATURAL_DEFENSE: 10 })

class WardedArmor( Enhancer ):
    NAMEPAT = "Warded {0}"
    DESCPAT = "{0} It is covered in protective sigils which give +10% to aura."
    PLUSRANK = 5
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR)
    BONUSES = stats.StatMod({ stats.MAGIC_DEFENSE: 10, stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

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
    DESCPAT = "{0} Protective runes give +10% to defense and aura, while also protecting against both dark and holy damage."
    PLUSRANK = 8
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10, stats.NATURAL_DEFENSE: 10, stats.MAGIC_DEFENSE: 10, stats.RESIST_SOLAR: 25, stats.RESIST_LUNAR: 25 })


#  ********************************
#  ***   SHIELD  ENHANCEMENTS   ***
#  ********************************

class SturdyShield( Enhancer ):
    NAMEPAT = "Sturdy {0}"
    DESCPAT = "{0} It is reinforced to provide an additional +5% to defense."
    PLUSRANK = 1
    AFFECTS = (SHIELD,)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })

class ShieldOfBashing( Enhancer ):
    NAMEPAT = "{0} of Bashing"
    DESCPAT = "{0} It may be used to bash enemies, doing 2d6 damage and potentially stunning them."
    PLUSRANK = 2
    AFFECTS = (SHIELD,)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })
    TECH = ( invocations.MPInvocation( "Shield Bash",
        effects.PhysicalAttackRoll( att_stat=stats.STRENGTH, on_success = (
            effects.HealthDamage( (2,6,0), stat_bonus=stats.STRENGTH, element=stats.RESIST_CRUSHING, stat_mod=2, anim=animobs.RedBoom ),
            effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, def_stat=stats.TOUGHNESS, on_success = ( 
                effects.Paralyze( max_duration = 3 ),
            ))
        ,), on_failure = (
            effects.NoEffect( anim=animobs.SmallBoom )
        ,) ), com_tar=targetarea.SingleTarget(reach=1),ai_tar=invocations.TargetEnemy(),mp_cost=3
      ), )

class ShinyShield( Enhancer ):
    NAMEPAT = "Shiny {0}"
    DESCPAT = "{0} It provides an additional +5% to aura and defense."
    PLUSRANK = 3
    AFFECTS = (SHIELD,)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.MAGIC_DEFENSE: 5 })

class ResistShield( Enhancer ):
    NAMEPAT = "{0} of Resistance"
    DESCPAT = "{0} It allows its user to cast Resist Energy."
    PLUSRANK = 3
    AFFECTS = (SHIELD,HOLYSYMBOL)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })
    TECH = (spells.waterspells.RESIST_ENERGY,)

class ResilentShield( Enhancer ):
    NAMEPAT = "{0} of Resilence"
    DESCPAT = "{0} It provides a +2 bonus to toughness."
    PLUSRANK = 4
    AFFECTS = (SHIELD,)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.TOUGHNESS:2 })

class ElementalShield( Enhancer ):
    NAMEPAT = "Elemental {0}"
    DESCPAT = "{0} It has been warded to provide 20% protection against fire, cold, lightning, and acid."
    PLUSRANK = 5
    AFFECTS = (SHIELD,)
    BONUSES = stats.StatMod({ stats.RESIST_FIRE:20, stats.RESIST_COLD: 20, stats.RESIST_LIGHTNING: 20, stats.RESIST_ACID: 20 })

#  *******************************
#  ***   CLOAK  ENHANCEMENTS   ***
#  *******************************

class DefenseCloak( Enhancer ):
    NAMEPAT = "{0} of Defense"
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

class HealthCloak( Enhancer ):
    NAMEPAT = "{0} of Health"
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
    DESCPAT = "{0} It provides a +20% bonus to awareness and allows use of the Probe spell."
    PLUSRANK = 2
    AFFECTS = (HAT,HELM)
    BONUSES = stats.StatMod({ stats.AWARENESS:20 })
    TECH = (spells.airspells.PROBE,)

class TrickHat( Enhancer ):
    NAMEPAT = "{0} of Tricks"
    DESCPAT = "{0} Critters may be magically summoned from the hat."
    PLUSRANK = 3
    AFFECTS = (HAT,)
    TECH = (spells.earthspells.CALL_CRITTER,)

class SturdyHat( Enhancer ):
    NAMEPAT = "Sturdy {0}"
    DESCPAT = "{0} It is reinforced to provide an additional +5% to defense."
    PLUSRANK = 4
    AFFECTS = (HAT,HELM)
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

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



#  **********************************
#  ***   GLOVES  AND  GAUNTLETS   ***
#  **********************************

class HandyGlove( Enhancer ):
    NAMEPAT = "Handy {0}"
    DESCPAT = "{0} They provide a +10% bonus to disarm traps."
    PLUSRANK = 1
    AFFECTS = (GLOVE,GAUNTLET)
    BONUSES = stats.StatMod({ stats.DISARM_TRAPS:10 })

class PunchingGlove( Enhancer ):
    NAMEPAT = "{1} of Punching"
    DESCPAT = "{0} They provide a +5% bonus to kung fu."
    PLUSRANK = 2
    AFFECTS = (GLOVE,)
    BONUSES = stats.StatMod({ stats.KUNG_FU:5 })

class SpikyGlove( Enhancer ):
    NAMEPAT = "Spiky {0}"
    DESCPAT = "{0} They provide a +5% bonus to attack."
    PLUSRANK = 3
    AFFECTS = (GLOVE,GAUNTLET)
    BONUSES = stats.StatMod({ stats.PHYSICAL_ATTACK: 5 })

class SpellcraftGlove( Enhancer ):
    NAMEPAT = "{1} of Spellcraft"
    DESCPAT = "{0} They provide a +5% bonus to magic."
    PLUSRANK = 3
    AFFECTS = (GLOVE,)
    BONUSES = stats.StatMod({ stats.MAGIC_ATTACK: 5 })

class FireGlove( Enhancer ):
    NAMEPAT = "{0} of Fire"
    DESCPAT = "{0} The user may project an arc of fire from the fingertips."
    PLUSRANK = 4
    AFFECTS = (GLOVE,GAUNTLET)
    BONUSES = stats.StatMod({ stats.RESIST_FIRE: 15 })
    TECH = ( invocations.Invocation( "Flamethrower",
        effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
            effects.HealthDamage( (2,5,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
        ,), on_failure = (
            effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
        ,) ), com_tar=targetarea.Cone(reach=4), ai_tar=invocations.TargetEnemy()
      ), )

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

class FleetShoe( Enhancer ):
    NAMEPAT = "Fleet {0}"
    DESCPAT = "{0} They provide a +5% bonus to natural defense."
    PLUSRANK = 1
    AFFECTS = (SANDALS,)
    BONUSES = stats.StatMod({ stats.NATURAL_DEFENSE:5 })

class SilenceShoe( Enhancer ):
    NAMEPAT = "Silent {1}"
    DESCPAT = "{0} They provide a +5% bonus to stealth."
    PLUSRANK = 2
    AFFECTS = (SHOES,SANDALS,BOOTS)
    BONUSES = stats.StatMod({ stats.STEALTH:5 })

class KickingShoe( Enhancer ):
    NAMEPAT = "{1} of Kicking"
    DESCPAT = "{0} They provide a +5% bonus to kung fu."
    PLUSRANK = 3
    AFFECTS = (SHOES,SANDALS,BOOTS)
    BONUSES = stats.StatMod({ stats.KUNG_FU:5 })

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

class Ajura( Enhancer ):
    NAMEPAT = "Ajura {0}"
    DESCPAT = "{0} It aids counterspells, providing +5% to aura."
    PLUSRANK = 3
    AFFECTS = (WAND,HOLYSYMBOL)
    BONUSES = stats.StatMod({ stats.MAGIC_DEFENSE: 5 })

class Evoca( Enhancer ):
    NAMEPAT = "Evoca {0}"
    DESCPAT = "{0} It aids spellcasting, providing +5% to magic."
    PLUSRANK = 4
    AFFECTS = (WAND,HOLYSYMBOL)
    BONUSES = stats.StatMod({ stats.MAGIC_ATTACK: 5 })


#  *************************
#  ***   MISCELLANEOUS   ***
#  *************************

class Lucky( Enhancer ):
    NAMEPAT = "Lucky {0}"
    DESCPAT = "{0} It provides an additional +5% to aura and defense."
    PLUSRANK = 5
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, BOW, SHIELD, \
        SLING, CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, HAT, HELM, GLOVE, \
        GAUNTLET, SANDALS, SHOES, BOOTS, CLOAK, HOLYSYMBOL, WAND, FARMTOOL, \
        LANCE )
    BONUSES = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5, stats.MAGIC_DEFENSE: 5 })



