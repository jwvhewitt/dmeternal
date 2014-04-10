from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import invocations

# CIRCLE ONE

AIR_ARMOR = Spell( "Shield of Wind",
    "Increases the physical and magical defense of all allies within 6 tiles by +5%. This effect lasts until the end of combat.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.AirArmor, anim=animobs.BlueSparkle )
    ,) ), rank=1, gems={AIR:1}, com_tar=targetarea.SelfCentered() )

PROBE = Spell( "Probe",
    "This spell reveals secret knowledge about one target creature.",
    effects.NoEffect( anim=animobs.BlueSparkle, children = (
        effects.Probe()
    ,) ), rank=1, gems={AIR:1}, mpfudge=-1, com_tar=targetarea.SingleTarget(), exp_tar=targetarea.SingleTarget() )

# CIRCLE TWO

SILENCE = Spell( "Silence",
    "Causes living creatures in a 2 tile radius to fall asleep.",
    effects.OpposedRoll( att_modifier=0, on_success = (
        effects.CauseSilence(),
    ), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom ),
    )),
    rank=2, gems={AIR:1}, com_tar=targetarea.Blast(radius=2), ai_tar=invocations.vs_enemy )

SHOUT = Spell( "Shout",
    "The caster's words become a sonic wave, doing 1d8 wind damage to all targets within reach.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (1,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.SonicHit )
    ,), on_failure = (
        effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.SonicHit )
    ,) ), rank=1, gems={AIR:2}, com_tar=targetarea.Cone(reach=3), ai_tar=invocations.vs_enemy )


# CIRCLE THREE

THUNDER_STRIKE = Spell( "Thunder Strike",
    "A bolt of lightning strikes all in its path for 3d6 damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (3,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
    ,), on_failure = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
    ,) ), rank=3, gems={AIR:1}, com_tar=targetarea.Line(), ai_tar=invocations.vs_enemy )

MAGIC_MAP = Spell( "Magic Map",
    "This spell reveals detailed knowledge about the local area.",
    effects.MagicMap( anim=animobs.BlueSparkle ),
     rank=3, gems={AIR:2}, mpfudge=8, com_tar=targetarea.SelfOnly(), exp_tar=targetarea.SelfOnly() )


# CIRCLE FOUR



# CIRCLE FIVE

TORNADO = Spell( "Tornado",
    "Conjures a whirlwind which does 4d8 wind damage to all targets in a radius of 3 tiles.",
    effects.OpposedRoll( def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (4,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.Spiral )
    ,), on_failure = (
        effects.HealthDamage( (1,16,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.Spiral )
    ,) ), rank=5, gems={AIR:3}, com_tar=targetarea.Blast(radius=3), shot_anim=animobs.Whirlwind, ai_tar=invocations.vs_enemy )


# CIRCLE SIX



# CIRCLE SEVEN



# CIRCLE EIGHT



# CIRCLE NINE






