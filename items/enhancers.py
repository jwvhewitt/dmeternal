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
import random

ENHANCEMENT_LIST = list()

# There are three Enhancer types:
#  ET_CRAFT is generally not magic, but refers to make of item.
#  ET_PRIMARY is a primary enchantment.
#  ET_SECONDARY may not be chosen as the primary enchantment.
# The secondary enchantment must be one step below the primary.
ET_CRAFT,ET_PRIMARY,ET_SECONDARY = 1,2,3

class Enhancer( object ):
    NAMEPAT = "Enhanced {0}"
    DESCPAT = "{0}"
    PLUSRANK = 2
    # Upranks- lists point costs of subsequent upgrades
    UPRANKS = ()
    # Upgrades- Dict of upgrades activated at particular ranks
    UPGRADES = {}
    AFFECTS = ()
    BONUSES_PER_RANK = stats.StatMod()
    TYPE = ET_CRAFT
    FREQUENCY = 10
    # Attack Enhancements- for weapons & ammo only
    ATTACK_ON_HIT = None
    # Techniques- list of invocations
    TECH = ()
    def __init__( self, item, points=1, primary=True ):
        # Determine the _rank of this enhancement.
        self._rank = 1
        points -= self.PLUSRANK
        self._secondary = None
        if primary and points > 0:
            s = select_enhancer( item, points, (self.TYPE+1,) )
            if s:
                self._secondary = s(item,points,False)
                points -= self._secondary.PLUSRANK
        # Spend any remaining points on upranks.
        self.spend_points( points )

    @classmethod
    def can_enchant( self, item, points=0 ):
        return ( self.PLUSRANK <= points ) and item.itemtype in self.AFFECTS
    def get_stat( self, stat ):
        it = self.BONUSES_PER_RANK.get(stat,0) * self._rank
        if self._secondary:
            it += self._secondary.get_stat( stat )
        return it
    def spend_points( self, points ):
        candidates = [self,]
        if self._secondary:
            candidates.append( self._secondary )
        while candidates and points > 0:
            a = random.choice( candidates )
            ok,points = a.upgrade(points)
            if not ok:
                candidates.remove( a )
        # Record leftover points for later.
        self.xp = points
    def upgrade( self, points ):
        """Upgrade this enhancer if possible; return a tuple telling whether an
            upgrade was applied and the number of points remaining."""
        opoints = points
        if self.can_be_upgraded() and points >= self.UPRANKS[self._rank-1]:
            points -= self.UPRANKS[self._rank-1]
            self.PLUSRANK += self.UPRANKS[self._rank-1]
            self._rank += 1
            # Apply the upgrade for this rank.
            ug = self.UPGRADES.get( self._rank )
            if ug:
                ug( self )
        return (opoints!=points,points)
    def can_be_upgraded( self ):
        """Return True if this enhancer still has intrinsic upgrades left."""
        return len( self.UPRANKS ) >= self._rank
    def get_name( self, it ):
        if self._secondary:
            basename = self._secondary.get_name(it)
            return self.NAMEPAT.format( basename, basename, self._rank )
        return self.NAMEPAT.format( it.true_name, it.itemtype.name, self._rank )
    def modify_desc( self, odesc ):
        if self._secondary:
            odesc = self._secondary.modify_desc(odesc)
        return self.DESCPAT.format( odesc )
    def cost( self ):
        return 250 * self.min_rank()
    def min_rank( self ):
        it = self.PLUSRANK
        if self._secondary:
            it += self._secondary.min_rank()
        return it
    def modify_attack( self, fx, pc ):
        pc.add_attack_enhancements( fx, self )
        if self._secondary:
            self._secondary.modify_attack( fx, pc )

class UpgradeTechnique( object ):
    """Add a new technique to the enhancer at this rank."""
    def __init__( self, tech, descpat = "{}" ):
        self.tech = tech
        self.descpat = descpat
    def __call__( self,enh):
        enh.TECH = list( enh.TECH ) + [self.tech,]
        enh.DESCPAT = self.descpat

class UpgradeAttack( object ):
    """Replace the ATTACK_ON_HIT of the enhancer at this rank."""
    def __init__( self, fx, descpat = "{}" ):
        self.fx = fx
        self.descpat = descpat
    def __call__( self,enh):
        enh.ATTACK_ON_HIT = self.fx
        enh.DESCPAT = self.descpat

