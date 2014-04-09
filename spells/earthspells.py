from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import context
import invocations

# CIRCLE 1

EARTHBIND = Spell( "Earthbind",
    "Conjures plants which grab at travelers, making passage through the area very difficult.",
    effects.PlaceField( enchantments.Entanglement, anim=animobs.OrangeSparkle ),
    rank=1, gems={EARTH:1}, com_tar=targetarea.Blast(radius=4), mpfudge=1, ai_tar=invocations.vs_enemy )

CALL_CRITTER = Spell( "Call Critter",
    "This spell will summon a small woodland creature to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE}, 2, anim=animobs.OrangeSparkle ),
    rank=1, gems={EARTH:1}, com_tar=targetarea.SingleTarget(reach=2), mpfudge = 2 )

# CIRCLE 2

ACID_SPRAY = Spell( "Acid Spray",
    "This attack does 2d5 acid damage to a single target, and may corrode the target's armor.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (2,5,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_ACID, anim=animobs.GreenExplosion ),
        effects.OpposedRoll( def_stat=stats.TOUGHNESS, on_success = (
            effects.Enchant( enchantments.ArmorDamage, anim=animobs.OrangeSparkle )
        ,))
    ), on_failure = (
        effects.HealthDamage( (1,5,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
    ,) ), rank=2, gems={EARTH:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.GreenSpray,
    ai_tar=invocations.vs_enemy )

# CIRCLE 3

SHAPE_FLESH = Spell( "Shape Flesh",
    "By touching a living creature, you may reshape its flesh so as to either cause or cure 3-18 damage.",
    effects.TargetIs( effects.ALIVE, on_true= (
        effects.TargetIsAlly( on_true=(
            effects.HealthRestore( dice=(3,6,0) ), ),),
        effects.TargetIsEnemy( on_true=(
            effects.HealthDamage( (3,6,0), stat_bonus=None, element=stats.RESIST_ATOMIC, anim=animobs.RedBoom )
        ,))
    )),
    rank=3, gems={EARTH:2}, com_tar=targetarea.SingleTarget(reach=1),
    exp_tar=targetarea.SinglePartyMember(), mpfudge = -1 )


# CIRCLE 4

# CIRCLE 5

# CIRCLE 6

# CIRCLE 7

# CIRCLE 8

# CIRCLE 9



