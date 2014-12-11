import stats
from . import Consumable,POTION
import enchantments
import animobs
import invocations
import targetarea
import effects


class PotionOfHealing( Consumable ):
    true_name = "Potion of Healing"
    true_desc = "This potion restores 3d8 damage instantly."
    itemtype = POTION
    mass_per_q = 4
    cost_per_q = 50
    tech = invocations.Invocation( "Healing",
        effects.HealthRestore( dice=(3,8,0) ),
        com_tar=targetarea.SelfOnly(), exp_tar=targetarea.SelfOnly() )

class PotionOfMana( Consumable ):
    true_name = "Potion of Mana"
    true_desc = "This potion restores 3d8 spell points instantly."
    itemtype = POTION
    mass_per_q = 4
    cost_per_q = 60
    tech = invocations.Invocation( "Recharge",
        effects.ManaRestore( dice=(3,8,0) ),
        com_tar=targetarea.SelfOnly(), exp_tar=targetarea.SelfOnly() )

class PotionOfCurePoison( Consumable ):
    true_name = "Antidote"
    true_desc = "This medicine counteracts poison."
    itemtype = POTION
    mass_per_q = 4
    cost_per_q = 75
    tech = invocations.Invocation( "Cure Poison",
        effects.TidyEnchantments( enchantments.POISON, anim=animobs.YellowSparkle ),
        com_tar=targetarea.SelfOnly(), exp_tar=targetarea.SelfOnly() )

class PotionOfStrength( Consumable ):
    true_name = "Potion of Strength"
    true_desc = "This potion grants a +4 bonus to strength and toughness, along with a +5% bonus to physical attack. The effect lasts until combat ends."
    itemtype = POTION
    mass_per_q = 4
    cost_per_q = 90
    tech = invocations.Invocation( "Strength",
        effects.Enchant( enchantments.BeastlyMightEn, anim=animobs.OrangeSparkle, ),
        com_tar=targetarea.SelfOnly(), exp_tar=None )

class PotionOfResistEnergy( Consumable ):
    true_name = "Potion of Resist Energy"
    true_desc = "This potion grants 50% resistance to fire, cold, lightning, and acid. The effect lasts for one day or until dispelled."
    itemtype = POTION
    mass_per_q = 4
    cost_per_q = 120
    tech = invocations.Invocation( "Resist Energy",
        effects.Enchant( enchantments.ResistEnergyEn, anim=animobs.GreenSparkle, alt_dispel=(enchantments.MAGIC,enchantments.DAILY) ),
        com_tar=targetarea.SelfOnly(), exp_tar=targetarea.SelfOnly() )

class PotionOfHeroism( Consumable ):
    true_name = "Potion of Heroism"
    true_desc = "This potion grants a +2 bonus to all stats. The effect lasts for one day or until dispelled."
    itemtype = POTION
    mass_per_q = 4
    cost_per_q = 150
    tech = invocations.Invocation( "Heroism",
        effects.Enchant( enchantments.HeroismEn, anim=animobs.YellowSparkle, alt_dispel=(enchantments.MAGIC,enchantments.DAILY) ),
        com_tar=targetarea.SelfOnly(), exp_tar=targetarea.SelfOnly() )