def select_enhancer( item_to_enchant, points, etypes=(ET_CRAFT,ET_PRIMARY) ):
    elist = list()
    for e in ENHANCEMENT_LIST:
        if e.can_enchant(item_to_enchant,points) and e.TYPE in etypes:
            elist += [e,] * e.FREQUENCY
    if elist:
        return random.choice( elist )

#  ********************************
#  ***   WEAPON  ENHANCEMENTS   ***
#  ********************************

class MagicWeapon( Enhancer ):
    # The basic weapon enhancement.
    NAMEPAT = "{0} +{2}"
    PLUSRANK = 2
    UPRANKS = (1,2,3,5)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.WEAPON_DAMAGE_BONUS: 1 })
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, BOW, SLING, LANCE)
    TYPE = ET_PRIMARY
    FREQUENCY = 100

class ProtectionStaff( Enhancer ):
    NAMEPAT = "{0} of Protection"
    DESCPAT = "{0} It allows its user to cast Shield of Wind in combat."
    PLUSRANK = 1
    AFFECTS = (STAFF,WAND)
    TECH = (spells.airspells.AIR_ARMOR,)
    TYPE = ET_SECONDARY

class BlessingStaff( Enhancer ):
    NAMEPAT = "{0} of Blessing"
    DESCPAT = "{0} It allows its user to cast Blessing in combat."
    PLUSRANK = 1
    AFFECTS = (STAFF,WAND)
    TECH = (spells.solarspells.BLESSING,)
    TYPE = ET_SECONDARY

class CursingStaff( Enhancer ):
    NAMEPAT = "{0} of Cursing"
    DESCPAT = "{0} It allows its user to cast Curse in combat."
    PLUSRANK = 1
    AFFECTS = (STAFF,WAND)
    TECH = (spells.lunarspells.CURSE,)
    TYPE = ET_SECONDARY

class OrcishWeapon( Enhancer ):
    NAMEPAT = "Orcish {0}"
    DESCPAT = "{0} Its heavy construction does an extra 1d3 crushing damage."
    PLUSRANK = 1
    AFFECTS = (SWORD, DAGGER, POLEARM, FARMTOOL)
    ATTACK_ON_HIT = effects.HealthDamage( (1,3,0), stat_bonus=None, element=stats.RESIST_CRUSHING, anim=animobs.BloodSplat )
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_ATTACK: -5 })
    FREQUENCY = 4

class DwarvenWeapon( Enhancer ):
    NAMEPAT = "Dwarven {0}"
    DESCPAT = "{0} Its fine craftsmanship provides +5% to attack."
    PLUSRANK = 1
    AFFECTS = (SWORD, MACE, POLEARM, STAFF)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_ATTACK: 5 })
    FREQUENCY = 5

class ElvenWeapon( Enhancer ):
    NAMEPAT = "Elven {0}"
    DESCPAT = "{0} It has been balanced for parrying, providing +5% to defense."
    PLUSRANK = 1
    AFFECTS = (SWORD,DAGGER,STAFF,LANCE)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })
    FREQUENCY = 4

class ElvenBow( Enhancer ):
    NAMEPAT = "Elven {0}"
    DESCPAT = "{0} Its elegant craftsmanship provides +5% to attack."
    PLUSRANK = 1
    AFFECTS = (BOW,)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_ATTACK: 5 })

class HurthlingSling( Enhancer ):
    NAMEPAT = "Hurthling {0}"
    DESCPAT = "{0} It gives +5% to attack."
    PLUSRANK = 1
    AFFECTS = (SLING,)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_ATTACK: 5 })

class Defender( Enhancer ):
    NAMEPAT = "Defender {0}"
    DESCPAT = "{0} It has been enchanted to provide a bonus to defense."
    PLUSRANK = 1
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL)
    UPRANKS = (1,2,3,5)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })
    TYPE = ET_SECONDARY

class Seeker( Enhancer ):
    NAMEPAT = "Seeker {0}"
    DESCPAT = "{0} It has been enchanted to give +10% attack."
    PLUSRANK = 2
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, BOW, SLING, LANCE)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_ATTACK: 10 })
    TYPE = ET_SECONDARY

class Balanced( Enhancer ):
    NAMEPAT = "Balanced {0}"
    DESCPAT = "{0} It is balanced to aid both attack and defense."
    PLUSRANK = 2
    AFFECTS = (SWORD, DAGGER, STAFF)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })
    FREQUENCY = 1

