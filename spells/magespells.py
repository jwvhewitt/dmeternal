from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import invocations
import context

# Mages get AIR, FIRE, and LUNAR magic. These spells use a combination of colors.

# CIRCLE ONE

FIRE_ARC = Spell( "Fire Arc",
    "Conjures an arc of intense heat which burns enemies for 1d6 damage. This spell has a short range but can affect several targets.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (1,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )
    ,), on_failure = (
        effects.HealthDamage( (1,2,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )
    ,) ), rank=1, gems={FIRE:1,LUNAR:1}, com_tar=targetarea.Cone(reach=3), ai_tar=invocations.vs_enemy, mpfudge=-2 )

SHOCK_SPHERE = Spell( "Shock Sphere",
    "An electrical burst will deal 1-6 points of damage to all enemies within two tiles of the caster.",
    effects.TargetIsEnemy( on_true = (
        effects.OpposedRoll( on_success = (
            effects.HealthDamage( (1,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap )
        ,), on_failure = (
            effects.HealthDamage( (1,3,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap )
    ,) ) ,) ), rank=1, gems={AIR:1,LUNAR:1}, com_tar=targetarea.SelfCentered(radius=2,exclude_middle=True), mpfudge=-1,
    ai_tar=invocations.vs_enemy )

# CIRCLE TWO

LIGHTNING_BOLT = Spell( "Lightning Bolt",
    "This spell conjures magical lightning, which will unerringly hit one foe for 2d8 damage.",
    effects.HealthDamage((2,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap ),
    rank=2, gems={AIR:1,LUNAR:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.Lightning, ai_tar=invocations.vs_enemy,
    mpfudge=-2 )

# CIRCLE THREE

FIRE_SIGN = Spell( "Fire Sign",
    "Burns all enemies within 6 tiles with a flaming sigil, doing 2d4 damage and preventing them from hiding.",
    effects.TargetIsEnemy( on_true = (
        effects.OpposedRoll( on_success = (
            effects.HealthDamage( (2,4,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
        ,), on_failure = (
            effects.HealthDamage( (1,4,1), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
        ,)),
        effects.Enchant( enchantments.FireSignEn, anim=None )
    ) ), rank=3, gems={AIR:1,FIRE:1}, com_tar=targetarea.SelfCentered(), ai_tar=invocations.vs_enemy )


# CIRCLE FOUR

ANIMATION = Spell( "Animation",
    "This spell will temporarily imbue inanimate objects with life.",
    effects.CallMonster( {context.MTY_CONSTRUCT: True, context.DES_AIR: context.MAYBE, context.DES_FIRE: context.MAYBE}, 8, anim=animobs.RedSparkle ),
    rank=4, gems={AIR:1,FIRE:1}, com_tar=targetarea.SingleTarget(reach=2), mpfudge = 10 )

INCINERATE = Spell( "Incinerate",
    "Eldritch flames envelop a single foe, doing 6d6 fire damage and possibly setting the target alight.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (6,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.RedCloud ),
        effects.Enchant( enchantments.BurnLowEn )
    ), on_failure = (
        effects.HealthDamage( (2,8,1), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud ),
    ) ), rank=4, gems={FIRE:1,LUNAR:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.FireBolt, ai_tar=invocations.vs_enemy )


# CIRCLE FIVE

# CIRCLE SIX

EXTERMINATE = Spell( "Exterminate",
    "This spell produces a caustic spray which causes 3d8 acid damage and 3d8 poison damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (3,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_ACID, anim=animobs.GreenCloud ),
        effects.HealthDamage( (3,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_POISON, anim=animobs.PoisonCloud )
    ), on_failure = (
        effects.HealthDamage( (1,12,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenCloud ),
        effects.HealthDamage( (1,12,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud )
    ) ), rank=6, gems={AIR:1,LUNAR:2}, com_tar=targetarea.Cone(), ai_tar=invocations.vs_enemy )

# CIRCLE SEVEN

FLAMING_SWORD = Spell( "Flaming Sword",
    "Conjures an animated flaming sword, which will fight for your party until the end of combat.",
    effects.CallMonster( {context.SUMMON_FLAMINGSWORD: True, context.DES_AIR: context.MAYBE, context.DES_FIRE: context.MAYBE}, 14, anim=animobs.RedSparkle ),
    rank=7, gems={AIR:2,FIRE:2}, com_tar=targetarea.SingleTarget(reach=5), mpfudge = 16 )

FROSTFIRE = Spell( "Frostfire",
    "This spell creates a sphere of pure anti-fire, which freezes all targets in a 3 tile radius for 4d12 cold damage. The frostfire may continue to burn until the victim is frozen solid.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (4,12,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.SnowCloud ),
        effects.Enchant( enchantments.FrostBurnEn )
    ,), on_failure = (
        effects.HealthDamage( (4,8,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
    ,) ), rank=7, gems={FIRE:2,LUNAR:3}, com_tar=targetarea.Blast(radius=3), shot_anim=animobs.BlueComet, ai_tar=invocations.vs_enemy )

# CIRCLE EIGHT

METEOR_STORM = Spell( "Meteor Storm",
    "This spell calls down flaming rocks from the heavens, doing 10d8 fire damage and setting targets alight in a 4 tile radius.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (10,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.MeteorStorm ),
        effects.Enchant( enchantments.BurnLowEn )
    ), on_failure = (
        effects.HealthDamage( (3,12,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.MeteorStorm ),
    ) ), rank=8, gems={FIRE:2,AIR:2}, com_tar=targetarea.Blast(radius=4), ai_tar=invocations.vs_enemy )


# CIRCLE NINE





