from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import invocations

# Mages get AIR, FIRE, and LUNAR magic. These spells use a combination of colors.

# CIRCLE ONE

FIRE_ARC = Spell( "Fire Arc",
    "Conjures an arc of intense heat which burns enemies for 1d6 damage. This spell has a short range but can affect several targets.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (1,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )
    ,), on_failure = (
        effects.HealthDamage( (1,2,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )
    ,) ), rank=1, gems={FIRE:1,LUNAR:1}, com_tar=targetarea.Cone(reach=3), ai_tar=invocations.vs_enemy )

SHOCK_SPHERE = Spell( "Shock Sphere",
    "An electrical burst will deal 1-6 points of damage to all enemies within two tiles of the caster.",
    effects.TargetIsEnemy( on_true = (
        effects.OpposedRoll( on_success = (
            effects.HealthDamage( (1,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap )
        ,), on_failure = (
            effects.HealthDamage( (1,3,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap )
    ,) ) ,) ), rank=1, gems={AIR:1,LUNAR:1}, com_tar=targetarea.SelfCentered(radius=2,exclude_middle=True), mpfudge=-2,
    ai_tar=invocations.vs_enemy )

# CIRCLE TWO

# CIRCLE THREE



