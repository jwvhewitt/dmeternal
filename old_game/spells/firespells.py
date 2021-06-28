from .base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
from .. import effects
from .. import targetarea
from .. import enchantments
from .. import animobs
from .. import stats
from .. import invocations
from .. import context

# CIRCLE ONE

FIRE_BOLT = Spell( "Fire Bolt",
    "This attack does 1d8 fire damage to a single target.",
    effects.OpposedRoll( att_modifier=10, on_success = (
        effects.HealthDamage( (1,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )
    ,), on_failure = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )
    ,) ), rank=1, gems={FIRE:1}, com_tar=targetarea.SingleTarget(),
    shot_anim=animobs.FireBolt, ai_tar=invocations.TargetEnemy() )

BURNING_WEAPON = Spell( "Burning Weapon",
    "Magical flames burst from an ally's weapon, causing an extra 1-6 points of damge per hit. This effect lasts until the end of combat.",
    effects.Enchant( enchantments.FireWepEn, anim=animobs.RedSparkle ),
    rank=1, gems={FIRE:1}, com_tar=targetarea.SinglePartyMember(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.FireWepEn) )

# CIRCLE 2

BLINDING_FLASH = Spell( "Blinding Flash",
    "A sudden flash of light will daze, and possibly stun, all enemies within 4 tiles.",
    effects.TargetIsEnemy( on_true = (
        effects.Enchant( enchantments.BlindedEn, anim=animobs.RedSparkle ),
        effects.OpposedRoll( att_modifier=-20, on_success = (
            effects.Paralyze( max_duration = 2 )
        ,) )
    ) ), rank=2, gems={FIRE:2}, com_tar=targetarea.SelfCentered(radius=4), ai_tar=invocations.TargetEnemy() )

IGNITE = Spell( "Ignite",
    "You touch one opponent, causing them to burst into flame. The target suffers 2d5 fire damage and may continue burning.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (2,5,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.Ignite ),
        effects.Enchant( enchantments.BurnLowEn )
    ,), on_failure = (
        effects.HealthDamage( (2,5,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.Ignite )
    ,) ), rank=2, gems={FIRE:1}, com_tar=targetarea.SingleTarget(reach=1),ai_tar=invocations.TargetEnemy(), mpfudge=-2 )

    # Rush

# CIRCLE 3

EXPLOSION = Spell( "Explosion",
    "Causes a magical explosion which does 2d6 fire damage to all targets within 3 tiles.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (2,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
    ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
    ,) ), rank=3, gems={FIRE:2}, com_tar=targetarea.Blast(radius=3), shot_anim=animobs.Fireball, 
    ai_tar=invocations.TargetEnemy(min_distance=4) )

    # Fire Shield

# CIRCLE 4

PYROTECHNICS = Spell( "Pyrotechnics",
    "Conjures magical fireworks which do 4d6 fire damage to all targets in a straight line.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (4,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.Ignite )
    ,), on_failure = (
        effects.HealthDamage( (1,12,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.Ignite )
    ,) ), rank=4, gems={FIRE:3}, com_tar=targetarea.Line(), ai_tar=invocations.TargetEnemy() )

    # Wall of Fire


# CIRCLE 5

HEAT_WAVE = Spell( "Heat Wave",
    "A rapidly expanding wall of heat is projected from your hands. Anyone standing in its way takes 6d6 points of fire damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (6,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.DragonFire )
    ,), on_failure = (
        effects.HealthDamage( (3,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.DragonFire )
    ,) ), rank=5, gems={FIRE:3}, com_tar=targetarea.Cone(), ai_tar=invocations.TargetEnemy() )


# CIRCLE 6

CALL_FIRE_ELEMENTAL = Spell( "Call Fire Elemental",
    "This spell will call forth a living vortex of fire to serve you for the duration of combat.",
    effects.CallMonster( {context.DES_FIRE: True, context.SUMMON_ELEMENTAL: True }, 12, anim=animobs.RedSparkle ),
    rank=6, gems={FIRE:3}, com_tar=targetarea.SingleTarget(reach=5), ai_tar=invocations.TargetEmptySpot(), mpfudge = 12 )

    # Quickness

# CIRCLE SEVEN

DISINTEGRATION = Spell( "Disintegration",
    "The primal flames of the universe are called forth to reduce a single target to dust. This spell does 10d10 atomic damage on a successful hit.",
    effects.OpposedRoll( att_modifier=10, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (10,10,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_ATOMIC, anim=animobs.Nuclear )
    ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
    ,) ), rank=7, gems={FIRE:3}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.Fireball, ai_tar=invocations.TargetEnemy() )


# CIRCLE EIGHT

    # Army of Fire

# CIRCLE NINE

NUCLEAR = Spell( "Nuclear",
    "This spell causes a massive explosion, doing 20d6 atomic damage to all targets in a 4 tile radius.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (20,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_ATOMIC, anim=animobs.Nuclear )
    ,), on_failure = (
        effects.HealthDamage( (10,6,0), stat_bonus=None, element=stats.RESIST_ATOMIC, anim=animobs.Nuclear )
    ,) ), rank=9, gems={FIRE:5}, com_tar=targetarea.Blast(radius=4), shot_anim=animobs.Fireball,
    ai_tar=invocations.TargetEnemy(min_distance=5) )



