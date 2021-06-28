from .base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
from .. import effects
from .. import targetarea
from .. import enchantments
from .. import animobs
from .. import stats
from .. import invocations
from .. import context

# CIRCLE ONE

AIR_ARMOR = Spell( "Shield of Wind",
    "Increases the physical and magical defense of all allies within 6 tiles by +5%. This effect lasts until the end of combat.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.AirArmor, anim=animobs.BlueSparkle )
    ,) ), rank=1, gems={AIR:1}, com_tar=targetarea.SelfCentered(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.AirArmor) )

PROBE = Spell( "Probe",
    "This spell reveals secret knowledge about one target creature.",
    effects.NoEffect( anim=animobs.BlueSparkle, children = (
        effects.Probe()
    ,) ), rank=1, gems={AIR:1}, mpfudge=-1, com_tar=targetarea.SingleTarget(), exp_tar=targetarea.SingleTarget() )

# CIRCLE TWO

SILENCE = Spell( "Silence",
    "Targets within a 2 tile radius may be silenced, preventing them from casting spells.",
    effects.OpposedRoll( att_modifier=0, on_success = (
        effects.CauseSilence(),
    ), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom ),
    )),
    rank=2, gems={AIR:1}, com_tar=targetarea.Blast(radius=2), ai_tar=invocations.TargetEnemy() )

SHOUT = Spell( "Shout",
    "The caster's words become a sonic wave, doing 1d8 wind damage to all targets within reach.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (1,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.SonicHit )
    ,), on_failure = (
        effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.SonicHit )
    ,) ), rank=2, gems={AIR:2}, com_tar=targetarea.Cone(reach=4), ai_tar=invocations.TargetEnemy(), mpfudge=-1 )

# CIRCLE THREE

THUNDER_STRIKE = Spell( "Thunder Strike",
    "A bolt of lightning strikes all in its path for 3d6 damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (3,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
    ,), on_failure = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.Spark )
    ,) ), rank=3, gems={AIR:1}, com_tar=targetarea.Line(), ai_tar=invocations.TargetEnemy() )

MAGIC_MAP = Spell( "Magic Map",
    "This spell reveals detailed knowledge about the local area.",
    effects.MagicMap( anim=animobs.BlueSparkle ),
     rank=3, gems={AIR:2}, com_tar=targetarea.SelfOnly(), exp_tar=targetarea.SelfOnly() )


# CIRCLE FOUR

DISPEL_MAGIC = Spell( "Dispel Magic",
    "Deactivates all enchantments within a three tile radius, including both harmful and beneficial effects.",
    effects.TidyEnchantments( enchantments.MAGIC, anim=animobs.BlueSparkle ),
    rank=4, gems={AIR:2}, com_tar=targetarea.Blast(radius=3),
    exp_tar=targetarea.Blast(radius=3) )

    # Phantasmal Force?
    # Identify


# CIRCLE FIVE

TORNADO = Spell( "Tornado",
    "Conjures a whirlwind which does 4d8 wind damage to all targets in a radius of 3 tiles.",
    effects.OpposedRoll( def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (4,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.Spiral )
    ,), on_failure = (
        effects.HealthDamage( (1,16,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.Spiral )
    ,) ), rank=5, gems={AIR:3}, com_tar=targetarea.Blast(radius=3), shot_anim=animobs.Whirlwind,
    ai_tar=invocations.TargetEnemy(min_distance=4) )

    # Teleport

# CIRCLE SIX

DISMISSAL = Spell( "Dismissal",
    "Forces one demon, elemental, or spirit to leave the mortal realm and return to its home plane.",
    effects.TargetIs( effects.OTHERWORLDLY, anim=animobs.BlueSparkle, on_true=(
        effects.OpposedRoll( on_success = (
            effects.InstaKill( anim=animobs.CriticalHit )
        ,), on_failure = (
            effects.HealthDamage( (3,12,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion ), )
        ),
        ), on_false = (effects.NoEffect( anim=animobs.Caption ),)
    ), rank=6, gems={AIR:2}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.MysticBolt )

CALL_AIR_ELEMENTAL = Spell( "Call Air Elemental",
    "This spell will summon a living embodiment of the skies to fight on your behalf.",
    effects.CallMonster( {context.DES_AIR: True, context.SUMMON_ELEMENTAL: True }, 12, anim=animobs.BlueSparkle ),
    rank=6, gems={AIR:3}, com_tar=targetarea.SingleTarget(reach=5), ai_tar=invocations.TargetEmptySpot(), mpfudge = 12 )



# CIRCLE SEVEN

    # Identify All


# CIRCLE EIGHT

THUNDER_STORM = Spell( "Thunder Storm",
    "Calls down the wrath of the heavens. All targets within a 5 tile radius will be struck for 10d8 lightning damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (10,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LIGHTNING, anim=animobs.ThunderStorm )
    ,), on_failure = (
        effects.HealthDamage( (4,10,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.ThunderStorm )
    ,) ), rank=8, gems={AIR:5}, com_tar=targetarea.Blast(radius=5), 
    ai_tar=invocations.TargetEnemy(min_distance=6) )



# CIRCLE NINE

    # Wall of Force




