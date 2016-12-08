from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
from .. import effects
from .. import targetarea
from .. import enchantments
from .. import animobs
from .. import stats
from .. import invocations
from .. import context

# Spells that cannot be learned by any basic class because they either require
# opposite colors (Solar-Lunar, Earth-Air, Water-Fire) or they require more than
# three colors.

# CIRCLE ONE


# CIRCLE TWO

CHAOS_BOLT = Spell( "Chaos Bolt",
    "This mystic bolt does 1d8 damage to health and an additional 1d8 damage to mana.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage((1,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion ),
        effects.ManaDamage((1,8,0), stat_bonus=stats.INTELLIGENCE, anim=animobs.PurpleExplosion ),
    ), on_failure = (
        effects.HealthDamage((1,4,0), stat_bonus=None, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion ),
        effects.ManaDamage((1,4,0), stat_bonus=None, anim=animobs.PurpleExplosion ),
    )),
    rank=2, gems={LUNAR:1,SOLAR:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.WizardMissile,
    ai_tar=invocations.TargetEnemy(), mpfudge=-3 )



# CIRCLE THREE

CHAOTIC_AID = Spell( "Chaotic Aid",
    "This spell calls forth a servant of chaos to aid you in battle.",
    effects.CallMonster( {context.GEN_CHAOS: True, context.MTY_FIGHTER: True}, 5, anim=animobs.OrangeSparkle ),
    rank=3, gems={EARTH:1,AIR:1}, com_tar=targetarea.SingleTarget(reach=2), ai_tar=invocations.TargetEmptySpot(), mpfudge = 3 )


# CIRCLE FOUR



# CIRCLE FIVE

# CIRCLE SIX


# CIRCLE SEVEN


# CIRCLE EIGHT



# CIRCLE NINE





