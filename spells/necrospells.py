from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import invocations

# Necromancers get EARTH, LUNAR, and WATER magic. These spells use at least two
# of those colors.

# CIRCLE ONE

ICE_BOLT = Spell( "ICE_BOLT", "Icy Bolt",
    "This attack does 1d8 cold damage to a single target.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (1,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.BlueExplosion )
    ,), on_failure = (
        effects.HealthDamage( (1,3,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.BlueExplosion )
    ,) ), rank=1, gems={LUNAR:1,WATER:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.BlueBolt, mpfudge=-2,
    ai_tar=invocations.vs_enemy )

