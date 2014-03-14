from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import invocations

# CIRCLE ONE

FIRE_BOLT = Spell( "Fire Bolt",
    "This attack does 1d8 fire damage when it hits.",
    effects.OpposedRoll( att_modifier=10, on_success = (
        effects.HealthDamage( (1,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )
    ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
    ,) ), rank=1, gems={FIRE:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.FireBolt, ai_tar=invocations.vs_enemy )

BURNING_WEAPON = Spell( "Burning Weapon",
    "Magical flames burst from an ally's weapon, causing an extra 1-6 points of damge per hit. This effect lasts until the end of combat.",
    effects.Enchant( enchantments.FireWepEn, anim=animobs.RedSparkle ),
    rank=1, gems={FIRE:1}, com_tar=targetarea.SinglePartyMember() )

# CIRCLE 2

# CIRCLE 3

EXPLOSION = Spell( "Explosion",
    "Causes a magical explosion which does 2d6 fire damage to all targets within 3 tiles.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (2,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
    ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
    ,) ), rank=3, gems={FIRE:2}, com_tar=targetarea.Blast(radius=3), shot_anim=animobs.Fireball, ai_tar=invocations.vs_enemy )

# CIRCLE 4



# CIRCLE 5

# CIRCLE 6