class HealingStaff( Enhancer ):
    NAMEPAT = "{0} of Healing"
    DESCPAT = "{0} It allows its user to cast Minor Cure."
    PLUSRANK = 1
    AFFECTS = (STAFF,WAND)
    TECH = (spells.solarspells.MINOR_CURE,)
    TYPE = ET_SECONDARY

class DreadWeapon( Enhancer ):
    NAMEPAT = "Dread {0}"
    DESCPAT = "{0} Targets struck by this weapon may find themselves cursed."
    PLUSRANK = 1
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, BOW, SLING)
    ATTACK_ON_HIT = effects.Enchant( enchantments.CurseEn, anim=animobs.PurpleSparkle )
    TYPE = ET_SECONDARY

class Lockpick( Enhancer ):
    NAMEPAT = "Lockpick {0}"
    DESCPAT = "{0} It contains tools which give +15% to disarm traps."
    PLUSRANK = 1
    AFFECTS = (DAGGER,SWORD)
    BONUSES_PER_RANK = stats.StatMod({ stats.DISARM_TRAPS: 15 })
    TYPE = ET_SECONDARY

class Smasher( Enhancer ):
    NAMEPAT = "{1} of Smashing"
    DESCPAT = "{0} It does extra damage to constructs."
    PLUSRANK = 1
    AFFECTS = (AXE, MACE, STAFF)
    ATTACK_ON_HIT = effects.TargetIs( effects.CONSTRUCT, on_true=(
            effects.HealthDamage( (2,4,0), stat_bonus=None, element=stats.RESIST_ATOMIC, anim=animobs.EarthBoom )
        ,))
    TYPE = ET_SECONDARY

class HarvestWeapon( Enhancer ):
    NAMEPAT = "{0} of Harvest"
    DESCPAT = "{0} It does extra damage to plants."
    PLUSRANK = 1
    AFFECTS = (SWORD, AXE, STAFF, POLEARM, FARMTOOL)
    ATTACK_ON_HIT = effects.TargetIs( effects.PLANT, on_true=(
            effects.HealthDamage( (2,4,0), stat_bonus=None, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion )
        ,))
    TYPE = ET_SECONDARY

class SpiteWeapon( Enhancer ):
    NAMEPAT = "{0} of Spite"
    DESCPAT = "{0} It gives a bonus to Counter Attack."
    PLUSRANK = 1
    UPRANKS = (1,1,2,3)
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, LANCE)
    BONUSES_PER_RANK = stats.StatMod({ stats.COUNTER_ATTACK: 5 })
    TYPE = ET_SECONDARY

class Blessed( Enhancer ):
    NAMEPAT = "Anointed {0}"
    DESCPAT = "{0} This weapon does extra damage to unholy creatures."
    PLUSRANK = 1
    AFFECTS = (SWORD, MACE, STAFF, POLEARM, LANCE)
    ATTACK_ON_HIT = effects.TargetIs( effects.UNHOLY, on_true=(
            effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
        ,))
    BONUSES_PER_RANK = stats.StatMod({ stats.MAGIC_DEFENSE: 5 })
    TYPE = ET_SECONDARY

class GoldenWeapon( Enhancer ):
    NAMEPAT = "Golden {0}"
    DESCPAT = "{0} It gives a +15% bonus to Looting."
    PLUSRANK = 2
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, LANCE, BOW, SLING)
    BONUSES_PER_RANK = stats.StatMod({ stats.LOOTING: 15 })
    FREQUENCY = 2

class NatureStaff( Enhancer ):
    NAMEPAT = "{0} of Nature"
    DESCPAT = "{0} It allows its user to cast Call Animal."
    PLUSRANK = 2
    AFFECTS = (STAFF,)
    TECH = ( spells.druidspells.CALL_ANIMAL, )
    BONUSES_PER_RANK = stats.StatMod({ stats.MAGIC_DEFENSE: 5 })
    TYPE = ET_SECONDARY

class NightStaff( Enhancer ):
    NAMEPAT = "{0} of Night"
    DESCPAT = "{0} It allows its user to cast Sleep and Wizard Missile."
    PLUSRANK = 3
    AFFECTS = (STAFF,)
    TECH = ( spells.lunarspells.SLEEP, spells.lunarspells.WIZARD_MISSILE )
    BONUSES_PER_RANK = stats.StatMod({ stats.MAGIC_DEFENSE: 5 })
    TYPE = ET_SECONDARY

