import stats
from . import Consumable,POTION
import enchantments
import animobs
import invocations
import targetarea
import effects


class PotionOfHealing( Consumable ):
    true_name = "Potion of Healing"
    true_desc = "This potion restores 3d6 damage instantly."
    itemtype = POTION
    mass_per_q = 4
    cost_per_q = 50
    tech = invocations.Invocation( "Healing",
        effects.HealthRestore( dice=(3,6,0) ),
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




