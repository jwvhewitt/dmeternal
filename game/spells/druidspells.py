from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
from .. import effects
from .. import targetarea
from .. import enchantments
from .. import animobs
from .. import stats
from .. import context
from .. import invocations

# Druids get EARTH, FIRE, and SOLAR magic. These spells use a combination of
# those colors.

# CIRCLE ONE

ACID_SPRAY = Spell( "Acid Spray",
    "A stream of acid sprays forth, burning enemies for 1d6 damage. This spell has a short range but can affect several targets.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (1,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
    ,), on_failure = (
        effects.HealthDamage( (1,2,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
    ,) ), rank=1, gems={FIRE:1,EARTH:1}, com_tar=targetarea.Cone(reach=3), ai_tar=invocations.TargetEnemy() )


# CIRCLE TWO

CALL_ANIMAL = Spell( "Call Animal",
    "This spell will summon a natural creature to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 4, anim=animobs.OrangeSparkle ),
    rank=2, gems={EARTH:1,SOLAR:1}, com_tar=targetarea.SingleTarget(reach=2), ai_tar=invocations.TargetEmptySpot(), mpfudge = 4 )

    # Tame Animal (FS)
    # Wolf Form (EF)

# CIRCLE THREE

CALL_CREATURE = Spell( "Call Creature",
    "This spell will summon a large natural creature to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 6, anim=animobs.OrangeSparkle ),
    rank=3, gems={EARTH:2,SOLAR:1}, com_tar=targetarea.SingleTarget(reach=2), ai_tar=invocations.TargetEmptySpot(), mpfudge = 6 )

SLIMY_WEAPON = Spell( "Slimy Weapon",
    "One ally's weapon will be coated in caustic slime which causes an extra 1d10 acid damage and may corrode an opponent's armor.",
    effects.Enchant( enchantments.AcidWepEn, anim=animobs.OrangeSparkle ),
    rank=3, gems={EARTH:1}, com_tar=targetarea.SingleTarget(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.AcidWepEn) )

    # Firebird (FS)

# CIRCLE FOUR

CALL_BEAST = Spell( "Call Beast",
    "This spell will summon a powerful creature to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 8, anim=animobs.OrangeSparkle ),
    rank=4, gems={EARTH:2,SOLAR:1}, com_tar=targetarea.SingleTarget(reach=2), ai_tar=invocations.TargetEmptySpot(), mpfudge = 9 )

    # Tame Plants (FS)
    # Web (EF)

# CIRCLE FIVE

CALL_MONSTER = Spell( "Call Monster",
    "This spell will summon a powerful monster to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 10, anim=animobs.OrangeSparkle ),
    rank=5, gems={EARTH:2,SOLAR:2}, com_tar=targetarea.SingleTarget(reach=2), ai_tar=invocations.TargetEmptySpot(), mpfudge = 10 )

ELEMENTAL_STORM = Spell( "Elemental Storm",
    "The wrath of nature is brought to bear on your foes. All targets within a 3 tile radius take 2d4 damage from each of fire, cold, lightning, and acid.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (2,4,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion ),
        effects.HealthDamage( (2,4,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.BlueBoom ),
        effects.HealthDamage( (2,4,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap ),
        effects.HealthDamage( (2,4,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_ACID, anim=animobs.GreenSplat )
    ), on_failure = (
        effects.HealthDamage( (2,4,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion ),
        effects.HealthDamage( (2,4,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.BlueBoom ),
        effects.HealthDamage( (2,4,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap ),
        effects.HealthDamage( (2,4,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenSplat )
    ) ), rank=5, gems={FIRE:2,SOLAR:1}, com_tar=targetarea.Blast(radius=3), shot_anim=animobs.CrystalBall, 
    ai_tar=invocations.TargetEnemy(min_distance=4) )

TRANSFORMATION = Spell( "Transformation",
    "Transforms all allies within six tiles, providing +10% to defense plus 25% resistance to slashing, crushing, and piercing damage.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.WoodSkinEn, anim=animobs.OrangeSparkle ),
    )), rank=5, gems={EARTH:3,FIRE:1}, com_tar=targetarea.SelfCentered(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.WoodSkinEn) )


# CIRCLE SIX

CALL_BEHEMOTH = Spell( "Call Behemoth",
    "This spell will summon a very powerful monster to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 12, anim=animobs.OrangeSparkle ),
    rank=6, gems={EARTH:2,SOLAR:2}, com_tar=targetarea.SingleTarget(reach=2), ai_tar=invocations.TargetEmptySpot(), mpfudge = 12 )

    # Devouring Horde (EF)

# CIRCLE SEVEN

CALL_COLOSSUS = Spell( "Call Colossus",
    "This spell will summon an extremely powerful monster to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 14, anim=animobs.OrangeSparkle ),
    rank=7, gems={EARTH:2,SOLAR:2}, com_tar=targetarea.SingleTarget(reach=2), ai_tar=invocations.TargetEmptySpot(), mpfudge = 14 )

    # Elemental Form (EF)

# CIRCLE EIGHT

CALL_JUGGERNAUT = Spell( "Call Juggernaut",
    "This spell will summon a nigh-unstoppable monster to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 16, anim=animobs.OrangeSparkle ),
    rank=8, gems={EARTH:3,SOLAR:2}, com_tar=targetarea.SingleTarget(reach=3), ai_tar=invocations.TargetEmptySpot(), mpfudge = 16 )


NATURAL_DISASTER = Spell( "Natural Disaster",
    "Causes massive fire damage in a five tile radius.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (10,10,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.Nuclear )
    ,), on_failure = (
        effects.HealthDamage( (5,10,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.Nuclear )
    ,) ), rank=8, gems={EARTH:2,FIRE:3}, com_tar=targetarea.Blast(radius=5, delay_from=1), shot_anim=animobs.BigMeteor,
    ai_tar=invocations.TargetEnemy(min_distance=6) )

# CIRCLE NINE

CALL_LEVIATHAN = Spell( "Call Leviathan",
    "This spell will summon a legendary monster to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE, context.DES_SOLAR: context.MAYBE}, 18, anim=animobs.OrangeSparkle ),
    rank=9, gems={EARTH:3,SOLAR:3}, com_tar=targetarea.SingleTarget(reach=4), ai_tar=invocations.TargetEmptySpot(), mpfudge = 20 )

    # Dragon Form (EF)