class Flaming( Enhancer ):
    NAMEPAT = "Flaming {0}"
    DESCPAT = "{0} It glows with magical fire that does an extra 1d6 damage."
    PLUSRANK = 3
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, LANCE)
    ATTACK_ON_HIT = effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )
    TYPE = ET_SECONDARY
    UPRANKS = (2,2)
    UPGRADES = { 2: UpgradeTechnique( spells.firespells.PYROTECHNICS, "{0} It glows with magical fire that does an extra 1d6 damage, and allows use of the Pyrotechnics spell."),
        3: UpgradeAttack( effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion,
             on_success=( effects.Enchant( enchantments.BurnLowEn ),) ),
            "{0} It glows with magical fire that burns continuously for 1d6 damage. It also allows use of the Pyrotechnics spell." )
        }

class Frost( Enhancer ):
    NAMEPAT = "Frost {0}"
    DESCPAT = "{0} It shimmers with magical cold that does an extra 1d6 damage."
    PLUSRANK = 3
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, LANCE)
    ATTACK_ON_HIT = effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.BlueExplosion )
    TYPE = ET_SECONDARY

class Slimy( Enhancer ):
    NAMEPAT = "Slimy {0}"
    DESCPAT = "{0} It does an extra 1d6 acid damage."
    PLUSRANK = 3
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, LANCE)
    ATTACK_ON_HIT = effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
    TYPE = ET_SECONDARY

class Shocking( Enhancer ):
    NAMEPAT = "Shocking {0}"
    DESCPAT = "{0} It calls magical lightning that does an extra 1d6 damage."
    PLUSRANK = 3
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM, FARMTOOL, LANCE)
    ATTACK_ON_HIT = effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap )
    TYPE = ET_SECONDARY

class Sharp( Enhancer ):
    NAMEPAT = "Sharp {0}"
    DESCPAT = "{0} It gives a bonus to Critical Hit."
    PLUSRANK = 3
    UPRANKS = (2,3,5,8,13)
    AFFECTS = (SWORD, AXE, POLEARM, FARMTOOL)
    BONUSES_PER_RANK = stats.StatMod({ stats.CRITICAL_HIT: 5 })
    TYPE = ET_SECONDARY

class ResistStaff( Enhancer ):
    NAMEPAT = "{0} of Resistance"
    DESCPAT = "{0} It allows its user to cast Resist Energy and Resist Elements."
    PLUSRANK = 3
    AFFECTS = (STAFF,)
    TECH = (spells.waterspells.RESIST_ENERGY,spells.waterspells.RESIST_ELEMENTS)
    BONUSES_PER_RANK = stats.StatMod({ stats.MAGIC_DEFENSE: 10 })
    TYPE = ET_SECONDARY

class RuneWeapon( Enhancer ):
    NAMEPAT = "Rune {0}"
    DESCPAT = "{0} It crackles with eldritch fire, doing an extra 1d8 dark damage."
    PLUSRANK = 4
    AFFECTS = (SWORD, AXE, MACE, DAGGER, STAFF, POLEARM)
    ATTACK_ON_HIT = effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion )
    BONUSES_PER_RANK = stats.StatMod({ stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 5 })
    TYPE = ET_SECONDARY
    UPRANKS = (2,3)

class HolyWeapon( Enhancer ):
    NAMEPAT = "Holy {0}"
    DESCPAT = "{0} It does an extra 1d8 holy damage and disrupts unholy creatures."
    PLUSRANK = 5
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
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_ATTACK: 5, stats.RESIST_LUNAR: 25 })
    TYPE = ET_SECONDARY

class HolyBow( Enhancer ):
    NAMEPAT = "Holy {0}"
    DESCPAT = "{0} A hit from this weapon may disrupt unholy creatures."
    PLUSRANK = 5
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
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_ATTACK: 10, stats.RESIST_LUNAR: 25 })
    TYPE = ET_SECONDARY

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
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class MagicArmor( Enhancer ):
    # The basic armor enhancement.
    NAMEPAT = "{0} +{2}"
    PLUSRANK = 2
    UPRANKS = (2,2,3,5)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5,
        stats.RESIST_CRUSHING: 10, stats.RESIST_PIERCING: 10, stats.RESIST_SLASHING: 10 })
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR )
    TYPE = ET_PRIMARY
    FREQUENCY = 100

