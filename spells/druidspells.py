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

ACID_SPRAY = Spell( "Acid Spray",
    "A stream of acid sprays forth, burning enemies for 1d6 damage. This spell has a short range but can affect several targets.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (1,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
    ,), on_failure = (
        effects.HealthDamage( (1,2,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
    ,) ), rank=1, gems={FIRE:1,EARTH:1}, com_tar=targetarea.Cone(reach=3), ai_tar=invocations.vs_enemy )


# CIRCLE TWO

CALL_ANIMAL = Spell( "Call Animal",
    "This spell will summon a natural creature to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 4, anim=animobs.OrangeSparkle ),
    rank=2, gems={EARTH:1,SOLAR:1}, com_tar=targetarea.SingleTarget(reach=2), mpfudge = 4 )

# CIRCLE THREE

CALL_CREATURE = Spell( "Call Creature",
    "This spell will summon a large natural creature to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 6, anim=animobs.OrangeSparkle ),
    rank=3, gems={EARTH:2,SOLAR:1}, com_tar=targetarea.SingleTarget(reach=2), mpfudge = 6 )

# CIRCLE FOUR

CALL_BEAST = Spell( "Call Beast",
    "This spell will summon a powerful creature to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 8, anim=animobs.OrangeSparkle ),
    rank=4, gems={EARTH:2,SOLAR:1}, com_tar=targetarea.SingleTarget(reach=2), mpfudge = 9 )

# CIRCLE FIVE

CALL_MONSTER = Spell( "Call Monster",
    "This spell will summon a powerful monster to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 10, anim=animobs.OrangeSparkle ),
    rank=5, gems={EARTH:2,SOLAR:2}, com_tar=targetarea.SingleTarget(reach=2), mpfudge = 10 )

# CIRCLE SIX

CALL_BEHEMOTH = Spell( "Call Behemoth",
    "This spell will summon a very powerful monster to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 12, anim=animobs.OrangeSparkle ),
    rank=6, gems={EARTH:2,SOLAR:2}, com_tar=targetarea.SingleTarget(reach=2), mpfudge = 12 )


# CIRCLE SEVEN

CALL_COLOSSUS = Spell( "Call Colossus",
    "This spell will summon an extremely powerful monster to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 14, anim=animobs.OrangeSparkle ),
    rank=7, gems={EARTH:2,SOLAR:2}, com_tar=targetarea.SingleTarget(reach=2), mpfudge = 14 )


# CIRCLE EIGHT

CALL_JUGGERNAUT = Spell( "Call Juggernaut",
    "This spell will summon a nigh-unstoppable monster to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 16, anim=animobs.OrangeSparkle ),
    rank=8, gems={EARTH:3,SOLAR:2}, com_tar=targetarea.SingleTarget(reach=3), mpfudge = 16 )


NATURAL_DISASTER = Spell( "Natural Disaster",
    "Causes massive fire damage in a five tile radius.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (10,10,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.Nuclear )
    ,), on_failure = (
        effects.HealthDamage( (5,10,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.Nuclear )
    ,) ), rank=8, gems={EARTH:2,FIRE:3}, com_tar=targetarea.Blast(radius=5, delay_from=1), shot_anim=animobs.BigMeteor,
    ai_tar=invocations.vs_enemy )

# CIRCLE NINE

CALL_LEVIATHAN = Spell( "Call Leviathan",
    "This spell will summon a legendary monster to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 18, anim=animobs.OrangeSparkle ),
    rank=9, gems={EARTH:3,SOLAR:3}, com_tar=targetarea.SingleTarget(reach=4), mpfudge = 20 )




