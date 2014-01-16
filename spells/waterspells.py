from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats

# CIRCLE ONE

FREEZE_FOE = Spell( "FREEZE_FOE", "Freeze Foe",
    "A single target will be frozen in its tracks, unable to act for 1 to 3 rounds.",
    effects.OpposedRoll( on_success = (
        effects.Paralyze( max_duration = 3 )
    ,), on_failure =(
        effects.NoEffect( anim=animobs.SmallBoom )
    ,) ), rank=1, gems={WATER:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.BlueComet )

RESTORE_FLUIDITY = Spell( "RESTORE_FLUIDITY", "Restore Fluidity",
    "This spell restores mobility to an ally who has been paralyzed or sedated.",
    effects.RestoreMobility( anim=animobs.GreenSparkle ),
    rank=1, gems={WATER:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.BlueComet, mpfudge=-1 )

# CIRCLE 2

# CIRCLE 3

WINTER_WIND = Spell( "WINTER_WIND", "Winter Wind",
    "Conjures a cone of intense cold which freezes enemies for 2d6 damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (2,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.BlueCloud )
    ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.BlueCloud )
    ,) ), rank=3, gems={WATER:2}, com_tar=targetarea.Cone(reach=8) )