class FireArmor( Enhancer ):
    NAMEPAT = "Flame {0}"
    DESCPAT = "{0} It provides protection against fire."
    PLUSRANK = 1
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, SHIELD)
    BONUSES_PER_RANK = stats.StatMod({ stats.RESIST_FIRE:25 })
    UPRANKS = (2,5)
    TYPE = ET_SECONDARY

class ColdArmor( Enhancer ):
    NAMEPAT = "Ice {0}"
    DESCPAT = "{0} It provides protection against cold."
    PLUSRANK = 2
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, SHIELD)
    BONUSES_PER_RANK = stats.StatMod({ stats.RESIST_COLD:25 })
    UPRANKS = (2,5)
    TYPE = ET_SECONDARY

class AcidArmor( Enhancer ):
    NAMEPAT = "Acid {0}"
    DESCPAT = "{0} It provides protection against acid."
    PLUSRANK = 2
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, SHIELD)
    BONUSES_PER_RANK = stats.StatMod({ stats.RESIST_ACID:25 })
    UPRANKS = (2,5)
    TYPE = ET_SECONDARY

class LightningArmor( Enhancer ):
    NAMEPAT = "Lightning {0}"
    DESCPAT = "{0} It provides protection against lightning."
    PLUSRANK = 2
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, SHIELD)
    BONUSES_PER_RANK = stats.StatMod({ stats.RESIST_LIGHTNING:25 })
    UPRANKS = (2,5)
    TYPE = ET_SECONDARY

class ShadowArmor( Enhancer ):
    NAMEPAT = "Shadow {0}"
    DESCPAT = "{0} It has been enchanted to give a bonus to stealth."
    PLUSRANK = 2
    AFFECTS = (CLOTHES, LIGHT_ARMOR)
    BONUSES_PER_RANK = stats.StatMod({ stats.STEALTH: 5 })
    UPRANKS = (1,2,3,5)
    TYPE = ET_SECONDARY

class ShinyArmor( Enhancer ):
    NAMEPAT = "Shiny {0}"
    DESCPAT = "{0} It provides a bonus to aura."
    PLUSRANK = 1
    AFFECTS = (HEAVY_ARMOR,)
    BONUSES_PER_RANK = stats.StatMod({ stats.MAGIC_DEFENSE: 5 })
    UPRANKS = (2,3,5,8)
    TYPE = ET_SECONDARY

class HeroicArmor( Enhancer ):
    NAMEPAT = "Heroic {0}"
    DESCPAT = "{0} Its intricate design boosts morale and charisma."
    PLUSRANK = 5
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR)
    BONUSES_PER_RANK = stats.StatMod({ stats.CHARISMA: 2, stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 5 })
    TYPE = ET_SECONDARY

class InvulnerableArmor( Enhancer ):
    NAMEPAT = "Invulnerable {0}"
    DESCPAT = "{0} It provides protection against slashing, piercing, and crushing attacks."
    PLUSRANK = 5
    AFFECTS = (CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, SHIELD)
    BONUSES_PER_RANK = stats.StatMod({ stats.RESIST_SLASHING:25, stats.RESIST_CRUSHING:25, stats.RESIST_PIERCING:25 })
    UPRANKS = (5,7)
    TYPE = ET_SECONDARY


#  ********************************
#  ***   SHIELD  ENHANCEMENTS   ***
#  ********************************

class MagicShield( Enhancer ):
    # The basic armor enhancement.
    NAMEPAT = "{0} +{2}"
    PLUSRANK = 2
    UPRANKS = (1,2,3,5)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, })
    AFFECTS = (SHIELD,)
    TYPE = ET_PRIMARY
    FREQUENCY = 100

class SturdyShield( Enhancer ):
    NAMEPAT = "Sturdy {0}"
    DESCPAT = "{0} It is reinforced to provide an additional +5% to defense."
    PLUSRANK = 2
    AFFECTS = (SHIELD,)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })

class ShieldOfBashing( Enhancer ):
    NAMEPAT = "{0} of Bashing"
    DESCPAT = "{0} It may be used to bash enemies, doing 2d6 damage and potentially stunning them."
    PLUSRANK = 2
    AFFECTS = (SHIELD,)
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
    TYPE = ET_SECONDARY

