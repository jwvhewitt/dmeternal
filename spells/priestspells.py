from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import context
import invocations

# Priests get AIR, SOLAR, and WATER magic. These spells use a mixture of two
# or more of those colors.

# CIRCLE ONE

ARMOR_OF_FAITH = Spell( "Armor of Faith",
    "The caster is infused with divine energy, healing wounds and bestowing protection.",
    effects.HealthRestore( dice=(2,6,0), anim=animobs.YellowSparkle, children = (
        effects.Enchant( enchantments.BlessingEn, anim=None ),
        effects.Enchant( enchantments.AirArmor, anim=None )
    ,) ), rank=1, gems={SOLAR:1,AIR:1}, com_tar=targetarea.SelfOnly(), mpfudge=-2 )

BLAST_UNDEAD = Spell( "Blast Undead",
    "This mystic bolt deals 1-6 damage to undead creatures.",
    effects.TargetIs( pat=effects.UNDEAD, on_true = (
        effects.HealthDamage((1,6,0), stat_bonus=stats.PIETY, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
    ,), on_false = (
        effects.NoEffect( anim=animobs.SmallBoom )
    ,) ),
    rank=1, gems={SOLAR:1,WATER:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.YellowBolt, mpfudge=-1 )


# CIRCLE TWO

WEAPON_BLESSING = Spell( "Weapon Blessing",
    "One ally's weapon will be blessed to do an extra 1-8 points of damage.",
    effects.Enchant( enchantments.BlessedWepEn, anim=animobs.YellowSparkle ),
    rank=2, gems={AIR:1,SOLAR:1}, com_tar=targetarea.SinglePartyMember() )

DISPEL_EVIL = Spell( "Dispel Evil",
    "All unholy creatures within three tiles will be struck for 1-12 damage.",
    effects.TargetIs( pat=effects.UNHOLY, on_true = (
        effects.OpposedRoll( on_success = (
            effects.HealthDamage( (1,12,0), stat_bonus=stats.CHARISMA, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
        ,), on_failure = (
            effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
    ,) ) ,) ), rank=2, gems={SOLAR:1,WATER:1}, com_tar=targetarea.SelfCentered(radius=3,exclude_middle=True), mpfudge=-2,
    ai_tar=invocations.vs_enemy )


# CIRCLE THREE

HEALING_LIGHT = Spell( "Healing Light",
    "Blessed radiance will heal one ally for 3-24 damage.",
    effects.HealthRestore( dice=(3,8,0) ),
    rank=3, gems={AIR:1,SOLAR:2}, com_tar=targetarea.SingleTarget(reach=10), ai_tar=invocations.vs_wounded_ally,
    exp_tar=targetarea.SinglePartyMember(), shot_anim=animobs.YellowVortex )


# CIRCLE FOUR

BLIZZARD = Spell( "Blizzard",
    "Conjures a storm which causes 2d8 cold damage and 2d8 wind damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (2,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.Blizzard,
            on_success= (effects.HealthDamage( (2,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
            on_failure= (effects.HealthDamage( (2,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
            on_death= (effects.HealthDamage( (2,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
     )
    ,), on_failure = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.Blizzard,
            on_success= (effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
            on_failure= (effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
            on_death= (effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
     )
    ,) ), rank=4, gems={WATER:1,AIR:1}, com_tar=targetarea.Blast(radius=4, delay_from=1),
    ai_tar=invocations.vs_enemy )


