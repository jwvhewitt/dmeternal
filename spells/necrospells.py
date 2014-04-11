from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import context
import invocations

# Necromancers get EARTH, LUNAR, and WATER magic. These spells use at least two
# of those colors.

# CIRCLE ONE

ICE_BOLT = Spell( "Icy Bolt",
    "This attack does 1d8 cold damage to a single target.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (1,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.BlueExplosion )
    ,), on_failure = (
        effects.HealthDamage( (1,3,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.BlueExplosion )
    ,) ), rank=1, gems={LUNAR:1,WATER:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.BlueBolt, mpfudge=-2,
    ai_tar=invocations.vs_enemy )

RAISE_SKELETON = Spell( "Raise Skeleton",
    "You conjure dark forces to animate a skeleton which will fight on your behaf.",
    effects.CallMonster( {context.MTY_UNDEAD: True, context.DES_LUNAR: context.MAYBE, context.GEN_UNDEAD: context.MAYBE}, 2, anim=animobs.PurpleSparkle ),
    rank=1, gems={EARTH:1,LUNAR:1}, com_tar=targetarea.SingleTarget(reach=2) )

# CIRCLE 2

RAISE_CORPSE = Spell( "Raise Corpse",
    "You conjure dark forces to animate a lesser undead creature which will fight on your behaf.",
    effects.CallMonster( {context.MTY_UNDEAD: True, context.DES_LUNAR: context.MAYBE, context.GEN_UNDEAD: context.MAYBE}, 4, anim=animobs.PurpleSparkle ),
    rank=2, gems={EARTH:1,LUNAR:1}, com_tar=targetarea.SingleTarget(reach=2), mpfudge=4 )

# CIRCLE 3

ACID_CLOUD = Spell( "Acid Cloud",
    "Calls forth billowing clouds of acid which do 2d6 damage to all targets within 3 tiles.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (2,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_ACID, anim=animobs.GreenCloud )
    ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenCloud )
    ,) ), rank=3, gems={EARTH:1,LUNAR:1}, com_tar=targetarea.Blast(radius=3), shot_anim=animobs.GreenComet, ai_tar=invocations.vs_enemy )

# CIRCLE FOUR

# CIRCLE FIVE

# CIRCLE SIX

# CIRCLE SEVEN

# CIRCLE EIGHT

# CIRCLE NINE