class ShinyShield( Enhancer ):
    NAMEPAT = "Shiny {0}"
    DESCPAT = "{0} It provides a bonus to aura."
    PLUSRANK = 1
    AFFECTS = (SHIELD,)
    BONUSES_PER_RANK = stats.StatMod({ stats.MAGIC_DEFENSE: 5 })

class ResistShield( Enhancer ):
    NAMEPAT = "{0} of Resistance"
    DESCPAT = "{0} It allows its user to cast Resist Energy."
    PLUSRANK = 1
    AFFECTS = (SHIELD,HOLYSYMBOL)
    TECH = (spells.waterspells.RESIST_ENERGY,)
    TYPE = ET_SECONDARY

class ResilentShield( Enhancer ):
    NAMEPAT = "{0} of Resilence"
    DESCPAT = "{0} It provides a bonus to toughness."
    PLUSRANK = 3
    AFFECTS = (SHIELD,)
    BONUSES_PER_RANK = stats.StatMod({ stats.TOUGHNESS:1 })
    UPRANKS = (2,5)
    TYPE = ET_SECONDARY

class ElementalShield( Enhancer ):
    NAMEPAT = "Elemental {0}"
    DESCPAT = "{0} It has been warded to provide 20% protection against fire, cold, lightning, and acid."
    PLUSRANK = 4
    AFFECTS = (SHIELD,)
    BONUSES_PER_RANK = stats.StatMod({ stats.RESIST_FIRE:20, stats.RESIST_COLD: 20, stats.RESIST_LIGHTNING: 20, stats.RESIST_ACID: 20 })
    UPRANKS = (1,2,3,5)
    TYPE = ET_SECONDARY

#  *******************************
#  ***   CLOAK  ENHANCEMENTS   ***
#  *******************************

class DefenseCloak( Enhancer ):
    NAMEPAT = "{0} of Defense +{2}"
    DESCPAT = "{0} It has been enhanced to provide a bonus to defense."
    PLUSRANK = 2
    AFFECTS = (CLOAK,)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })
    UPRANKS = (2,3,4,6)
    TYPE = ET_PRIMARY

class ElvenCloak( Enhancer ):
    NAMEPAT = "Elven {0}"
    DESCPAT = "{0} Its fine construction provides a +5% bonus to aura and stealth."
    PLUSRANK = 2
    AFFECTS = (CLOAK,)
    BONUSES_PER_RANK = stats.StatMod({ stats.MAGIC_DEFENSE: 5, stats.STEALTH: 5 })

class HealthCloak( Enhancer ):
    NAMEPAT = "{0} of Health +{2}"
    DESCPAT = "{0} It provides a bonus to toughness."
    PLUSRANK = 4
    AFFECTS = (CLOAK,CLOTHES)
    BONUSES_PER_RANK = stats.StatMod({ stats.TOUGHNESS:1 })
    TYPE = ET_PRIMARY
    UPRANKS = (1,2,3,4,5)

class ProtectionCloak( Enhancer ):
    NAMEPAT = "{1} of Protection"
    DESCPAT = "{0} It has been warded to provide 20% protection against fire, cold, lightning, and acid."
    PLUSRANK = 7
    AFFECTS = (CLOAK,)
    BONUSES_PER_RANK = stats.StatMod({ stats.RESIST_FIRE:20, stats.RESIST_COLD: 20, stats.RESIST_LIGHTNING: 20, stats.RESIST_ACID: 20 })
    TYPE = ET_PRIMARY

#  ********************
#  ***   HEADGEAR   ***
#  ********************

class AwareHat( Enhancer ):
    NAMEPAT = "{1} of Awareness"
    DESCPAT = "{0} It provides a +20% bonus to awareness and allows use of the Probe spell."
    PLUSRANK = 2
    AFFECTS = (HAT,HELM)
    BONUSES_PER_RANK = stats.StatMod({ stats.AWARENESS:20 })
    TECH = (spells.airspells.PROBE,)
    TYPE = ET_PRIMARY

class TrickHat( Enhancer ):
    NAMEPAT = "{0} of Tricks"
    DESCPAT = "{0} Critters may be magically summoned from the hat."
    PLUSRANK = 3
    AFFECTS = (HAT,)
    TECH = (spells.earthspells.CALL_CRITTER,)
    TYPE = ET_PRIMARY

