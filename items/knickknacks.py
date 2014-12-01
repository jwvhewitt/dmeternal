import stats
from . import Consumable,GEM
import enchantments
import animobs
import invocations
import targetarea
import effects
import context

# Stuff that doesn't really fit into other categories.

class GemOfHolograms( Consumable ):
    true_name = "Gem of Holograms"
    true_desc = "This gem may be used to summon an illusory monster to aid you in combat."
    itemtype = GEM
    mass_per_q = 3
    cost_per_q = 600
    tech = invocations.Invocation( "Create Illusion",
        effects.CallMonster( {(context.HAB_EVERY,context.SET_EVERY): True}, 5, anim=animobs.BlueSparkle ),
        com_tar=targetarea.SingleTarget(reach=5), exp_tar=None )


class GemOfSeeing( Consumable ):
    true_name = "Gem of Seeing"
    true_desc = "You can peer into this gem for an overview of the surrounding area."
    itemtype = GEM
    mass_per_q = 3
    cost_per_q = 150
    tech = invocations.Invocation( "Scry",
        effects.MagicMap( anim=animobs.BlueSparkle ),
        com_tar=targetarea.SelfOnly(), exp_tar=targetarea.SelfOnly() )




