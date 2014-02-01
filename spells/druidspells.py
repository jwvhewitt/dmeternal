from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import context
import invocations

# Druids get EARTH, FIRE, and SOLAR magic. These spells use a combination of
# those colors.

# CIRCLE ONE


# CIRCLE TWO

CALL_ANIMAL = Spell( "CALL_ANIMAL", "Call Animal",
    "This spell will summon a natural creature to fight on your behaf.",
    effects.CallMonster( {context.MTY_BEAST: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 4, anim=animobs.OrangeSparkle ),
    rank=2, gems={EARTH:1,SOLAR:1}, com_tar=targetarea.SingleTarget(reach=2), mpfudge = 4 )

# CIRCLE THREE

CALL_BEAST = Spell( "CALL_BEAST", "Call Beast",
    "This spell will summon a large natural creature to fight on your behaf.",
    effects.CallMonster( {context.MTY_BEAST: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 6, anim=animobs.OrangeSparkle ),
    rank=3, gems={EARTH:2,SOLAR:1}, com_tar=targetarea.SingleTarget(reach=2), mpfudge = 6 )

# CIRCLE FOUR

CALL_MONSTER = Spell( "CALL_MONSTER", "Call Monster",
    "This spell will summon a powerful creature to fight on your behaf.",
    effects.CallMonster( {context.MTY_BEAST: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 8, anim=animobs.OrangeSparkle ),
    rank=4, gems={EARTH:2,SOLAR:1}, com_tar=targetarea.SingleTarget(reach=2), mpfudge = 9 )


# CIRCLE EIGHT

NATURAL_DISASTER = Spell( "NATURAL_DISASTER", "Natural Disaster",
    "Causes massive fire damage in a five tile radius.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (20,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.Nuclear )
    ,), on_failure = (
        effects.HealthDamage( (10,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.Nuclear )
    ,) ), rank=8, gems={EARTH:2,FIRE:3}, com_tar=targetarea.Blast(radius=5, delay_from=1), shot_anim=animobs.BigMeteor,
    ai_tar=invocations.vs_enemy )