class SturdyHat( Enhancer ):
    NAMEPAT = "Sturdy {0}"
    DESCPAT = "{0} It is reinforced to provide an additional +5% to defense."
    PLUSRANK = 4
    AFFECTS = (HAT,HELM)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })

class SmartHat( Enhancer ):
    NAMEPAT = "{1} of Intelligence"
    DESCPAT = "{0} It provides a bonus to intelligence."
    PLUSRANK = 4
    AFFECTS = (HAT,HELM)
    BONUSES_PER_RANK = stats.StatMod({ stats.INTELLIGENCE:1 })
    TYPE = ET_PRIMARY
    UPRANKS = (1,2,3,4,5)

class PiousHat( Enhancer ):
    NAMEPAT = "{1} of Faith"
    DESCPAT = "{0} It provides a bonus to piety."
    PLUSRANK = 4
    AFFECTS = (HAT,HELM)
    BONUSES_PER_RANK = stats.StatMod({ stats.PIETY:1 })
    TYPE = ET_PRIMARY
    UPRANKS = (1,2,3,4,5)



#  **********************************
#  ***   GLOVES  AND  GAUNTLETS   ***
#  **********************************

class HandyGlove( Enhancer ):
    NAMEPAT = "Handy {0}"
    DESCPAT = "{0} They provide a bonus to disarm traps."
    PLUSRANK = 1
    AFFECTS = (GLOVE,GAUNTLET)
    BONUSES_PER_RANK = stats.StatMod({ stats.DISARM_TRAPS:10 })

class PunchingGlove( Enhancer ):
    NAMEPAT = "{1} of Punching +{2}"
    DESCPAT = "{0} They provide a bonus to kung fu."
    PLUSRANK = 2
    AFFECTS = (GLOVE,)
    BONUSES_PER_RANK = stats.StatMod({ stats.KUNG_FU:5 })
    TYPE = ET_PRIMARY
    UPRANKS = (2,3)

class SpikyGlove( Enhancer ):
    NAMEPAT = "Spiky {0}"
    DESCPAT = "{0} They provide a +5% bonus to attack."
    PLUSRANK = 3
    AFFECTS = (GLOVE,GAUNTLET)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_ATTACK: 5 })

class SpellcraftGlove( Enhancer ):
    NAMEPAT = "{1} of Spellcraft"
    DESCPAT = "{0} They provide a +5% bonus to magic."
    PLUSRANK = 3
    AFFECTS = (GLOVE,)
    BONUSES_PER_RANK = stats.StatMod({ stats.MAGIC_ATTACK: 5 })
    UPRANKS = (3,5)

class FireGlove( Enhancer ):
    NAMEPAT = "{0} of Fire"
    DESCPAT = "{0} The user may project an arc of fire from the fingertips."
    PLUSRANK = 4
    AFFECTS = (GLOVE,GAUNTLET)
    BONUSES_PER_RANK = stats.StatMod({ stats.RESIST_FIRE: 15 })
    TYPE = ET_PRIMARY
    TECH = ( invocations.Invocation( "Flamethrower",
        effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
            effects.HealthDamage( (2,5,0), stat_bonus=stats.TOUGHNESS, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
        ,), on_failure = (
            effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
        ,) ), com_tar=targetarea.Cone(reach=4), ai_tar=invocations.TargetEnemy()
      ), )

class StrengthGlove( Enhancer ):
    NAMEPAT = "{1} of Might +{2}"
    DESCPAT = "{0} They provide a bonus to strength."
    PLUSRANK = 4
    AFFECTS = (GLOVE,GAUNTLET)
    BONUSES_PER_RANK = stats.StatMod({ stats.STRENGTH:1 })
    TYPE = ET_PRIMARY
    UPRANKS = (1,2,3,4,5)

class SturdyGlove( Enhancer ):
    NAMEPAT = "Sturdy {0}"
    DESCPAT = "{0} They are reinforced to provide an additional +5% to defense."
    PLUSRANK = 6
    AFFECTS = (GLOVE,GAUNTLET)
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })

