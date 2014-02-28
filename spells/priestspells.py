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

ARMOR_OF_FAITH = Spell( "ARMOR_OF_FAITH", "Armor of Faith",
    "The caster is infused with divine energy, healing wounds and bestowing protection.",
    effects.HealthRestore( dice=(2,6,0), anim=animobs.YellowSparkle, children = (
        effects.Enchant( enchantments.BlessingEn, anim=None ),
        effects.Enchant( enchantments.AirArmor, anim=None )
    ,) ), rank=1, gems={SOLAR:1,AIR:1}, com_tar=targetarea.SelfOnly(), mpfudge=-2 )

# CIRCLE TWO

WEAPON_BLESSING = Spell( "WEAPON_BLESSING", "Weapon Blessing",
    "One ally's weapon will be blessed to do an extra 1-8 points of damage.",
    effects.Enchant( enchantments.BlessedWepEn, anim=animobs.YellowSparkle ),
    rank=2, gems={AIR:1,SOLAR:1}, com_tar=targetarea.SinglePartyMember() )

DISPEL_EVIL = Spell( "DISPEL_EVIL", "Dispel Evil",
    "All unholy creatures within three tiles will be struck for 1-12 damage.",
    effects.TargetIs( pat=effects.UNHOLY, on_true = (
        effects.OpposedRoll( on_success = (
            effects.HealthDamage( (1,12,0), stat_bonus=stats.CHARISMA, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
        ,), on_failure = (
            effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
    ,) ) ,) ), rank=2, gems={SOLAR:1,WATER:1}, com_tar=targetarea.SelfCentered(radius=3,exclude_middle=True), mpfudge=-2,
    ai_tar=invocations.vs_enemy )


# CIRCLE THREE

# CIRCLE FOUR

BLIZZARD = Spell( "BLIZZARD", "Blizzard",
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