class AlchemicalGlove( Enhancer ):
    NAMEPAT = "Alchemical {0}"
    DESCPAT = "{0} They reduce acid damage by 25%."
    PLUSRANK = 3
    AFFECTS = (GLOVE,GAUNTLET)
    BONUSES_PER_RANK = stats.StatMod({ stats.RESIST_ACID: 25 })

class ForgeGlove( Enhancer ):
    NAMEPAT = "Forge {0}"
    DESCPAT = "{0} They reduce fire damage by 25%."
    PLUSRANK = 3
    AFFECTS = (GLOVE,GAUNTLET)
    BONUSES_PER_RANK = stats.StatMod({ stats.RESIST_FIRE: 25 })


#  ********************
#  ***   FOOTWEAR   ***
#  ********************

class FleetShoe( Enhancer ):
    NAMEPAT = "Fleet {0}"
    DESCPAT = "{0} They provide a bonus to natural defense."
    PLUSRANK = 3
    AFFECTS = (SANDALS,)
    BONUSES_PER_RANK = stats.StatMod({ stats.NATURAL_DEFENSE:5 })
    UPRANKS = (3,5)

class SilenceShoe( Enhancer ):
    NAMEPAT = "Silent {1}"
    DESCPAT = "{0} They provide a +5% bonus to stealth."
    PLUSRANK = 2
    AFFECTS = (SHOES,SANDALS,BOOTS)
    BONUSES_PER_RANK = stats.StatMod({ stats.STEALTH:5 })

class KickingShoe( Enhancer ):
    NAMEPAT = "{1} of Kicking"
    DESCPAT = "{0} They provide a bonus to kung fu."
    PLUSRANK = 3
    AFFECTS = (SHOES,SANDALS,BOOTS)
    BONUSES_PER_RANK = stats.StatMod({ stats.KUNG_FU:5 })
    UPRANKS = (3,5)

class ReflexShoe( Enhancer ):
    NAMEPAT = "{1} of Speed +{2}"
    DESCPAT = "{0} They provide a bonus to reflexes."
    PLUSRANK = 4
    AFFECTS = (SHOES,SANDALS,BOOTS)
    BONUSES_PER_RANK = stats.StatMod({ stats.REFLEXES:1 })
    TYPE = ET_PRIMARY
    UPRANKS = (1,2,3,4,5)

class RubberSoledShoe( Enhancer ):
    NAMEPAT = "Rubber Soled {1}"
    DESCPAT = "{0} They provide 25% resistance to lightning."
    PLUSRANK = 3
    AFFECTS = (SHOES,SANDALS,BOOTS)
    BONUSES_PER_RANK = stats.StatMod({ stats.RESIST_LIGHTNING:25 })

class WinterShoe( Enhancer ):
    NAMEPAT = "Winter {1}"
    DESCPAT = "{0} They provide 25% resistance to cold."
    PLUSRANK = 3
    AFFECTS = (SHOES,BOOTS)
    BONUSES_PER_RANK = stats.StatMod({ stats.RESIST_COLD:25 })


#  ***********************************
#  ***   HOLYSYMBOLS  AND  WANDS   ***
#  ***********************************

class Ajura( Enhancer ):
    NAMEPAT = "Ajura {0}"
    DESCPAT = "{0} It aids counterspells, providing +5% to aura."
    PLUSRANK = 3
    AFFECTS = (WAND,HOLYSYMBOL)
    BONUSES_PER_RANK = stats.StatMod({ stats.MAGIC_DEFENSE: 5 })

class Evoca( Enhancer ):
    NAMEPAT = "Evoca {0}"
    DESCPAT = "{0} It aids spellcasting, providing +5% to magic."
    PLUSRANK = 4
    AFFECTS = (WAND,HOLYSYMBOL)
    BONUSES_PER_RANK = stats.StatMod({ stats.MAGIC_ATTACK: 5 })


#  *************************
#  ***   MISCELLANEOUS   ***
#  *************************

class Lucky( Enhancer ):
    NAMEPAT = "Lucky {0}"
    DESCPAT = "{0} It provides bonuses to aura and defense."
    PLUSRANK = 3
    AFFECTS = ( HAT, HELM, GLOVE, \
        GAUNTLET, SANDALS, SHOES, BOOTS, CLOAK, HOLYSYMBOL )
    BONUSES_PER_RANK = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.NATURAL_DEFENSE: 5, stats.MAGIC_DEFENSE: 5 })
    TYPE = ET_PRIMARY
    FREQUENCY = 1


